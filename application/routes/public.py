from flask import Blueprint, render_template, request, flash, redirect, url_for
from application.models import Product, Franchise, FranchiseApplication
from flask_login import current_user

public = Blueprint('public', __name__)

@public.route('/')
def index():
    featured_products = Product.objects(status='funding', featured=True)[:3]
    featured_franchises = Franchise.objects(status='active', featured=True)[:3]
    return render_template('public/index.html', 
                         featured_products=featured_products,
                         featured_franchises=featured_franchises)

@public.route('/about')
def about():
    return render_template('public/about.html')

@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        name = request.form.get('name')
        email = request.form.get('email')
        subject = request.form.get('subject')
        message = request.form.get('message')
        
        # Here you would typically send an email or save to database
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('public/contact.html')

@public.route('/opportunities')
def opportunities():
    # Get filter parameters
    category = request.args.get('category')
    min_investment = request.args.get('min_investment', type=float)
    max_investment = request.args.get('max_investment', type=float)
    risk_level = request.args.get('risk_level')
    
    # Build query
    query = {'status': 'funding'}
    if category:
        query['category'] = category
    if min_investment:
        query['min_investment__gte'] = min_investment
    if max_investment:
        query['min_investment__lte'] = max_investment
    if risk_level:
        query['risk_level'] = risk_level
    
    products = Product.objects(**query).order_by('-created_at')
    categories = Product.objects.distinct('category')
    
    return render_template('public/invest.html', 
                         products=products,
                         categories=categories,
                         current_filters={
                             'category': category,
                             'min_investment': min_investment,
                             'max_investment': max_investment,
                             'risk_level': risk_level
                         })

@public.route('/opportunities/<product_id>')
def product_detail(product_id):
    product = Product.objects(id=product_id).first_or_404()
    similar_products = Product.objects(
        category=product.category,
        id__ne=product.id,
        status='funding'
    )[:3]
    return render_template('public/product_detail.html',
                         product=product,
                         similar_products=similar_products)

@public.route('/franchise/apply', methods=['GET', 'POST'])
def franchise_apply():
    if request.method == 'POST':
        if not current_user.is_authenticated:
            flash('Please login or register to submit a franchise application.', 'warning')
            return redirect(url_for('auth.login'))
        
        application = FranchiseApplication(
            applicant=current_user.id,
            business_name=request.form.get('business_name'),
            location=request.form.get('location'),
            experience=request.form.get('experience'),
            investment_amount=float(request.form.get('investment_amount')),
            business_plan=request.form.get('business_plan')
        )
        application.save()
        
        flash('Your franchise application has been submitted successfully!', 'success')
        return redirect(url_for('public.franchise_apply'))
        
    return render_template('public/franchise_apply.html')

@public.route('/success-stories')
def success_stories():
    successful_franchises = Franchise.objects(
        status='active',
        featured=True,
        success_story__exists=True
    )
    return render_template('public/success_stories.html', franchises=successful_franchises)

@public.route('/faq')
def faq():
    return render_template('public/faq.html')

@public.route('/terms')
def terms():
    return render_template('public/terms.html')

@public.route('/privacy')
def privacy():
    return render_template('public/privacy.html')
