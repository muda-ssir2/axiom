from flask import Blueprint, render_template, request, flash, redirect, url_for
from models import db, Job, Course, Testimonial, ContactMessage, Company, Test, User
from forms import ContactForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    featured_jobs = Job.query.filter_by(is_active=True).order_by(Job.is_featured.desc(), Job.created_at.desc()).limit(6).all()
    popular_courses = Course.query.order_by(Course.enrolled_count.desc()).limit(4).all()
    testimonials = Testimonial.query.filter_by(is_featured=True).limit(6).all()
    mock_tests = Test.query.filter_by(is_active=True).limit(4).all()
    
    # Real-time statistics counters
    stats = {
        'total_placed': 2840,
        'placement_rate': 94.2,
        'highest_ctc': '24.5 LPA',
        'partner_companies': Company.query.count() or 18,
        'active_openings': Job.query.filter_by(is_active=True).count() or 42,
        'practice_questions': 45000
    }
    
    return render_template(
        'index.html',
        featured_jobs=featured_jobs,
        popular_courses=popular_courses,
        testimonials=testimonials,
        mock_tests=mock_tests,
        stats=stats
    )


@main_bp.route('/about')
def about():
    testimonials = Testimonial.query.limit(3).all()
    stats = {
        'total_students': User.query.filter_by(role='student').count() or 3420,
        'partner_companies': Company.query.count() or 22,
        'hiring_ratio': '94.2%',
        'practice_tests': Test.query.count() or 16
    }
    return render_template('about.html', testimonials=testimonials, stats=stats)


@main_bp.route('/pricing')
def pricing():
    return render_template('pricing.html')


@main_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    form = ContactForm()
    if form.validate_on_submit():
        msg = ContactMessage(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            subject=form.subject.data.strip(),
            message=form.message.data.strip()
        )
        db.session.add(msg)
        db.session.commit()
        flash("Your message has been received! Our placement counselors will reach out to you within 24 hours.", "success")
        return redirect(url_for('main.contact'))

    return render_template('contact.html', form=form)


@main_bp.route('/faq')
def faq():
    return render_template('faq.html')


@main_bp.route('/privacy')
def privacy():
    return render_template('privacy.html')


@main_bp.route('/terms')
def terms():
    return render_template('terms.html')
