"""Business logic services for the Inventory Management System."""
from typing import List, Optional, Dict, Any
from models import db, Product, Sale, User
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class InventoryService:
    """Service class for inventory operations."""
    
    @staticmethod
    def get_all_products() -> List[Product]:
        """Get all products."""
        return Product.query.all()
    
    @staticmethod
    def get_product_by_id(product_id: int) -> Optional[Product]:
        """Get product by ID."""
        return Product.query.get(product_id)
    
    @staticmethod
    def search_products(query: str) -> List[Product]:
        """Search products by name or category."""
        return Product.query.filter(
            Product.name.contains(query) | Product.category.contains(query)
        ).all()
    
    @staticmethod
    def add_product(name: str, price: float, quantity: int, 
                   description: str = None, category: str = None) -> Product:
        """Add new product to inventory."""
        product = Product(
            name=name,
            price=price,
            quantity=quantity,
            description=description,
            category=category
        )
        db.session.add(product)
        db.session.commit()
        logger.info(f"Added product: {name}")
        return product
    
    @staticmethod
    def update_product(product_id: int, **kwargs) -> Optional[Product]:
        """Update product details."""
        product = Product.query.get(product_id)
        if not product:
            return None
        
        for key, value in kwargs.items():
            if hasattr(product, key):
                setattr(product, key, value)
        
        product.updated_at = datetime.utcnow()
        db.session.commit()
        logger.info(f"Updated product: {product.name}")
        return product
    
    @staticmethod
    def delete_product(product_id: int) -> bool:
        """Delete product from inventory."""
        product = Product.query.get(product_id)
        if not product:
            return False
        
        db.session.delete(product)
        db.session.commit()
        logger.info(f"Deleted product: {product.name}")
        return True
    
    @staticmethod
    def get_low_stock_products(threshold: int = 10) -> List[Product]:
        """Get products with low stock."""
        return Product.query.filter(Product.quantity <= threshold).all()

class SalesService:
    """Service class for sales operations."""
    
    @staticmethod
    def create_sale(user_id: int, product_id: int, quantity: int) -> Dict[str, Any]:
        """Create a new sale transaction."""
        product = Product.query.get(product_id)
        if not product:
            return {'success': False, 'message': 'Product not found'}
        
        if product.quantity < quantity:
            return {
                'success': False, 
                'message': f'Insufficient stock. Available: {product.quantity}'
            }
        
        # Create sale record
        total_amount = product.price * quantity
        sale = Sale(
            user_id=user_id,
            product_id=product_id,
            quantity=quantity,
            unit_price=product.price,
            total_amount=total_amount
        )
        
        # Update product quantity
        product.quantity -= quantity
        
        db.session.add(sale)
        db.session.commit()
        
        logger.info(f"Sale created: {quantity} x {product.name} = ${total_amount}")
        
        return {
            'success': True,
            'sale': sale.to_dict(),
            'message': 'Sale completed successfully'
        }
    
    @staticmethod
    def get_sales_by_user(user_id: int) -> List[Sale]:
        """Get all sales for a user."""
        return Sale.query.filter_by(user_id=user_id).all()
    
    @staticmethod
    def get_sales_report(days: int = 30) -> Dict[str, Any]:
        """Generate sales report for specified days."""
        start_date = datetime.utcnow() - timedelta(days=days)
        sales = Sale.query.filter(Sale.sale_date >= start_date).all()
        
        total_revenue = sum(sale.total_amount for sale in sales)
        total_transactions = len(sales)
        
        return {
            'period_days': days,
            'total_revenue': total_revenue,
            'total_transactions': total_transactions,
            'sales': [sale.to_dict() for sale in sales]
        }

class UserService:
    """Service class for user operations."""
    
    @staticmethod
    def create_user(username: str, email: str, phone: str, password: str) -> User:
        """Create new user."""
        user = User(username=username, email=email, phone=phone)
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        logger.info(f"Created user: {username}")
        return user
    
    @staticmethod
    def authenticate_user(username: str, password: str) -> Optional[User]:
        """Authenticate user credentials."""
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            return user
        return None