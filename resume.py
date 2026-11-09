from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify, send_file
from flask_login import login_required, current_user
from models import db, Resume, StudentProfile
from utils import generate_resume_pdf
import json

resume_bp = Blueprint('resume', __name__, url_prefix='/resume-builder')

@resume_bp.route('/')
@login_required
def index():
    # Fetch existing resume if any, or prefill from profile
    resume = Resume.query.filter_by(user_id=current_user.id).order_by(Resume.updated_at.desc()).first()
    profile = current_user.profile

    # Default template data if no existing resume
    initial_data = {
        'full_name': resume.full_name if resume else current_user.name,
        'email': resume.email if resume else current_user.email,
        'phone': resume.phone if resume else (current_user.phone or '+91 98765 43210'),
        'location': resume.location if resume else 'Bengaluru, India',
        'linkedin': resume.linkedin if resume else (profile.linkedin_url if profile else 'https://linkedin.com/in/username'),
        'github': resume.github if resume else (profile.github_url if profile else 'https://github.com/username'),
        'portfolio': resume.portfolio if resume else '',
        'summary': resume.summary if resume else (profile.bio if profile and profile.bio else 'Passionate software engineer with hands-on experience in full-stack web development, Python, and scalable architecture. Proven problem-solving ability with 300+ LeetCode problems solved.'),
        'education': json.loads(resume.education_json) if resume and resume.education_json else [
            {
                'degree': profile.degree if profile else 'B.Tech in Computer Science & Engineering',
                'institution': profile.college if profile else 'National Institute of Technology',
                'year': str(profile.graduation_year) if profile else '2022 - 2026',
                'score': f"{profile.cgpa} CGPA" if profile and profile.cgpa else '8.7 CGPA'
            }
        ],
        'experience': json.loads(resume.experience_json) if resume and resume.experience_json else [
            {
                'role': 'Software Engineering Intern',
                'company': 'TechNova Solutions',
                'duration': 'May 2025 - July 2025',
                'description': 'Engineered REST APIs using Python & Flask, improved database query performance by 30%, and collaborated with DevOps team on Docker CI/CD pipelines.'
            }
        ],
        'projects': json.loads(resume.projects_json) if resume and resume.projects_json else [
            {
                'title': 'AI-Powered Placement Prep Platform',
                'tech': 'Python, Flask, SQLite, Chart.js, HTML5/CSS3',
                'description': 'Designed and developed an end-to-end recruitment preparation platform with real-time aptitude testing, dynamic resume generation, and job tracking.'
            },
            {
                'title': 'Distributed Key-Value Store',
                'tech': 'Go, gRPC, Raft Consensus, Docker',
                'description': 'Built a fault-tolerant distributed storage node with leader election and log replication handling up to 15,000 req/sec.'
            }
        ],
        'skills': json.loads(resume.skills_json) if resume and resume.skills_json else (
            [s.strip() for s in profile.skills.split(',')] if profile and profile.skills else
            ['Python', 'JavaScript', 'SQL', 'Flask', 'React', 'Data Structures & Algorithms', 'Git', 'Docker']
        ),
        'certifications': json.loads(resume.certifications_json) if resume and resume.certifications_json else [
            'AWS Certified Cloud Practitioner (2025)',
            'HackerRank Problem Solving (Advanced) 5-Star Certified'
        ],
        'achievements': json.loads(resume.achievements_json) if resume and resume.achievements_json else [
            'Secured Global Rank 142 in Codeforces Round #840',
            'Winner of Smart India Hackathon 2025 (College Internal Round)'
        ]
    }

    return render_template('resume_builder.html', resume=resume, initial_data=initial_data)


@resume_bp.route('/save', methods=['POST'])
@login_required
def save():
    data = request.get_json() if request.is_json else request.form

    full_name = data.get('full_name') or current_user.name
    email = data.get('email') or current_user.email
    phone = data.get('phone') or ''
    location = data.get('location') or 'Bengaluru, India'
    linkedin = data.get('linkedin') or ''
    github = data.get('github') or ''
    portfolio = data.get('portfolio') or ''
    summary = data.get('summary') or ''
    template_name = data.get('template_name') or 'modern_cyber'

    education_json = data.get('education_json') or '[]'
    experience_json = data.get('experience_json') or '[]'
    projects_json = data.get('projects_json') or '[]'
    skills_json = data.get('skills_json') or '[]'
    certifications_json = data.get('certifications_json') or '[]'
    achievements_json = data.get('achievements_json') or '[]'

    # Check for existing resume for this user
    resume = Resume.query.filter_by(user_id=current_user.id).first()
    if not resume:
        resume = Resume(user_id=current_user.id)
        db.session.add(resume)

    resume.full_name = full_name
    resume.email = email
    resume.phone = phone
    resume.location = location
    resume.linkedin = linkedin
    resume.github = github
    resume.portfolio = portfolio
    resume.summary = summary
    resume.template_name = template_name
    resume.education_json = education_json if isinstance(education_json, str) else json.dumps(education_json)
    resume.experience_json = experience_json if isinstance(experience_json, str) else json.dumps(experience_json)
    resume.projects_json = projects_json if isinstance(projects_json, str) else json.dumps(projects_json)
    resume.skills_json = skills_json if isinstance(skills_json, str) else json.dumps(skills_json)
    resume.certifications_json = certifications_json if isinstance(certifications_json, str) else json.dumps(certifications_json)
    resume.achievements_json = achievements_json if isinstance(achievements_json, str) else json.dumps(achievements_json)

    db.session.commit()

    if request.is_json or request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return jsonify({'status': 'success', 'resume_id': resume.id, 'message': 'Resume saved successfully!'})

    flash("Resume changes saved successfully!", "success")
    return redirect(url_for('resume.index'))


@resume_bp.route('/download/<int:resume_id>')
@login_required
def download_pdf(resume_id):
    resume = Resume.query.get_or_404(resume_id)
    if resume.user_id != current_user.id and not current_user.is_admin:
        flash("Unauthorized access to this resume.", "danger")
        return redirect(url_for('resume.index'))

    pdf_buffer = generate_resume_pdf(resume)
    safe_filename = f"{resume.full_name.replace(' ', '_')}_Resume_AXIOMPATH.pdf"

    return send_file(
        pdf_buffer,
        as_attachment=True,
        download_name=safe_filename,
        mimetype='application/pdf'
    )
