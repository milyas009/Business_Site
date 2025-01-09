import os
from dotenv import load_dotenv

load_dotenv()

class Config(object):
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'your-secret-key-here'
    
    MONGODB_SETTINGS = {
        'db': 'business_site',
        'host': os.environ.get('MONGODB_URI', 'mongodb://localhost:27017/business_site')
    }
    
    # Flask-Login configuration
    LOGIN_DISABLED = False
    LOGIN_VIEW = 'auth.login'
    LOGIN_MESSAGE_CATEGORY = 'info'
    
    # Flask-WTF configuration
    WTF_CSRF_ENABLED = True
    WTF_CSRF_SECRET_KEY = os.environ.get('WTF_CSRF_SECRET_KEY') or 'csrf-key-here'