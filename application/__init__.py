from flask import Flask
from flask_mongoengine import MongoEngine
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config

# Initialize Flask app
app = Flask(__name__)
app.config.from_object(Config)

# Initialize extensions
db = MongoEngine(app)
csrf = CSRFProtect(app)
login_manager = LoginManager(app)
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'

# Import models
from application.models import User

@login_manager.user_loader
def load_user(user_id):
    return User.objects(id=user_id).first()

# Register blueprints
from application.routes.main import main
from application.routes.auth import auth
from application.routes.admin import admin

app.register_blueprint(main)
app.register_blueprint(auth, url_prefix='/auth')
app.register_blueprint(admin, url_prefix='/admin')