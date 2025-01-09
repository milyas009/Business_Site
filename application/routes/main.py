from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from application.models import Product, Investment, Franchise, Transaction
from datetime import datetime

main = Blueprint('main', __name__)

@main.route('/')
@main.route('/index')
@main.route('/home')
def index():
    featured_products = Product.objects(status='funding')[:3]
    return render_template("index.html", featured_products=featured_products)

@main.route('/investment-opportunities')
def investment_opportunities():
    products = Product.objects(status='funding')
    return render_template("products.html", products=products)

@main.route('/product/<product_id>')
def product_detail(product_id):
    product = Product.objects(id=product_id).first_or_404()
    return render_template("product_detail.html", product=product)

@main.route('/franchise')
def franchise():
    return render_template("franchise_apply.html")

@main.route('/about')
def about():
    return render_template("about.html")

@main.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('main.contact'))
    return render_template("contact.html")

@main.route('/market-analysis')
@login_required
def market_analysis():
    return render_template("market_analysis.html")

@main.route('/investment-analytics')
@login_required
def investment_analytics():
    investments = Investment.objects(investor=current_user.id)
    return render_template("investment_analytics.html", investments=investments)

@main.route('/manage-inventory')
@login_required
def manage_inventory():
    if current_user.role != 'franchisee':
        flash('Access denied. This page is only for franchisees.', 'danger')
        return redirect(url_for('main.index'))
    
    franchise = Franchise.objects(owner=current_user.id).first()
    if not franchise:
        flash('No franchise found. Please apply for a franchise first.', 'warning')
        return redirect(url_for('main.franchise'))
    
    return render_template("manage_inventory.html", franchise=franchise)

@main.route('/investor-dashboard')
@login_required
def investor_dashboard():
    if current_user.role not in ['investor', 'admin']:
        flash('Access denied. This page is only for investors.', 'danger')
        return redirect(url_for('main.index'))
    
    stats = {
        'total_investments': Investment.objects(investor=current_user.id, status='active').count(),
        'total_invested': sum(inv.amount for inv in Investment.objects(investor=current_user.id)),
        'avg_roi': Investment.objects(investor=current_user.id).average('returns') or 0,
        'franchise_count': Franchise.objects(owner=current_user.id).count()
    }
    
    recent_investments = Investment.objects(investor=current_user.id).order_by('-investment_date')[:5]
    market_data = {
        'labels': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun'],
        'values': [65, 59, 80, 81, 56, 55]
    }
    
    return render_template("investor_dashboard.html", 
                         stats=stats, 
                         recent_investments=recent_investments,
                         market_data=market_data)

@main.route('/franchise-dashboard')
@login_required
def franchise_dashboard():
    if current_user.role != 'franchisee':
        flash('Access denied. This page is only for franchisees.', 'danger')
        return redirect(url_for('main.index'))
    
    franchise = Franchise.objects(owner=current_user.id).first()
    if not franchise:
        flash('No franchise found. Please apply for a franchise first.', 'warning')
        return redirect(url_for('main.franchise'))
    
    recent_transactions = Transaction.objects(franchise=franchise.id).order_by('-timestamp')[:10]
    
    return render_template("franchise_dashboard.html", 
                         franchise=franchise,
                         recent_transactions=recent_transactions)

@main.route('/invest/<product_id>', methods=['GET', 'POST'])
@login_required
def invest(product_id):
    if current_user.role not in ['investor', 'admin']:
        flash('Access denied. This page is only for investors.', 'danger')
        return redirect(url_for('main.index'))
    
    product = Product.objects(id=product_id).first_or_404()
    if product.status != 'funding':
        flash('This investment opportunity is no longer available.', 'warning')
        return redirect(url_for('main.investment_opportunities'))
    
    if request.method == 'POST':
        amount = float(request.form.get('amount', 0))
        if amount < product.min_investment:
            flash(f'Minimum investment amount is ${product.min_investment}', 'danger')
        else:
            investment = Investment(
                investor=current_user.id,
                product=product.id,
                amount=amount,
                investment_date=datetime.utcnow()
            )
            investment.save()
            flash('Investment successful!', 'success')
            return redirect(url_for('main.investor_dashboard'))
            
    return render_template('invest.html', product=product)

@main.route('/profile', methods=['GET'])
@login_required
def profile():
    stats = {
        'total_investments': Investment.objects(investor=current_user.id, status='active').count(),
        'total_invested': sum(inv.amount for inv in Investment.objects(investor=current_user.id)),
        'avg_roi': Investment.objects(investor=current_user.id).average('returns') or 0
    }
    return render_template('profile.html', stats=stats)

@main.route('/update-profile', methods=['POST'])
@login_required
def update_profile():
    if request.method == 'POST':
        current_user.first_name = request.form.get('first_name')
        current_user.last_name = request.form.get('last_name')
        current_user.email = request.form.get('email')
        current_user.save()
        flash('Profile updated successfully!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/update-privacy', methods=['POST'])
@login_required
def update_privacy():
    if request.method == 'POST':
        current_user.privacy_settings = {
            'profile_visible': bool(request.form.get('profile_visible')),
            'show_investments': bool(request.form.get('show_investments'))
        }
        current_user.save()
        flash('Privacy settings updated!', 'success')
    return redirect(url_for('main.profile'))

@main.route('/update-notifications', methods=['POST'])
@login_required
def update_notifications():
    if request.method == 'POST':
        current_user.notification_preferences = {
            'email_notifications': bool(request.form.get('emailNotifications')),
            'investment_updates': bool(request.form.get('investmentUpdates')),
            'newsletter': bool(request.form.get('newsletter'))
        }
        current_user.save()
        flash('Notification preferences updated!', 'success')
    return redirect(url_for('main.profile'))
