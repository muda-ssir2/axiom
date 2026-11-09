from flask import Blueprint, render_template, request, redirect, url_for, flash, abort, jsonify
from flask_login import login_required, current_user
from models import db, User, StudentProfile, Job, Company, Application, Test, TestResult, Course, ContactMessage, Testimonial
from forms import JobForm
from utils import admin_required
from datetime import datetime, timezone

admin_bp = Blueprint('admin', __name__, url_prefix='/admin')

@admin_bp.before_request
@login_required
def ensure_admin():
    if not current_user.is_admin:
        flash("Access denied. Platform administrative privileges required.", "danger")
        return redirect(url_for('student.dashboard'))


@admin_bp.route('/')
def dashboard():
    total_students = User.query.filter_by(role='student').count()
    total_jobs = Job.query.count()
    active_jobs = Job.query.filter_by(is_active=True).count()
    total_applications = Application.query.count()
    total_tests_taken = TestResult.query.count()
    pending_messages = ContactMessage.query.filter_by(is_resolved=False).count()

    # Recent items
    recent_applications = Application.query.order_by(Application.applied_at.desc()).limit(8).all()
    recent_students = User.query.filter_by(role='student').order_by(User.created_at.desc()).limit(6).all()
    recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).all()

    # Placement metrics
    shortlisted_count = Application.query.filter(Application.status.in_(['Shortlisted', 'Interview Scheduled', 'Offer Extended'])).count()
    offers_count = Application.query.filter_by(status='Offer Extended').count()

    stats = {
        'total_students': total_students,
        'total_jobs': total_jobs,
        'active_jobs': active_jobs,
        'total_applications': total_applications,
        'total_tests_taken': total_tests_taken,
        'shortlisted_count': shortlisted_count,
        'offers_count': offers_count,
        'pending_messages': pending_messages
    }

    return render_template(
        'admin/dashboard.html',
        stats=stats,
        recent_applications=recent_applications,
        recent_students=recent_students,
        recent_jobs=recent_jobs
    )


# ----------------- JOBS MANAGEMENT -----------------

@admin_bp.route('/jobs')
def jobs():
    all_jobs = Job.query.order_by(Job.created_at.desc()).all()
    return render_template('admin/jobs.html', jobs=all_jobs)


@admin_bp.route('/jobs/new', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    companies = Company.query.order_by(Company.name).all()
    form.company_id.choices = [(c.id, c.name) for c in companies]

    if form.validate_on_submit():
        job = Job(
            title=form.title.data.strip(),
            company_id=form.company_id.data,
            role_category=form.role_category.data,
            job_type=form.job_type.data,
            location=form.location.data.strip(),
            workplace_type=form.workplace_type.data,
            experience_level=form.experience_level.data,
            salary_display=form.salary_display.data.strip(),
            min_salary=form.min_salary.data or 6.0,
            max_salary=form.max_salary.data or 12.0,
            skills_required=form.skills_required.data.strip(),
            openings=form.openings.data or 1,
            description=form.description.data.strip(),
            requirements=form.requirements.data.strip(),
            is_featured=form.is_featured.data,
            is_active=form.is_active.data
        )
        db.session.add(job)
        db.session.commit()
        flash(f"Job opening '{job.title}' created successfully!", "success")
        return redirect(url_for('admin.jobs'))

    return render_template('admin/job_form.html', form=form, title="Create New Job Listing", is_edit=False)


@admin_bp.route('/jobs/<int:job_id>/edit', methods=['GET', 'POST'])
def edit_job(job_id):
    job = Job.query.get_or_404(job_id)
    form = JobForm(obj=job)
    companies = Company.query.order_by(Company.name).all()
    form.company_id.choices = [(c.id, c.name) for c in companies]

    if form.validate_on_submit():
        job.title = form.title.data.strip()
        job.company_id = form.company_id.data
        job.role_category = form.role_category.data
        job.job_type = form.job_type.data
        job.location = form.location.data.strip()
        job.workplace_type = form.workplace_type.data
        job.experience_level = form.experience_level.data
        job.salary_display = form.salary_display.data.strip()
        job.min_salary = form.min_salary.data
        job.max_salary = form.max_salary.data
        job.skills_required = form.skills_required.data.strip()
        job.openings = form.openings.data
        job.description = form.description.data.strip()
        job.requirements = form.requirements.data.strip()
        job.is_featured = form.is_featured.data
        job.is_active = form.is_active.data

        db.session.commit()
        flash(f"Job opening '{job.title}' updated successfully!", "success")
        return redirect(url_for('admin.jobs'))

    return render_template('admin/job_form.html', form=form, title=f"Edit: {job.title}", is_edit=True, job=job)


@admin_bp.route('/jobs/<int:job_id>/delete', methods=['POST'])
def delete_job(job_id):
    job = Job.query.get_or_404(job_id)
    title = job.title
    db.session.delete(job)
    db.session.commit()
    flash(f"Job '{title}' has been removed from platform.", "info")
    return redirect(url_for('admin.jobs'))


@admin_bp.route('/jobs/<int:job_id>/toggle-status', methods=['POST'])
def toggle_job_status(job_id):
    job = Job.query.get_or_404(job_id)
    job.is_active = not job.is_active
    db.session.commit()
    status_str = "activated" if job.is_active else "deactivated"
    flash(f"Job '{job.title}' is now {status_str}.", "success")
    return redirect(url_for('admin.jobs'))


# ----------------- APPLICATIONS MANAGEMENT -----------------

@admin_bp.route('/applications')
def applications():
    status_filter = request.args.get('status', 'All')
    query = Application.query

    if status_filter != 'All':
        query = query.filter_by(status=status_filter)

    all_apps = query.order_by(Application.applied_at.desc()).all()
    statuses = ['All', 'Applied', 'Under Review', 'Shortlisted', 'Interview Scheduled', 'Offer Extended', 'Rejected']

    return render_template('admin/applications.html', applications=all_apps, statuses=statuses, selected_status=status_filter)


@admin_bp.route('/applications/<int:app_id>/status', methods=['POST'])
def update_application_status(app_id):
    app_record = Application.query.get_or_404(app_id)
    new_status = request.form.get('status')
    admin_feedback = request.form.get('admin_feedback', '').strip()

    valid_statuses = ['Applied', 'Under Review', 'Shortlisted', 'Interview Scheduled', 'Offer Extended', 'Rejected']
    if new_status in valid_statuses:
        app_record.status = new_status
        if admin_feedback:
            app_record.admin_feedback = admin_feedback
        app_record.updated_at = datetime.now(timezone.utc)
        db.session.commit()
        flash(f"Application #{app_record.id} status updated to '{new_status}'.", "success")
    else:
        flash("Invalid application status supplied.", "danger")

    return redirect(request.referrer or url_for('admin.applications'))


# ----------------- STUDENTS MANAGEMENT -----------------

@admin_bp.route('/students')
def students():
    search = request.args.get('search', '').strip()
    query = User.query.filter_by(role='student')

    if search:
        query = query.filter(
            (User.name.ilike(f"%{search}%")) |
            (User.email.ilike(f"%{search}%"))
        )

    all_students = query.order_by(User.created_at.desc()).all()
    return render_template('admin/students.html', students=all_students, search=search)


@admin_bp.route('/students/<int:student_id>/toggle-status', methods=['POST'])
def toggle_student_status(student_id):
    user = User.query.get_or_404(student_id)
    if user.id == current_user.id:
        flash("Cannot modify your own administrator account status.", "warning")
        return redirect(url_for('admin.students'))

    user.is_active_account = not user.is_active_account
    db.session.commit()
    state = "activated" if user.is_active_account else "deactivated"
    flash(f"Account for {user.name} ({user.email}) has been {state}.", "info")
    return redirect(url_for('admin.students'))


# ----------------- MESSAGES & INQUIRIES -----------------

@admin_bp.route('/messages')
def messages():
    all_msgs = ContactMessage.query.order_by(ContactMessage.created_at.desc()).all()
    return render_template('admin/messages.html', messages=all_msgs)


@admin_bp.route('/messages/<int:msg_id>/resolve', methods=['POST'])
def resolve_message(msg_id):
    msg = ContactMessage.query.get_or_404(msg_id)
    msg.is_resolved = not msg.is_resolved
    db.session.commit()
    flash(f"Inquiry #{msg.id} status updated.", "success")
    return redirect(url_for('admin.messages'))
