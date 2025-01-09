import os

def setup_directories():
    """Create necessary directories for the application"""
    # Create reports directory
    reports_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'reports')
    if not os.path.exists(reports_dir):
        os.makedirs(reports_dir)
        print(f"Created reports directory at {reports_dir}")
    else:
        print(f"Reports directory already exists at {reports_dir}")

if __name__ == '__main__':
    setup_directories()
