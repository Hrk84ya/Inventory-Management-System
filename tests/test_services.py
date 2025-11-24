"""Unit tests for service layer."""
import pytest
from models import db, Product, User, Sale
from services import InventoryService, SalesService, UserService
from app import create_app

@pytest.fixture
def app():
    """Create test app."""
    app = create_app('testing')
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['TESTING'] = True
    
    with app.app_context():
        db.create_all()
        yield app
        db.drop_all()

@pytest.fixture
def client(app):
    """Create test client."""
    return app.test_client()

class TestInventoryService:
    """Test inventory service methods."""
    
    def test_add_product(self, app):
        """Test adding a product."""
        with app.app_context():
            product = InventoryService.add_product("Test Product", 10.0, 50)
            assert product.name == "Test Product"
            assert product.price == 10.0
            assert product.quantity == 50
    
    def test_get_product_by_id(self, app):
        """Test getting product by ID."""
        with app.app_context():
            product = InventoryService.add_product("Test Product", 10.0, 50)
            retrieved = InventoryService.get_product_by_id(product.id)
            assert retrieved.name == "Test Product"
    
    def test_update_product(self, app):
        """Test updating product."""
        with app.app_context():
            product = InventoryService.add_product("Test Product", 10.0, 50)
            updated = InventoryService.update_product(product.id, price=15.0)
            assert updated.price == 15.0
    
    def test_low_stock_products(self, app):
        """Test low stock detection."""
        with app.app_context():
            InventoryService.add_product("Low Stock", 10.0, 5)
            InventoryService.add_product("High Stock", 10.0, 50)
            
            low_stock = InventoryService.get_low_stock_products(10)
            assert len(low_stock) == 1
            assert low_stock[0].name == "Low Stock"

class TestSalesService:
    """Test sales service methods."""
    
    def test_create_sale_success(self, app):
        """Test successful sale creation."""
        with app.app_context():
            # Create user and product
            user = UserService.create_user("testuser", "test@test.com", "1234567890", "password")
            product = InventoryService.add_product("Test Product", 10.0, 50)
            
            # Create sale
            result = SalesService.create_sale(user.id, product.id, 5)
            
            assert result['success'] is True
            assert result['sale']['quantity'] == 5
            assert result['sale']['total_amount'] == 50.0
            
            # Check product quantity updated
            updated_product = InventoryService.get_product_by_id(product.id)
            assert updated_product.quantity == 45
    
    def test_create_sale_insufficient_stock(self, app):
        """Test sale with insufficient stock."""
        with app.app_context():
            user = UserService.create_user("testuser", "test@test.com", "1234567890", "password")
            product = InventoryService.add_product("Test Product", 10.0, 5)
            
            result = SalesService.create_sale(user.id, product.id, 10)
            
            assert result['success'] is False
            assert 'Insufficient stock' in result['message']

class TestUserService:
    """Test user service methods."""
    
    def test_create_user(self, app):
        """Test user creation."""
        with app.app_context():
            user = UserService.create_user("testuser", "test@test.com", "1234567890", "password")
            assert user.username == "testuser"
            assert user.email == "test@test.com"
    
    def test_authenticate_user(self, app):
        """Test user authentication."""
        with app.app_context():
            user = UserService.create_user("testuser", "test@test.com", "1234567890", "password")
            
            # Test correct credentials
            auth_user = UserService.authenticate_user("testuser", "password")
            assert auth_user is not None
            assert auth_user.username == "testuser"
            
            # Test incorrect credentials
            auth_user = UserService.authenticate_user("testuser", "wrongpassword")
            assert auth_user is None