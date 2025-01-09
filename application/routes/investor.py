from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from application.models import Product, Investment, Transaction
from datetime import datetime

investor = Blueprint('investor', __name__, url_prefix='/investor')

@investor.route('/dashboard')
@login_required
def dashboard():
    if current_user.role not in ['investor', 'admin']:
        flash('Access denied. This page is only for investors.', 'danger')
        return redirect(url_for('main.index'))
    
    stats = {
        'total_investments': Investment.objects(investor=current_user.id, status='active').count(),
        'total_invested': sum(inv.amount for inv in Investment.objects(investor=current_user.id)),
        'avg_roi': Investment.objects(investor=current_user.id).average('returns') or 0,
        'total_returns': sum(inv.returns for inv in Investment.objects(investor=current_user.id))
    }
    
    recent_investments = Investment.objects(investor=current_user.id).order_by('-investment_date')[:5]
    recent_transactions = Transaction.objects(investor=current_user.id).order_by('-timestamp')[:10]
    
    # Get portfolio distribution
    portfolio = {}
    for inv in Investment.objects(investor=current_user.id, status='active'):
        category = inv.product.category
        portfolio[category] = portfolio.get(category, 0) + inv.amount
    
    return render_template('investor/dashboard.html',
                         stats=stats,
                         recent_investments=recent_investments,
                         recent_transactions=recent_transactions,
                         portfolio=portfolio)

@investor.route('/investments')
@login_required
def investments():
    investments = Investment.objects(investor=current_user.id).order_by('-investment_date')
    return render_template('investor/investments.html', investments=investments)

@investor.route('/analytics')
@login_required
def analytics():
    # Get monthly returns data
    monthly_returns = []
    for inv in Investment.objects(investor=current_user.id):
        for return_data in inv.monthly_returns:
            monthly_returns.append({
                'date': return_data.date,
                'amount': return_data.amount,
                'product': inv.product.name
            })
    
    # Get portfolio performance
    portfolio_performance = {
        'total_invested': sum(inv.amount for inv in Investment.objects(investor=current_user.id)),
        'current_value': sum(inv.current_value for inv in Investment.objects(investor=current_user.id)),
        'total_returns': sum(inv.returns for inv in Investment.objects(investor=current_user.id))
    }
    
    return render_template('investor/analytics.html',
                         monthly_returns=monthly_returns,
                         portfolio_performance=portfolio_performance)

@investor.route('/opportunities')
@login_required
def opportunities():
    products = Product.objects(status='funding')
    return render_template('investor/opportunities.html', products=products)

@investor.route('/notifications')
@login_required
def notifications():
    return render_template('investor/notifications.html')
