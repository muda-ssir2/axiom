from flask import Blueprint, render_template, redirect, url_for, flash, request, jsonify
from flask_login import login_required, current_user
from models import db, User, StudentProfile, Application, SavedJob, TestResult, Test, Course
from forms import ProfileForm
import json

student_bp = Blueprint('student', __name__, url_prefix='/student')

@student_bp.route('/dashboard')
@login_required
def dashboard():
    profile = current_user.profile
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

    # Recent applications
    applications = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).limit(5).all()
    
    # Saved jobs
    saved_jobs = SavedJob.query.filter_by(user_id=current_user.id).order_by(SavedJob.saved_at.desc()).limit(4).all()
    
    # Test results & performance
    recent_tests = TestResult.query.filter_by(user_id=current_user.id).order_by(TestResult.taken_at.desc()).limit(5).all()
    all_tests = TestResult.query.filter_by(user_id=current_user.id).all()
    
    # Calculate performance metrics
    total_tests_taken = len(all_tests)
    avg_score = round(sum(t.percentage for t in all_tests) / total_tests_taken, 1) if total_tests_taken > 0 else 0
    
    # Recommended courses & mock tests
    upcoming_tests = Test.query.filter_by(is_active=True).limit(3).all()
    recommended_courses = Course.query.order_by(Course.rating.desc()).limit(3).all()

    # Performance radar data
    categories = ['Quantitative', 'Logical', 'Verbal', 'Technical', 'HR Mock']
    category_scores = {}
    for cat in categories:
        cat_results = [t for t in all_tests if t.test and cat.lower() in t.test.category.lower()]
        if cat_results:
            category_scores[cat] = round(sum(r.percentage for r in cat_results) / len(cat_results), 1)
        else:
            # Default progressive score for fresh dashboard
            category_scores[cat] = 72.0 if cat in ['Quantitative', 'Technical'] else 65.0

    return render_template(
        'dashboard.html',
        profile=profile,
        applications=applications,
        saved_jobs=saved_jobs,
        recent_tests=recent_tests,
        total_tests_taken=total_tests_taken,
        avg_score=avg_score,
        upcoming_tests=upcoming_tests,
        recommended_courses=recommended_courses,
        radar_labels=list(category_scores.keys()),
        radar_values=list(category_scores.values())
    )


@student_bp.route('/profile', methods=['GET', 'POST'])
@login_required
def profile():
    profile = current_user.profile
    if not profile:
        profile = StudentProfile(user_id=current_user.id)
        db.session.add(profile)
        db.session.commit()

    form = ProfileForm(obj=profile)
    # Pre-populate user fields
    if request.method == 'GET':
        form.name.data = current_user.name
        form.phone.data = current_user.phone

    if form.validate_on_submit():
        current_user.name = form.name.data.strip()
        current_user.phone = form.phone.data.strip() if form.phone.data else None
        
        profile.headline = form.headline.data.strip() if form.headline.data else None
        profile.college = form.college.data.strip() if form.college.data else None
        profile.degree = form.degree.data.strip() if form.degree.data else None
        profile.graduation_year = form.graduation_year.data
        profile.cgpa = form.cgpa.data
        profile.target_role = form.target_role.data.strip() if form.target_role.data else None
        profile.skills = form.skills.data.strip() if form.skills.data else None
        profile.bio = form.bio.data.strip() if form.bio.data else None
        profile.github_url = form.github_url.data.strip() if form.github_url.data else None
        profile.linkedin_url = form.linkedin_url.data.strip() if form.linkedin_url.data else None
        profile.portfolio_url = form.portfolio_url.data.strip() if form.portfolio_url.data else None

        db.session.commit()
        flash("Profile updated successfully! Recruiters love a complete profile.", "success")
        return redirect(url_for('student.profile'))

    return render_template('profile.html', form=form, profile=profile)


@student_bp.route('/saved-jobs')
@login_required
def saved_jobs():
    saved = SavedJob.query.filter_by(user_id=current_user.id).order_by(SavedJob.saved_at.desc()).all()
    return render_template('saved_jobs.html', saved_jobs=saved)


@student_bp.route('/applications')
@login_required
def applications():
    apps = Application.query.filter_by(user_id=current_user.id).order_by(Application.applied_at.desc()).all()
    return render_template('applications.html', applications=apps)


@student_bp.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    if request.method == 'POST':
        curr_pwd = request.form.get('current_password')
        new_pwd = request.form.get('new_password')
        confirm_pwd = request.form.get('confirm_password')

        if not current_user.check_password(curr_pwd):
            flash("Incorrect current password.", "danger")
        elif len(new_pwd) < 6:
            flash("New password must be at least 6 characters long.", "danger")
        elif new_pwd != confirm_pwd:
            flash("New passwords do not match.", "danger")
        else:
            current_user.set_password(new_pwd)
            db.session.commit()
            flash("Password updated successfully!", "success")
            return redirect(url_for('student.settings'))

    return render_template('settings.html')
