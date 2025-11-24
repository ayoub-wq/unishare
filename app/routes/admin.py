from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required
from app import db
from app.models import User, Gig, Post, Course
from app.forms import AdminCreateUserForm
from app.decorators import admin_required

bp = Blueprint('admin', __name__, url_prefix='/admin')


@bp.route('/dashboard')
@login_required
@admin_required
def dashboard():
    """Admin dashboard with statistics."""
    total_users = User.query.count()
    total_gigs = Gig.query.count()
    total_posts = Post.query.count()
    total_courses = Course.query.count()
    
    # Recent activity
    recent_users = User.query.order_by(User.created_at.desc()).limit(5).all()
    recent_gigs = Gig.query.order_by(Gig.created_at.desc()).limit(5).all()
    recent_posts = Post.query.order_by(Post.created_at.desc()).limit(5).all()
    recent_courses = Course.query.order_by(Course.created_at.desc()).limit(5).all()
    
    return render_template('admin/dashboard.html',
                         title='Admin Dashboard',
                         total_users=total_users,
                         total_gigs=total_gigs,
                         total_posts=total_posts,
                         total_courses=total_courses,
                         recent_users=recent_users,
                         recent_gigs=recent_gigs,
                         recent_posts=recent_posts,
                         recent_courses=recent_courses)


@bp.route('/users')
@login_required
@admin_required
def manage_users():
    """View and manage all users."""
    search = request.args.get('search', '')
    
    if search:
        users = User.query.filter(
            (User.username.contains(search)) | 
            (User.email.contains(search))
        ).all()
    else:
        users = User.query.order_by(User.created_at.desc()).all()
    
    return render_template('admin/users.html',
                         title='Manage Users',
                         users=users,
                         search=search)


@bp.route('/users/create', methods=['GET', 'POST'])
@login_required
@admin_required
def create_user():
    """Create a new user account."""
    form = AdminCreateUserForm()
    
    if form.validate_on_submit():
        user = User(
            username=form.username.data,
            email=form.email.data,
            role=form.role.data
        )
        user.set_password(form.password.data)
        
        if form.role.data == 'student' and form.major.data:
            user.major = form.major.data
        
        db.session.add(user)
        db.session.commit()
        
        flash(f'User {user.username} has been created!', 'success')
        return redirect(url_for('admin.manage_users'))
    
    return render_template('admin/create_user.html',
                         title='Create User',
                         form=form)


@bp.route('/users/<int:user_id>/delete', methods=['POST'])
@login_required
@admin_required
def delete_user(user_id):
    """Delete a user account."""
    user = User.query.get_or_404(user_id)
    
    # Prevent deleting own account
    from flask_login import current_user
    if user.id == current_user.id:
        flash('You cannot delete your own account!', 'danger')
        return redirect(url_for('admin.manage_users'))
    
    username = user.username
    db.session.delete(user)
    db.session.commit()
    
    flash(f'User {username} has been deleted.', 'info')
    return redirect(url_for('admin.manage_users'))


@bp.route('/content')
@login_required
@admin_required
def manage_content():
    """View and manage all content (gigs, posts, courses)."""
    gigs = Gig.query.order_by(Gig.created_at.desc()).all()
    posts = Post.query.order_by(Post.created_at.desc()).all()
    courses = Course.query.order_by(Course.created_at.desc()).all()
    
    return render_template('admin/content.html',
                         title='Manage Content',
                         gigs=gigs,
                         posts=posts,
                         courses=courses)
