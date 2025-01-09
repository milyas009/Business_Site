from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from application.models import Franchise, Transaction, Product, FranchiseApplication
from datetime import datetime

franchise = Blueprint('franchise', __name__, url_prefix='/franchise')

@franchise.route('/dashboard')
@login_required
def dashboard():
    if current_user.role != 'franchisee':
        flash('Access denied. This page is only for franchisees.', 'danger')
        return redirect(url_for('main.index'))
    
    franchise = Franchise.objects(owner=current_user.id).first()
    if not franchise:
        flash('No franchise found. Please apply for a franchise first.', 'warning')
        return redirect(url_for('franchise.apply'))
    
    stats = {
        'total_sales': sum(t.amount for t in Transaction.objects(franchise=franchise.id)),
        'monthly_sales': sum(t.amount for t in Transaction.objects(franchise=franchise.id, 
                           timestamp__gte=datetime.utcnow().replace(day=1))),
        'inventory_value': sum(p.stock_level * p.unit_price for p in Product.objects(franchise=franchise.id)),
        'customer_count': Transaction.objects(franchise=franchise.id).distinct('customer').count()
    }
    
    recent_transactions = Transaction.objects(franchise=franchise.id).order_by('-timestamp')[:10]
    low_stock_items = Product.objects(franchise=franchise.id, stock_level__lt=10)
    
    return render_template('franchise/dashboard.html',
                         franchise=franchise,
                         stats=stats,
                         recent_transactions=recent_transactions,
                         low_stock_items=low_stock_items)

@franchise.route('/apply', methods=['GET', 'POST'])
@login_required
def apply():
    if request.method == 'POST':
        application = FranchiseApplication(
            applicant=current_user.id,
            business_name=request.form.get('business_name'),
            location=request.form.get('location'),
            experience=request.form.get('experience'),
            investment_amount=float(request.form.get('investment_amount')),
            status='pending'
        )
        application.save()
        flash('Your franchise application has been submitted successfully!', 'success')
        return redirect(url_for('franchise.application_status'))
    
    return render_template('franchise/apply.html')

@franchise.route('/application-status')
@login_required
def application_status():
    applications = FranchiseApplication.objects(applicant=current_user.id).order_by('-submit_date')
    return render_template('franchise/application_status.html', applications=applications)

@franchise.route('/inventory')
@login_required
def inventory():
    franchise = Franchise.objects(owner=current_user.id).first_or_404()
    products = Product.objects(franchise=franchise.id)
    return render_template('franchise/inventory.html', products=products)

@franchise.route('/sales')
@login_required
def sales():
    franchise = Franchise.objects(owner=current_user.id).first_or_404()
    transactions = Transaction.objects(franchise=franchise.id).order_by('-timestamp')
    return render_template('franchise/sales.html', transactions=transactions)

@franchise.route('/reports')
@login_required
def reports():
    return render_template('franchise/reports.html')
