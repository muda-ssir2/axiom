from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from models import db, Job, Company, Application, SavedJob
from sqlalchemy import or_, and_

jobs_bp = Blueprint('jobs', __name__, url_prefix='/jobs')

@jobs_bp.route('/')
def index():
    query = Job.query.filter_by(is_active=True)

    # Search keyword
    q = request.args.get('q', '').strip()
    if q:
        query = query.join(Company).filter(
            or_(
                Job.title.ilike(f"%{q}%"),
                Company.name.ilike(f"%{q}%"),
                Job.skills_required.ilike(f"%{q}%"),
                Job.description.ilike(f"%{q}%")
            )
        )

    # Location filter
    location = request.args.get('location', '').strip()
    if location and location != 'All':
        query = query.filter(Job.location.ilike(f"%{location}%"))

    # Workplace type
    workplace = request.args.get('workplace', '').strip()
    if workplace and workplace != 'All':
        query = query.filter(Job.workplace_type == workplace)

    # Category filter
    category = request.args.get('category', '').strip()
    if category and category != 'All':
        query = query.filter(Job.role_category == category)

    # Experience level
    experience = request.args.get('experience', '').strip()
    if experience and experience != 'All':
        query = query.filter(Job.experience_level == experience)

    # Min salary
    min_sal = request.args.get('min_salary', type=float)
    if min_sal:
        query = query.filter(Job.max_salary >= min_sal)

    jobs = query.order_by(Job.is_featured.desc(), Job.created_at.desc()).all()

    # Collect unique locations & categories for filter badges
    all_categories = [
        'Software Engineering', 'Frontend Development', 'Backend Development',
        'Full Stack Development', 'Data Science & AI', 'Cloud & DevOps',
        'QA & Automation', 'Product & Analytics'
    ]
    popular_locations = ['All', 'Remote', 'Bengaluru', 'Hyderabad', 'Pune', 'Gurugram', 'Mumbai', 'Noida']

    # Get set of saved job IDs if current user is logged in
    saved_job_ids = set()
    applied_job_ids = set()
    if current_user.is_authenticated:
        saved_job_ids = {sj.job_id for sj in current_user.saved_jobs}
        applied_job_ids = {app.job_id for app in current_user.applications}

    return render_template(
        'jobs.html',
        jobs=jobs,
        all_categories=all_categories,
        popular_locations=popular_locations,
        selected_category=category,
        selected_location=location,
        selected_workplace=workplace,
        selected_experience=experience,
        search_query=q,
        saved_job_ids=saved_job_ids,
        applied_job_ids=applied_job_ids,
        total_results=len(jobs)
    )


@jobs_bp.route('/<int:job_id>')
def details(job_id):
    job = Job.query.get_or_404(job_id)
    
    # Check if current user has saved or applied
    is_saved = False
    has_applied = False
    existing_application = None

    if current_user.is_authenticated:
        is_saved = SavedJob.query.filter_by(job_id=job.id, user_id=current_user.id).first() is not None
        existing_application = Application.query.filter_by(job_id=job.id, user_id=current_user.id).first()
        has_applied = existing_application is not None

    similar_jobs = Job.query.filter(
        Job.id != job.id,
        Job.role_category == job.role_category,
        Job.is_active == True
    ).limit(3).all()

    return render_template(
        'job_details.html',
        job=job,
        is_saved=is_saved,
        has_applied=has_applied,
        existing_application=existing_application,
        similar_jobs=similar_jobs
    )


@jobs_bp.route('/<int:job_id>/apply', methods=['POST'])
@login_required
def apply(job_id):
    job = Job.query.get_or_404(job_id)

    if current_user.is_admin:
        flash("Administrators cannot submit student job applications.", "warning")
        return redirect(url_for('jobs.details', job_id=job.id))

    existing = Application.query.filter_by(job_id=job.id, user_id=current_user.id).first()
    if existing:
        flash("You have already applied for this opening. Check status on your dashboard.", "info")
        return redirect(url_for('jobs.details', job_id=job.id))

    cover_note = request.form.get('cover_note', '').strip()

    application = Application(
        job_id=job.id,
        user_id=current_user.id,
        cover_note=cover_note,
        status="Applied"
    )
    db.session.add(application)
    db.session.commit()

    flash(f"Application successfully submitted to {job.company.name} for '{job.title}'! Track status below.", "success")
    return redirect(url_for('student.applications'))


@jobs_bp.route('/<int:job_id>/save', methods=['POST'])
@login_required
def toggle_save(job_id):
    job = Job.query.get_or_404(job_id)
    existing = SavedJob.query.filter_by(job_id=job.id, user_id=current_user.id).first()

    if existing:
        db.session.delete(existing)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'saved': False, 'message': 'Job removed from saved list'})
        flash("Job removed from saved bookmarks.", "info")
    else:
        new_saved = SavedJob(job_id=job.id, user_id=current_user.id)
        db.session.add(new_saved)
        db.session.commit()
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return jsonify({'saved': True, 'message': 'Job saved to bookmarks!'})
        flash("Job saved to your bookmarks!", "success")

    return redirect(request.referrer or url_for('jobs.details', job_id=job.id))
