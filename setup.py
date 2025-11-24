"""Setup script for Inventory Management System."""
from setuptools import setup, find_packages

setup(
    name="inventory-management-system",
    version="1.0.0",
    description="Professional Inventory Management System with web and CLI interfaces",
    author="Your Name",
    author_email="your.email@example.com",
    packages=find_packages(),
    install_requires=[
        "flask>=2.3.3",
        "flask-sqlalchemy>=3.0.5",
        "flask-login>=0.6.3",
        "werkzeug>=2.3.7",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.2",
            "pytest-cov>=4.1.0",
        ]
    },
    entry_points={
        "console_scripts": [
            "inventory-cli=cli:main",
            "inventory-web=run:main",
        ]
    },
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
)