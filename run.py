#!/usr/bin/env python3
"""Entry point for the Inventory Management System."""
import sys
from app import create_app

def main():
    """Main entry point."""
    if len(sys.argv) > 1 and sys.argv[1] == 'cli':
        # Run CLI version
        from cli import InventoryCLI
        cli = InventoryCLI()
        cli.run()
    else:
        # Run web version
        app = create_app()
        print("Starting Inventory Management System...")
        print("Web interface: http://localhost:5000")
        print("Login with: admin / admin123")
        app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main()