from flask import Blueprint, render_template, redirect, url_for, flash, request, abort
from flask_login import login_required, current_user
from app import db
from app.models import Gig
from app.forms import GigForm

bp = Blueprint('gigs', __name__, url_prefix='/gigs')


@bp.route('/')
def list_gigs():
    """List all gigs with optional search/filter."""
    search_query = request.args.get('search', '')
    filter_major = request.args.get('major', '')
    
    query = Gig.query
    
    # Apply filters
    if search_query:
        query = query.filter(
            (Gig.subject.contains(search_query)) | 
            (Gig.major.contains(search_query))
        )
    
    if filter_major:
        query = query.filter(Gig.major == filter_major)
    
    gigs = query.order_by(Gig.created_at.desc()).all()
    
    # Get unique majors for filter dropdown
    all_majors = db.session.query(Gig.major).distinct().all()
    majors = [m[0] for m in all_majors]
    
    return render_template('gigs/list.html', 
                         title='Tutoring Gigs',
                         gigs=gigs,
                         majors=majors,
                         search_query=search_query,
                         filter_major=filter_major)


@bp.route('/create', methods=['GET', 'POST'])
@login_required
def create_gig():
    """Create a new gig (students only)."""
    if not current_user.is_student():
        flash('Only students can post tutoring gigs.', 'warning')
        return redirect(url_for('gigs.list_gigs'))
    
    form = GigForm()
    if form.validate_on_submit():
        gig = Gig(
            user_id=current_user.id,
            major=form.major.data,
            subject=form.subject.data,
            available_hours=form.available_hours.data
        )
        db.session.add(gig)
        db.session.commit()
        
        flash('Your tutoring gig has been posted!', 'success')
        return redirect(url_for('gigs.list_gigs'))
    
    return render_template('gigs/create.html', title='Post Gig', form=form)


@bp.route('/<int:gig_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_gig(gig_id):
    """Edit a gig."""
    gig = Gig.query.get_or_404(gig_id)
    
    # Check authorization
    if gig.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    form = GigForm()
    if form.validate_on_submit():
        gig.major = form.major.data
        gig.subject = form.subject.data
        gig.available_hours = form.available_hours.data
        db.session.commit()
        
        flash('Your gig has been updated!', 'success')
        return redirect(url_for('gigs.list_gigs'))
    
    # Pre-populate form
    elif request.method == 'GET':
        form.major.data = gig.major
        form.subject.data = gig.subject
        form.available_hours.data = gig.available_hours
    
    return render_template('gigs/edit.html', title='Edit Gig', form=form, gig=gig)


@bp.route('/<int:gig_id>/delete', methods=['POST'])
@login_required
def delete_gig(gig_id):
    """Delete a gig."""
    gig = Gig.query.get_or_404(gig_id)
    
    # Check authorization
    if gig.user_id != current_user.id and not current_user.is_admin():
        abort(403)
    
    db.session.delete(gig)
    db.session.commit()
    
    flash('Gig has been deleted.', 'info')
    return redirect(url_for('gigs.list_gigs'))
