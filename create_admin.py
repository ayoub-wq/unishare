#!/usr/bin/env python3
"""
Script to create an admin user for UniShare.
Run this script after deploying the application to create the first admin account.

Usage:
    Interactive mode:
        python create_admin.py
    
    Non-interactive mode (for deployment):
        ADMIN_USERNAME=admin ADMIN_EMAIL=admin@example.com ADMIN_PASSWORD=password python create_admin.py
"""

import os
import sys

# Add the parent directory to the path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app, db
from app.models import User
from getpass import getpass


def create_admin_interactive():
    """Create an admin user interactively."""
    print("=== UniShare Admin Account Creation ===\n")
    
    # Get admin details
    username = input("Enter admin username: ").strip()
    if not username:
        print("Username cannot be empty!")
        return None, None, None
    
    email = input("Enter admin email: ").strip()
    if not email:
        print("Email cannot be empty!")
        return None, None, None
    
    password = getpass("Enter admin password (min 6 characters): ")
    if len(password) < 6:
        print("Password must be at least 6 characters long!")
        return None, None, None
    
    confirm_password = getpass("Confirm password: ")
    if password != confirm_password:
        print("Passwords do not match!")
        return None, None, None
    
    return username, email, password


def create_admin_from_env():
    """Create an admin user from environment variables."""
    username = os.environ.get('ADMIN_USERNAME')
    email = os.environ.get('ADMIN_EMAIL')
    password = os.environ.get('ADMIN_PASSWORD')
    
    if not all([username, email, password]):
        return None, None, None
    
    print(f"Creating admin from environment variables: {username}")
    return username, email, password


def create_admin():
    """Create an admin user."""
    app = create_app(os.environ.get('FLASK_ENV', 'development'))
    
    with app.app_context():
        # Check if any admin already exists
        existing_admin = User.query.filter_by(role='admin').first()
        if existing_admin:
            print(f"Admin account already exists: {existing_admin.username}")
            return
        
        # Try to get credentials from environment variables first (for deployment)
        username, email, password = create_admin_from_env()
        
        # If not in environment, use interactive mode
        if not all([username, email, password]):
            username, email, password = create_admin_interactive()
        
        # If still no credentials, exit
        if not all([username, email, password]):
            print("Failed to get admin credentials!")
            return
        
        # Check if username exists
        if User.query.filter_by(username=username).first():
            print(f"Error: Username '{username}' already exists!")
            return
        
        # Check if email exists
        if User.query.filter_by(email=email).first():
            print(f"Error: Email '{email}' already exists!")
            return
        
        # Create admin user
        admin = User(
            username=username,
            email=email,
            role='admin'
        )
        admin.set_password(password)
        
        try:
            db.session.add(admin)
            db.session.commit()
            print(f"\n✓ Admin account '{username}' created successfully!")
            print(f"  Email: {email}")
            print(f"  Role: admin")
        except Exception as e:
            db.session.rollback()
            print(f"\n✗ Error creating admin account: {e}")


if __name__ == '__main__':
    create_admin()
