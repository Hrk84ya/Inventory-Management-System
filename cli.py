"""Command-line interface for the Inventory Management System."""
import sys
from typing import Optional
from models import db, User
from services import InventoryService, SalesService, UserService
from app import create_app
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InventoryCLI:
    """Command-line interface for inventory management."""
    
    def __init__(self):
        self.app = create_app()
        self.current_user: Optional[User] = None
    
    def run(self):
        """Main CLI loop."""
        with self.app.app_context():
            print("=== Inventory Management System ===")
            
            if not self.login():
                print("Authentication failed. Exiting...")
                return
            
            while True:
                self.show_menu()
                choice = input("\nEnter your choice: ").strip()
                
                if choice == '1':
                    self.view_products()
                elif choice == '2':
                    self.search_products()
                elif choice == '3':
                    self.make_purchase()
                elif choice == '4':
                    self.view_sales_history()
                elif choice == '5':
                    self.view_low_stock()
                elif choice == '6':
                    if self.current_user.role == 'admin':
                        self.admin_menu()
                    else:
                        print("Access denied. Admin privileges required.")
                elif choice == '7':
                    print("Thank you for using Inventory Management System!")
                    break
                else:
                    print("Invalid choice. Please try again.")
    
    def login(self) -> bool:
        """User authentication."""
        print("\n--- Login ---")
        username = input("Username: ").strip()
        password = input("Password: ").strip()
        
        user = UserService.authenticate_user(username, password)
        if user:
            self.current_user = user
            print(f"Welcome, {user.username}!")
            return True
        
        print("Invalid credentials.")
        return False
    
    def show_menu(self):
        """Display main menu."""
        print(f"\n--- Main Menu (User: {self.current_user.username}) ---")
        print("1. View All Products")
        print("2. Search Products")
        print("3. Make Purchase")
        print("4. View Sales History")
        print("5. View Low Stock Items")
        if self.current_user.role == 'admin':
            print("6. Admin Panel")
        print("7. Exit")
    
    def view_products(self):
        """Display all products."""
        products = InventoryService.get_all_products()
        if not products:
            print("No products available.")
            return
        
        print("\n--- Product Inventory ---")
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Stock':<10} {'Category':<15}")
        print("-" * 70)
        
        for product in products:
            print(f"{product.id:<5} {product.name:<20} ${product.price:<9.2f} "
                  f"{product.quantity:<10} {product.category or 'N/A':<15}")
    
    def search_products(self):
        """Search for products."""
        query = input("Enter search term: ").strip()
        if not query:
            return
        
        products = InventoryService.search_products(query)
        if not products:
            print("No products found.")
            return
        
        print(f"\n--- Search Results for '{query}' ---")
        print(f"{'ID':<5} {'Name':<20} {'Price':<10} {'Stock':<10}")
        print("-" * 50)
        
        for product in products:
            print(f"{product.id:<5} {product.name:<20} ${product.price:<9.2f} {product.quantity:<10}")
    
    def make_purchase(self):
        """Process a purchase."""
        try:
            product_id = int(input("Enter Product ID: "))
            quantity = int(input("Enter Quantity: "))
            
            result = SalesService.create_sale(self.current_user.id, product_id, quantity)
            
            if result['success']:
                sale = result['sale']
                print("\n--- Purchase Successful ---")
                print(f"Product: {sale['product']}")
                print(f"Quantity: {sale['quantity']}")
                print(f"Unit Price: ${sale['unit_price']:.2f}")
                print(f"Total Amount: ${sale['total_amount']:.2f}")
            else:
                print(f"Purchase failed: {result['message']}")
                
        except ValueError:
            print("Invalid input. Please enter valid numbers.")
        except Exception as e:
            print(f"Error: {e}")
    
    def view_sales_history(self):
        """View user's sales history."""
        sales = SalesService.get_sales_by_user(self.current_user.id)
        if not sales:
            print("No sales history found.")
            return
        
        print("\n--- Your Sales History ---")
        print(f"{'Date':<20} {'Product':<20} {'Qty':<5} {'Total':<10}")
        print("-" * 60)
        
        for sale in sales:
            date_str = sale.sale_date.strftime("%Y-%m-%d %H:%M")
            print(f"{date_str:<20} {sale.product.name:<20} {sale.quantity:<5} ${sale.total_amount:<9.2f}")
    
    def view_low_stock(self):
        """View low stock products."""
        products = InventoryService.get_low_stock_products()
        if not products:
            print("No low stock items.")
            return
        
        print("\n--- Low Stock Alert ---")
        print(f"{'ID':<5} {'Name':<20} {'Stock':<10}")
        print("-" * 40)
        
        for product in products:
            print(f"{product.id:<5} {product.name:<20} {product.quantity:<10}")
    
    def admin_menu(self):
        """Admin panel menu."""
        while True:
            print("\n--- Admin Panel ---")
            print("1. Add Product")
            print("2. Update Product")
            print("3. Delete Product")
            print("4. Sales Report")
            print("5. Back to Main Menu")
            
            choice = input("Enter choice: ").strip()
            
            if choice == '1':
                self.add_product()
            elif choice == '2':
                self.update_product()
            elif choice == '3':
                self.delete_product()
            elif choice == '4':
                self.sales_report()
            elif choice == '5':
                break
            else:
                print("Invalid choice.")
    
    def add_product(self):
        """Add new product."""
        try:
            name = input("Product Name: ").strip()
            price = float(input("Price: "))
            quantity = int(input("Quantity: "))
            category = input("Category (optional): ").strip() or None
            description = input("Description (optional): ").strip() or None
            
            product = InventoryService.add_product(name, price, quantity, description, category)
            print(f"Product '{product.name}' added successfully!")
            
        except ValueError:
            print("Invalid input. Please enter valid values.")
    
    def update_product(self):
        """Update existing product."""
        try:
            product_id = int(input("Product ID to update: "))
            product = InventoryService.get_product_by_id(product_id)
            
            if not product:
                print("Product not found.")
                return
            
            print(f"Current: {product.name} - ${product.price} - Stock: {product.quantity}")
            
            updates = {}
            new_price = input(f"New price (current: ${product.price}): ").strip()
            if new_price:
                updates['price'] = float(new_price)
            
            new_quantity = input(f"New quantity (current: {product.quantity}): ").strip()
            if new_quantity:
                updates['quantity'] = int(new_quantity)
            
            if updates:
                InventoryService.update_product(product_id, **updates)
                print("Product updated successfully!")
            else:
                print("No changes made.")
                
        except ValueError:
            print("Invalid input.")
    
    def delete_product(self):
        """Delete product."""
        try:
            product_id = int(input("Product ID to delete: "))
            if InventoryService.delete_product(product_id):
                print("Product deleted successfully!")
            else:
                print("Product not found.")
        except ValueError:
            print("Invalid product ID.")
    
    def sales_report(self):
        """Generate sales report."""
        try:
            days = int(input("Report period (days, default 30): ") or "30")
            report = SalesService.get_sales_report(days)
            
            print(f"\n--- Sales Report (Last {days} days) ---")
            print(f"Total Revenue: ${report['total_revenue']:.2f}")
            print(f"Total Transactions: {report['total_transactions']}")
            
        except ValueError:
            print("Invalid input.")

if __name__ == "__main__":
    cli = InventoryCLI()
    cli.run()