from application import db, login_manager
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

class User(UserMixin, db.Document):
    meta = {'collection': 'users'}
    
    email = db.StringField(max_length=100, unique=True, required=True)
    password = db.StringField(required=True)
    first_name = db.StringField(max_length=50, required=True)
    last_name = db.StringField(max_length=50, required=True)
    role = db.StringField(choices=['investor', 'franchisee', 'warehouse_manager', 'admin'], default='investor')
    notification_preferences = db.DictField(default={
        'email_notifications': True,
        'investment_updates': True,
        'newsletter': False
    })
    privacy_settings = db.DictField(default={
        'profile_visible': True,
        'show_investments': True
    })
    created_at = db.DateTimeField(default=datetime.utcnow)
    last_login = db.DateTimeField()
    phone = db.StringField(max_length=20)
    address = db.StringField(max_length=200)
    profile_image = db.StringField()
    kyc_verified = db.BooleanField(default=False)
    kyc_documents = db.ListField(db.StringField())
    is_admin = db.BooleanField(default=False)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def get_id(self):
        return str(self.id)

class Product(db.Document):
    meta = {'collection': 'products'}
    
    name = db.StringField(max_length=100, required=True)
    description = db.StringField(max_length=500)
    category = db.StringField(max_length=50, required=True)
    price = db.DecimalField(precision=2, required=True)
    stock_level = db.IntField(default=0)
    min_investment = db.DecimalField(precision=2, required=True)
    expected_roi = db.DecimalField(precision=2)
    created_at = db.DateTimeField(default=datetime.utcnow)
    status = db.StringField(choices=['funding', 'active', 'sold_out'], default='funding')
    image_url = db.StringField()
    featured = db.BooleanField(default=False)
    total_investment_goal = db.DecimalField(precision=2, required=True)
    current_investment = db.DecimalField(precision=2, default=0)
    investment_deadline = db.DateTimeField()
    risk_level = db.StringField(choices=['low', 'medium', 'high'])
    warehouse_location = db.StringField()
    supplier_info = db.DictField()
    specifications = db.DictField()
    tags = db.ListField(db.StringField())

class Investment(db.Document):
    meta = {'collection': 'investments'}
    
    investor = db.ReferenceField('User', required=True)
    product = db.ReferenceField('Product', required=True)
    franchise = db.ReferenceField('Franchise')
    amount = db.DecimalField(precision=2, required=True)
    investment_date = db.DateTimeField(default=datetime.utcnow)
    status = db.StringField(choices=['active', 'completed', 'cancelled'], default='active')
    returns = db.DecimalField(precision=2, default=0)
    monthly_returns = db.ListField(db.DictField())
    exit_date = db.DateTimeField()
    investment_documents = db.ListField(db.StringField())
    notes = db.StringField()

class Franchise(db.Document):
    meta = {'collection': 'franchises'}
    
    owner = db.ReferenceField('User', required=True)
    business_name = db.StringField(max_length=100, required=True)
    location = db.StringField(max_length=200, required=True)
    address = db.StringField(max_length=200, required=True)
    phone = db.StringField(max_length=20)
    status = db.StringField(choices=['pending', 'active', 'suspended'], default='pending')
    opening_date = db.DateTimeField()
    created_at = db.DateTimeField(default=datetime.utcnow)
    license_number = db.StringField()
    territory = db.StringField()
    employee_count = db.IntField(default=0)
    monthly_revenue_target = db.DecimalField(precision=2)
    performance_metrics = db.DictField()
    contract_documents = db.ListField(db.StringField())
    featured = db.BooleanField(default=False)
    success_story = db.StringField()
    performance_score = db.IntField(default=0)
    rating = db.DecimalField(precision=1, default=0)
    revenue = db.DecimalField(precision=2, default=0)
    revenue_growth = db.DecimalField(precision=2, default=0)
    customer_satisfaction = db.DecimalField(precision=2, default=0)
    investment_amount = db.FloatField(required=True)
    total_sales = db.FloatField(default=0)

class FranchiseApplication(db.Document):
    meta = {'collection': 'franchise_applications'}
    
    applicant = db.ReferenceField('User', required=True)
    business_name = db.StringField(max_length=100, required=True)
    location = db.StringField(max_length=200, required=True)
    experience = db.StringField()
    investment_amount = db.DecimalField(precision=2, required=True)
    business_plan = db.StringField()
    status = db.StringField(choices=['pending', 'approved', 'rejected'], default='pending')
    submit_date = db.DateTimeField(default=datetime.utcnow)
    documents = db.ListField(db.StringField())
    notes = db.StringField()
    reviewed_by = db.ReferenceField('User')
    review_date = db.DateTimeField()

class Inventory(db.Document):
    meta = {'collection': 'inventory'}
    
    warehouse = db.ReferenceField('Warehouse', required=True)
    product = db.ReferenceField('Product', required=True)
    quantity = db.IntField(default=0)
    last_updated = db.DateTimeField(default=datetime.utcnow)
    min_stock_level = db.IntField(default=10)
    max_stock_level = db.IntField()
    location_in_warehouse = db.StringField()
    condition = db.StringField(choices=['new', 'good', 'damaged'])
    batch_number = db.StringField()
    expiry_date = db.DateTimeField()

class Warehouse(db.Document):
    meta = {'collection': 'warehouses'}
    
    name = db.StringField(max_length=100, required=True)
    location = db.StringField(max_length=200, required=True)
    capacity = db.IntField(required=True)
    manager = db.ReferenceField('User')
    status = db.StringField(choices=['active', 'inactive', 'maintenance'])
    sections = db.ListField(db.StringField())
    contact_info = db.DictField()

class Transaction(db.Document):
    meta = {'collection': 'transactions'}
    
    franchise = db.ReferenceField('Franchise', required=True)
    product = db.ReferenceField('Product', required=True)
    quantity = db.IntField(required=True)
    unit_price = db.DecimalField(precision=2, required=True)
    total_amount = db.DecimalField(precision=2, required=True)
    transaction_type = db.StringField(choices=['sale', 'restock', 'return', 'adjustment'], required=True)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    payment_method = db.StringField()
    customer_info = db.DictField()
    invoice_number = db.StringField()
    processed_by = db.ReferenceField('User')

class InventoryTransaction(db.Document):
    meta = {'collection': 'inventory_transactions'}
    
    warehouse = db.ReferenceField('Warehouse', required=True)
    product = db.ReferenceField('Product', required=True)
    quantity = db.IntField(required=True)
    transaction_type = db.StringField(choices=['inbound', 'outbound', 'transfer', 'adjustment'])
    status = db.StringField(choices=['pending', 'completed', 'cancelled'])
    source_location = db.StringField()
    destination_location = db.StringField()
    timestamp = db.DateTimeField(default=datetime.utcnow)
    performed_by = db.ReferenceField('User')
    reference_number = db.StringField()
    notes = db.StringField()

class Report(db.Document):
    meta = {'collection': 'reports'}
    
    name = db.StringField(max_length=100, required=True)
    type = db.StringField(required=True)
    format = db.StringField(required=True)
    status = db.StringField(default='processing')
    file_path = db.StringField()
    generated_at = db.DateTimeField(default=datetime.utcnow)
    generated_by = db.ReferenceField('User')

class ReportTemplate(db.Document):
    meta = {'collection': 'report_templates'}
    
    name = db.StringField(max_length=100, required=True)
    description = db.StringField()
    type = db.StringField(choices=['financial', 'performance', 'operational'], required=True)
    frequency = db.StringField(choices=['daily', 'weekly', 'monthly', 'quarterly'])
    data_points = db.ListField(db.StringField())
    template_file = db.StringField(required=True)
    created_at = db.DateTimeField(default=datetime.utcnow)
    last_modified = db.DateTimeField(default=datetime.utcnow)
    created_by = db.ReferenceField('User')

class AnalyticsData(db.Document):
    meta = {'collection': 'analytics_data'}
    
    metric = db.StringField(required=True)
    value = db.DecimalField(precision=2)
    timestamp = db.DateTimeField(default=datetime.utcnow)
    category = db.StringField()
    tags = db.ListField(db.StringField())
    source = db.StringField()
    metadata = db.DictField()