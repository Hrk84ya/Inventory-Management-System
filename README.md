# Inventory Management System

A professional, full-featured inventory management system with both web and command-line interfaces.

## Features

### Core Functionality
- **Product Management**: Add, update, delete, and search products
- **Inventory Tracking**: Real-time stock monitoring with low stock alerts
- **Sales Management**: Complete transaction processing and history
- **User Authentication**: Secure login with role-based access control
- **Reporting**: Sales reports and analytics

### Technical Features
- **Web Interface**: Modern, responsive web UI built with Flask and Bootstrap
- **CLI Interface**: Command-line interface for terminal users
- **Database**: SQLite database with SQLAlchemy ORM
- **Security**: Password hashing, session management, input validation
- **Testing**: Comprehensive unit tests with pytest
- **Logging**: Structured logging for debugging and monitoring

## Installation

### Prerequisites
- Python 3.8 or higher
- pip package manager

### Setup
1. Clone the repository:
```bash
git clone https://github.com/Hrk84ya/Inventory-Management-System.git
cd Inventory-Management-System
```

2. Create virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirements.txt
```

4. Set up environment variables:
```bash
cp .env.example .env
# Edit .env with your configuration
```

## Usage

### Web Interface
Start the web application:
```bash
python run.py
```

Access the application at `http://localhost:5000`

**Default Login:**
- Username: `admin`
- Password: `admin123`

### Command Line Interface
Run the CLI version:
```bash
python run.py cli
```

### API Endpoints
- `GET /api/products` - List all products
- `POST /api/purchase` - Create a purchase
- `GET /api/sales` - Get sales history
- `POST /api/admin/products` - Add product (admin only)

## Project Structure

```
Inventory-Management-System/
├── app.py              # Flask web application
├── cli.py              # Command-line interface
├── models.py           # Database models
├── services.py         # Business logic layer
├── config.py           # Configuration management
├── run.py              # Main entry point
├── requirements.txt    # Python dependencies
├── .env                # Environment variables
├── templates/          # HTML templates
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── dashboard.html
│   └── admin.html
├── static/             # Static files (CSS, JS)
│   ├── css/style.css
│   └── js/app.js
└── tests/              # Unit tests
    └── test_services.py
```

## Development

### Running Tests
```bash
pytest tests/ -v
```

### Code Coverage
```bash
pytest --cov=. tests/
```

### Adding New Features
1. Update models in `models.py`
2. Add business logic to `services.py`
3. Create API endpoints in `app.py`
4. Add CLI commands to `cli.py`
5. Write tests in `tests/`

## Configuration

Environment variables in `.env`:
- `SECRET_KEY`: Flask secret key for sessions
- `DATABASE_URL`: Database connection string
- `FLASK_ENV`: Environment (development/production)
- `LOW_STOCK_THRESHOLD`: Stock level for alerts

## Security Features

- Password hashing with Werkzeug
- Session-based authentication
- Role-based access control (admin/user)
- Input validation and sanitization
- SQL injection prevention with ORM
- CSRF protection (Flask-WTF can be added)

## Database Schema

### Users
- id, username, email, phone, password_hash, role, created_at

### Products
- id, name, price, quantity, description, category, created_at, updated_at

### Sales
- id, user_id, product_id, quantity, unit_price, total_amount, sale_date

## API Documentation

### Authentication Required
All API endpoints require user authentication via session cookies.

### Product Management
- **GET /api/products**: Returns list of all products
- **POST /api/admin/products**: Create new product (admin only)

### Sales Management
- **POST /api/purchase**: Create purchase transaction
- **GET /api/sales**: Get user's sales history

## Deployment

### Production Setup
1. Set `FLASK_ENV=production` in `.env`
2. Use a production WSGI server (gunicorn, uWSGI)
3. Configure reverse proxy (nginx, Apache)
4. Use production database (PostgreSQL, MySQL)
5. Set up SSL/TLS certificates

### Docker Deployment
```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "run.py"]
```

## Contributing

1. Fork the repository
2. Create feature branch (`git checkout -b feature/new-feature`)
3. Commit changes (`git commit -am 'Add new feature'`)
4. Push to branch (`git push origin feature/new-feature`)
5. Create Pull Request


## Support

For support and questions:
- Create an issue on GitHub
- Email: hrk84ya@gmail.com

## Changelog

### Version 1.0.0
- Initial release
- Web and CLI interfaces
- User authentication
- Product and sales management
- Reporting features
- Unit tests and documentation