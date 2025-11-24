"""Flask web application for Inventory Management System."""
from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from models import db, User, Product, Sale
from services import InventoryService, SalesService, UserService
from config import config
import logging
import os

def create_app(config_name=None):
    """Application factory pattern."""
    app = Flask(__name__)
    
    config_name = config_name or os.environ.get('FLASK_ENV', 'default')
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    
    login_manager = LoginManager()
    login_manager.init_app(app)
    login_manager.login_view = 'login'
    
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))
    
    # Configure logging
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    @app.route('/')
    def index():
        """Home page."""
        return render_template('index.html')
    
    @app.route('/login', methods=['GET', 'POST'])
    def login():
        """User login."""
        if request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            
            user = UserService.authenticate_user(username, password)
            if user:
                login_user(user)
                return redirect(url_for('dashboard'))
            
            flash('Invalid credentials')
        
        return render_template('login.html')
    
    @app.route('/logout')
    @login_required
    def logout():
        """User logout."""
        logout_user()
        return redirect(url_for('index'))
    
    @app.route('/dashboard')
    @login_required
    def dashboard():
        """User dashboard."""
        products = InventoryService.get_all_products()
        low_stock = InventoryService.get_low_stock_products()
        return render_template('dashboard.html', products=products, low_stock=low_stock)
    
    @app.route('/api/products')
    @login_required
    def api_products():
        """API endpoint for products."""
        products = InventoryService.get_all_products()
        return jsonify([product.to_dict() for product in products])
    
    @app.route('/api/purchase', methods=['POST'])
    @login_required
    def api_purchase():
        """API endpoint for purchases."""
        data = request.get_json()
        result = SalesService.create_sale(
            current_user.id,
            data['product_id'],
            data['quantity']
        )
        return jsonify(result)
    
    @app.route('/api/sales')
    @login_required
    def api_sales():
        """API endpoint for sales history."""
        sales = SalesService.get_sales_by_user(current_user.id)
        return jsonify([sale.to_dict() for sale in sales])
    
    @app.route('/admin')
    @login_required
    def admin():
        """Admin panel."""
        if current_user.role != 'admin':
            flash('Access denied')
            return redirect(url_for('dashboard'))
        
        report = SalesService.get_sales_report()
        return render_template('admin.html', report=report)
    
    @app.route('/api/admin/products', methods=['POST'])
    @login_required
    def api_admin_add_product():
        """Admin API to add product."""
        if current_user.role != 'admin':
            return jsonify({'success': False, 'message': 'Access denied'}), 403
        
        data = request.get_json()
        product = InventoryService.add_product(
            data['name'],
            data['price'],
            data['quantity'],
            data.get('description'),
            data.get('category')
        )
        return jsonify({'success': True, 'product': product.to_dict()})
    
    # Create tables
    with app.app_context():
        db.create_all()
        
        # Create default admin user if not exists
        if not User.query.filter_by(username='admin').first():
            admin = User(
                username='admin',
                email='admin@inventory.com',
                phone='1234567890',
                role='admin'
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            
        # Add sample products if none exist
        if not Product.query.first():
            sample_products = [
                ('Pencil', 2.0, 90, 'Writing instrument', 'Stationery'),
                ('Eraser', 5.0, 95, 'Rubber eraser', 'Stationery'),
                ('Sharpener', 5.0, 100, 'Pencil sharpener', 'Stationery'),
                ('Pen', 10.0, 100, 'Ball point pen', 'Stationery'),
                ('Ruler', 10.0, 68, '12 inch ruler', 'Stationery'),
                ('Chart Papers', 5.0, 150, 'A4 chart papers', 'Paper'),
                ('Notebooks', 20.0, 100, 'Spiral notebooks', 'Books')
            ]
            
            for name, price, qty, desc, cat in sample_products:
                product = Product(
                    name=name,
                    price=price,
                    quantity=qty,
                    description=desc,
                    category=cat
                )
                db.session.add(product)
            
            db.session.commit()
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)