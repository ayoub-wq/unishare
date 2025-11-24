from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Course
from app.forms import CourseForm
from app.decorators import teacher_or_admin_required

bp = Blueprint('courses', __name__, url_prefix='/courses')


@bp.route('/')
def list_courses():
    """List all courses."""
    courses = Course.query.order_by(Course.created_at.desc()).all()
    return render_template('courses/list.html', title='Courses', courses=courses)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
@teacher_or_admin_required
def create_course():
    """Create a new course (teachers and admins only)."""
    form = CourseForm()
    if form.validate_on_submit():
        course = Course(
            teacher_id=current_user.id,
            title=form.title.data,
            description=form.description.data,
            link=form.link.data
        )
        db.session.add(course)
        db.session.commit()
        
        flash('Course has been added!', 'success')
        return redirect(url_for('courses.list_courses'))
    
    return render_template('courses/create.html', title='Add Course', form=form)


@bp.route('/<int:course_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_course(course_id):
    """Edit a course."""
    course = Course.query.get_or_404(course_id)
    
    # Check authorization
    if course.teacher_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    form = CourseForm()
    if form.validate_on_submit():
        course.title = form.title.data
        course.description = form.description.data
        course.link = form.link.data
        db.session.commit()
        
        flash('Course has been updated!', 'success')
        return redirect(url_for('courses.list_courses'))
    
    # Pre-populate form
    elif request.method == 'GET':
        form.title.data = course.title
        form.description.data = course.description
        form.link.data = course.link
    
    return render_template('courses/edit.html', title='Edit Course', form=form, course=course)


@bp.route('/<int:course_id>/delete', methods=['POST'])
@login_required
def delete_course(course_id):
    """Delete a course."""
    course = Course.query.get_or_404(course_id)
    
    # Check authorization
    if course.teacher_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    db.session.delete(course)
    db.session.commit()
    
    flash('Course has been deleted.', 'info')
    return redirect(url_for('courses.list_courses'))
