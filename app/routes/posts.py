from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Post
from app.forms import PostForm

bp = Blueprint('posts', __name__, url_prefix='/posts')


@bp.route('/')
def list_posts():
    """List all blog posts."""
    posts = Post.query.order_by(Post.created_at.desc()).all()
    return render_template('posts/list.html', title='Blog Posts', posts=posts)


@bp.route('/<int:post_id>')
def view_post(post_id):
    """View a single post."""
    post = Post.query.get_or_404(post_id)
    return render_template('posts/view.html', title=post.title, post=post)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_post():
    """Create a new blog post."""
    form = PostForm()
    if form.validate_on_submit():
        post = Post(
            user_id=current_user.id,
            title=form.title.data,
            content=form.content.data
        )
        db.session.add(post)
        db.session.commit()
        
        flash('Your post has been published!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    
    return render_template('posts/create.html', title='Create Post', form=form)


@bp.route('/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    """Edit a blog post."""
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
    if post.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        
        flash('Your post has been updated!', 'success')
        return redirect(url_for('posts.view_post', post_id=post.id))
    
    # Pre-populate form
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    
    return render_template('posts/edit.html', title='Edit Post', form=form, post=post)


@bp.route('/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    """Delete a blog post."""
    post = Post.query.get_or_404(post_id)
    
    # Check authorization
    if post.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    db.session.delete(post)
    db.session.commit()
    
    flash('Post has been deleted.', 'info')
    return redirect(url_for('posts.list_posts'))
