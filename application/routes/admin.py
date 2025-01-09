from flask import Blueprint, render_template, request, flash, redirect, url_for, jsonify
from flask_login import login_required, current_user
from application.models import User, Investment, Franchise, Transaction, FranchiseApplication, Report, ReportTemplate
from datetime import datetime, timedelta
from functools import wraps

admin = Blueprint('admin', __name__, url_prefix='/admin')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or current_user.role != 'admin':
            flash('Access denied. This page is only for administrators.', 'danger')
            return redirect(url_for('main.index'))
        return f(*args, **kwargs)
    return decorated_function

@admin.route('/dashboard')
@login_required
@admin_required
def dashboard():
    stats = {
        'total_users': User.objects().count(),
        'total_franchises': Franchise.objects().count(),
        'total_investment_value': sum(f.investment_amount for f in Franchise.objects()),
        'total_sales': sum(f.total_sales for f in Franchise.objects if hasattr(f, 'total_sales'))
    }
    
    recent_users = User.objects().order_by('-created_at')[:5]
    recent_applications = FranchiseApplication.objects().order_by('-submit_date')[:5]
    
    return render_template('admin/dashboard.html',
                         stats=stats,
                         recent_users=recent_users,
                         recent_applications=recent_applications)

@admin.route('/analytics')
@login_required
@admin_required
def analytics():
    # Get time range from query parameters
    days = int(request.args.get('days', 30))
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    # Calculate basic stats
    stats = {
        'total_users': User.objects().count(),
        'active_franchises': Franchise.objects(status='active').count(),
        'total_revenue': sum(f.total_sales for f in Franchise.objects if hasattr(f, 'total_sales')),
        'avg_rating': 4.5  # Placeholder - implement actual calculation
    }
    
    # Generate sample data for charts
    revenue_data = {
        'labels': [(end_date - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days-1, -1, -1)],
        'values': [1000 * (x+1) for x in range(days)]  # Sample data
    }
    
    demographics = {
        'labels': ['Investors', 'Franchisees', 'Admins', 'Others'],
        'values': [45, 30, 5, 20]  # Sample data
    }
    
    growth_data = {
        'labels': [(end_date - timedelta(days=x)).strftime('%Y-%m-%d') for x in range(days-1, -1, -1)],
        'user_growth': [100 + x*10 for x in range(days)],  # Sample data
        'revenue_growth': [1000 + x*100 for x in range(days)]  # Sample data
    }
    
    return render_template('admin/analytics.html',
                         stats=stats,
                         revenue_data=revenue_data,
                         demographics=demographics,
                         growth_data=growth_data)

@admin.route('/franchises')
@login_required
@admin_required
def franchises():
    # Get filter parameters
    status = request.args.get('status')
    region = request.args.get('region')
    performance = request.args.get('performance')
    search = request.args.get('search')
    
    # Base query
    query = Franchise.objects()
    
    # Apply filters
    if status:
        query = query.filter(status=status)
    if region:
        query = query.filter(region=region)
    if performance:
        if performance == 'high':
            query = query.filter(performance_score__gte=80)
        elif performance == 'medium':
            query = query.filter(performance_score__gte=50, performance_score__lt=80)
        else:
            query = query.filter(performance_score__lt=50)
    if search:
        query = query.filter(name__icontains=search)
    
    # Pagination
    page = request.args.get('page', 1, type=int)
    per_page = 10
    pagination = query.paginate(page=page, per_page=per_page)
    
    return render_template('admin/franchises.html',
                         franchises=pagination.items,
                         pagination=pagination,
                         regions=Franchise.objects().distinct('region'))

@admin.route('/franchise/<franchise_id>')
@login_required
@admin_required
def franchise_detail(franchise_id):
    franchise = Franchise.objects.get_or_404(id=franchise_id)
    return render_template('admin/franchise_detail.html', franchise=franchise)

@admin.route('/users')
@login_required
@admin_required
def users():
    users = User.objects().order_by('email')
    return render_template('admin/users.html', users=users)

@admin.route('/reports')
@login_required
@admin_required
def reports():
    recent_reports = Report.objects().order_by('-created_at')[:10]
    report_templates = ReportTemplate.objects()
    
    return render_template('admin/reports.html',
                         recent_reports=recent_reports,
                         report_templates=report_templates)

@admin.route('/generate_report', methods=['POST'])
@login_required
@admin_required
def generate_report():
    template_id = request.form.get('template')
    start_date = request.form.get('start_date')
    end_date = request.form.get('end_date')
    format = request.form.get('format', 'pdf')
    
    # Create report
    report = Report(
        name=f"Report_{datetime.utcnow().strftime('%Y%m%d_%H%M%S')}",
        template=template_id,
        generated_by=current_user.id,
        start_date=datetime.strptime(start_date, '%Y-%m-%d'),
        end_date=datetime.strptime(end_date, '%Y-%m-%d'),
        format=format
    ).save()
    
    # Generate report asynchronously
    #generate_report_task.delay(report.id)
    
    flash('Report generation started. You will be notified when it is ready.', 'success')
    return redirect(url_for('admin.reports'))

@admin.route('/franchise/approve/<application_id>', methods=['POST'])
@login_required
@admin_required
def approve_franchise(application_id):
    application = FranchiseApplication.objects.get_or_404(id=application_id)
    application.status = 'approved'
    application.save()
    
    # Create new franchise
    franchise = Franchise(
        owner=application.applicant,
        business_name=application.business_name,
        location=application.location,
        investment_amount=application.investment_amount,
        status='active'
    ).save()
    
    flash('Franchise application approved successfully!', 'success')
    return redirect(url_for('admin.franchises'))
