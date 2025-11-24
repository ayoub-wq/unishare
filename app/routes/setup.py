from flask import Blueprint, render_template, redirect, url_for, flash, request
from app import db
from app.models import User

bp = Blueprint('setup', __name__, url_prefix='/setup')


@bp.route('/create-first-admin', methods=['GET', 'POST'])
def create_first_admin():
    """One-time setup route to create the first admin account."""
    # Check if any admin already exists
    if User.query.filter_by(role='admin').first():
        flash('Admin account already exists!', 'warning')
        return redirect(url_for('index'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        email = request.form.get('email')
        password = request.form.get('password')
        
        # Create admin
        admin = User(
            username=username,
            email=email,
            role='admin'
        )
        admin.set_password(password)
        
        db.session.add(admin)
        db.session.commit()
        
        flash(f'Admin account {username} created successfully! You can now login.', 'success')
        return redirect(url_for('auth.login'))
    
    return render_template('setup/create_admin.html', title='Setup Admin Account')
