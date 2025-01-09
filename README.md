# Retail Investment Platform

A comprehensive retail investment and franchise management platform built with Flask and MongoDB.

## Features

- Product Management and Investment Tracking
- Franchise Application and Management
- Investment Analytics Dashboard
- Market Analysis Tools
- User Authentication and Authorization
- Real-time Performance Tracking
- Inventory Management System

## Prerequisites

- Python 3.8+
- MongoDB 4.4+
- pip (Python package manager)

## Setup Instructions

1. Clone the repository:
```bash
git clone <repository-url>
cd Business_Site
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
.\venv\Scripts\activate  # On Windows
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Configure environment variables:
- Copy `.env.example` to `.env`
- Update MongoDB connection string and other settings in `.env`

5. Initialize the database:
```bash
flask init-db  # This command will be available after first run
```

6. Run the application:
```bash
flask run
```

The application will be available at `http://127.0.0.1:5000`

## Project Structure

```
Business_Site/
├── application/
│   ├── templates/    # HTML templates
│   ├── static/       # CSS, JS, and media files
│   ├── models.py     # Database models
│   └── routes.py     # Application routes
├── requirements.txt  # Python dependencies
└── .env             # Environment variables
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## License

This project is licensed under the MIT License - see the LICENSE file for details.
