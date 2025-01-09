from application import app, db
from application.models import User
from werkzeug.security import generate_password_hash

def create_admin_user():
    with app.app_context():
        # Check if admin user exists
        admin = User.objects(email='admin@example.com').first()
        
        if not admin:
            # Create admin user
            admin = User(
                email='admin@example.com',
                first_name='Admin',
                last_name='User',
                role='admin'
            )
            admin.set_password('admin123')  # Set a default password
            admin.save()
            print("Admin user created successfully!")
            print("Email: admin@example.com")
            print("Password: admin123")
        else:
            print("Admin user already exists!")
            print("Email: admin@example.com")

if __name__ == '__main__':
    create_admin_user()
