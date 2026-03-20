# InvenTrack — Inventory Management System

A modern inventory management system with a premium web interface, CLI access, and RESTful API. Built with Flask, SQLAlchemy, and a custom-designed UI.

## Features

- Real-time inventory tracking with low-stock alerts
- Sales transaction processing and history
- Admin panel with revenue reports and product management
- Role-based authentication (admin / user)
- Responsive sidebar layout with toast notifications
- CLI interface for terminal-based workflows
- SQLite database with SQLAlchemy ORM

## Quick Start

### Prerequisites

- Python 3.8+

### Setup

```bash
git clone https://github.com/Hrk84ya/Inventory-Management-System.git
cd Inventory-Management-System
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env
```

### Run

```bash
python run.py
```

Open `http://localhost:8000` — login with `admin` / `admin123`.

For the CLI version:

```bash
python run.py cli
```

## Project Structure

```
├── app.py              # Flask routes and app factory
├── models.py           # User, Product, Sale models
├── services.py         # Business logic layer
├── config.py           # App configuration
├── run.py              # Entry point (web + CLI)
├── cli.py              # Command-line interface
├── templates/          # Jinja2 templates
│   ├── base.html       #   Sidebar layout (auth) / public layout
│   ├── index.html      #   Landing page
│   ├── login.html      #   Login page
│   ├── dashboard.html  #   Product table, stats, sales
│   └── admin.html      #   Reports, add product modal
├── static/
│   ├── css/style.css   # Custom design system
│   └── js/app.js       # Toast notifications, modals, API calls
└── tests/
    └── test_services.py
```

## API Endpoints

All endpoints require authentication via session cookie.

| Method | Endpoint | Description |
|--------|----------|-------------|
| `GET` | `/api/products` | List all products |
| `POST` | `/api/purchase` | Create a purchase (`product_id`, `quantity`) |
| `GET` | `/api/sales` | Current user's sales history |
| `POST` | `/api/admin/products` | Add product — admin only (`name`, `price`, `quantity`, `category`) |

## Configuration

Environment variables (`.env`):

| Variable | Default | Description |
|----------|---------|-------------|
| `SECRET_KEY` | `dev-secret-key` | Flask session secret |
| `DATABASE_URL` | `sqlite:///inventory.db` | Database connection string |
| `FLASK_ENV` | `development` | `development` or `production` |
| `LOW_STOCK_THRESHOLD` | `10` | Stock level that triggers alerts |

## Testing

```bash
pytest tests/ -v
pytest --cov=. tests/
```

## Deployment

1. Set `FLASK_ENV=production` and a strong `SECRET_KEY` in `.env`
2. Use a production WSGI server:
   ```bash
   pip install gunicorn
   gunicorn -w 4 -b 0.0.0.0:8000 "app:create_app()"
   ```
3. Put behind a reverse proxy (nginx) with SSL

