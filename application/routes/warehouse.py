from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from application.models import Product, Inventory, InventoryTransaction, Warehouse
from datetime import datetime

warehouse = Blueprint('warehouse', __name__, url_prefix='/warehouse')

@warehouse.route('/dashboard')
@login_required
def dashboard():
    if current_user.role not in ['warehouse_manager', 'admin']:
        flash('Access denied. This page is only for warehouse managers.', 'danger')
        return redirect(url_for('main.index'))
    
    stats = {
        'total_products': Product.objects().count(),
        'low_stock_items': Product.objects(stock_level__lt=10).count(),
        'pending_shipments': InventoryTransaction.objects(status='pending').count(),
        'total_value': sum(prod.stock_level * prod.unit_price for prod in Product.objects())
    }
    
    recent_transactions = InventoryTransaction.objects().order_by('-timestamp')[:10]
    low_stock_alerts = Product.objects(stock_level__lt=10)
    
    return render_template('warehouse/dashboard.html',
                         stats=stats,
                         recent_transactions=recent_transactions,
                         low_stock_alerts=low_stock_alerts)

@warehouse.route('/inventory')
@login_required
def inventory():
    products = Product.objects().order_by('name')
    return render_template('warehouse/inventory.html', products=products)

@warehouse.route('/transactions')
@login_required
def transactions():
    transactions = InventoryTransaction.objects().order_by('-timestamp')
    return render_template('warehouse/transactions.html', transactions=transactions)

@warehouse.route('/stock-adjustment', methods=['GET', 'POST'])
@login_required
def stock_adjustment():
    if request.method == 'POST':
        product_id = request.form.get('product_id')
        adjustment = int(request.form.get('adjustment'))
        reason = request.form.get('reason')
        
        product = Product.objects(id=product_id).first()
        if product:
            product.stock_level += adjustment
            product.save()
            
            transaction = InventoryTransaction(
                product=product,
                quantity=adjustment,
                type='adjustment',
                reason=reason,
                performed_by=current_user.id
            )
            transaction.save()
            
            flash('Stock adjustment recorded successfully', 'success')
        
    return redirect(url_for('warehouse.inventory'))

@warehouse.route('/shipments')
@login_required
def shipments():
    return render_template('warehouse/shipments.html')
