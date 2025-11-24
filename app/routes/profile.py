import os
from werkzeug.utils import secure_filename
from PIL import Image
from flask import Blueprint, render_template, redirect, url_for, flash, request, current_app
from flask_login import login_required, current_user
from app import db
from app.models import User, Gig, Post, Course
from app.forms import ProfileEditForm, ChangePasswordForm

bp = Blueprint('profile', __name__, url_prefix='/profile')


def save_profile_picture(form_picture):
    """Save and resize profile picture."""
    # Generate unique filename
    filename = secure_filename(form_picture.filename)
    random_hex = os.urandom(8).hex()
    _, f_ext = os.path.splitext(filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], picture_fn)
    
    # Resize image to 300x300
    output_size = (300, 300)
    img = Image.open(form_picture)
    img.thumbnail(output_size)
    img.save(picture_path)
    
    return picture_fn


@bp.route('/<string:username>')
def view_profile(username):
    """View a user's profile."""
    user = User.query.filter_by(username=username).first_or_404()
    
    # Get user's content
    gigs = Gig.query.filter_by(user_id=user.id).order_by(Gig.created_at.desc()).all()
    posts = Post.query.filter_by(user_id=user.id).order_by(Post.created_at.desc()).all()
    courses = Course.query.filter_by(teacher_id=user.id).order_by(Course.created_at.desc()).all()
    
    return render_template('profile/view.html',
                         title=f'{user.username}\'s Profile',
                         user=user,
                         gigs=gigs,
                         posts=posts,
                         courses=courses)


@bp.route('/edit', methods=['GET', 'POST'])
@login_required
def edit_profile():
    """Edit current user's profile."""
    form = ProfileEditForm(current_user.username, current_user.email)
    
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.bio = form.bio.data
        
        # Update major for students
        if current_user.is_student():
            current_user.major = form.major.data
        
        # Handle profile picture upload
        if form.profile_picture.data:
            # Delete old picture if exists
            if current_user.profile_picture:
                old_picture_path = os.path.join(current_app.config['UPLOAD_FOLDER'], 
                                              current_user.profile_picture)
                if os.path.exists(old_picture_path):
                    os.remove(old_picture_path)
            
            picture_file = save_profile_picture(form.profile_picture.data)
            current_user.profile_picture = picture_file
        
        db.session.commit()
        flash('Your profile has been updated!', 'success')
        return redirect(url_for('profile.view_profile', username=current_user.username))
    
    # Pre-populate form
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.bio.data = current_user.bio
        form.major.data = current_user.major
    
    return render_template('profile/edit.html', title='Edit Profile', form=form)


@bp.route('/change-password', methods=['GET', 'POST'])
@login_required
def change_password():
    """Change user password."""
    form = ChangePasswordForm()
    
    if form.validate_on_submit():
        if not current_user.check_password(form.current_password.data):
            flash('Current password is incorrect.', 'danger')
            return redirect(url_for('profile.change_password'))
        
        current_user.set_password(form.new_password.data)
        db.session.commit()
        
        flash('Your password has been changed!', 'success')
        return redirect(url_for('profile.view_profile', username=current_user.username))
    
    return render_template('profile/change_password.html', title='Change Password', form=form)
