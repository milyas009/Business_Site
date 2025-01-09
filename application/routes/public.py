from flask import Blueprint, render_template, request, flash, redirect, url_for
from application.models import Product, Franchise

public = Blueprint('public', __name__)

@public.route('/')
def index():
    featured_products = Product.objects(status='funding', featured=True)[:3]
    return render_template('public/index.html', featured_products=featured_products)

@public.route('/about')
def about():
    return render_template('public/about.html')

@public.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        # Handle contact form submission
        flash('Thank you for your message! We will get back to you soon.', 'success')
        return redirect(url_for('public.contact'))
    return render_template('public/contact.html')

@public.route('/opportunities')
def opportunities():
    products = Product.objects(status='funding')
    return render_template('public/opportunities.html', products=products)

@public.route('/franchise-opportunities')
def franchise_opportunities():
    return render_template('public/franchise_opportunities.html')

@public.route('/success-stories')
def success_stories():
    successful_franchises = Franchise.objects(status='active', featured=True)
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
