#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
flask db upgrade

# Create admin user if needed (only runs if no admin exists)
python create_admin.py
