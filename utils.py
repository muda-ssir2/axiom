from functools import wraps
from flask import abort, flash, redirect, url_for, send_file
from flask_login import current_user
import io
import json
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib import colors

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin:
            flash("Access restricted to platform administrators only.", "danger")
            return redirect(url_for('auth.login'))
        return f(*args, **kwargs)
    return decorated_function


def generate_resume_pdf(resume):
    """Generates a clean PDF document from Resume model instance using ReportLab."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer,
        pagesize=letter,
        rightMargin=40,
        leftMargin=40,
        topMargin=36,
        bottomMargin=36
    )

    styles = getSampleStyleSheet()

    # Custom styles
    primary_color = colors.HexColor('#0284c7')
    dark_color = colors.HexColor('#0f172a')
    gray_color = colors.HexColor('#475569')

    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=24,
        textColor=dark_color,
        spaceAfter=4
    )

    contact_style = ParagraphStyle(
        'DocContact',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9,
        leading=12,
        textColor=gray_color,
        spaceAfter=12
    )

    section_heading = ParagraphStyle(
        'SectionHeading',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=primary_color,
        spaceBefore=10,
        spaceAfter=4
    )

    body_style = ParagraphStyle(
        'BodyDark',
        parent=styles['Normal'],
        fontName='Helvetica',
        fontSize=9.5,
        leading=13.5,
        textColor=colors.HexColor('#1e293b')
    )

    subhead_style = ParagraphStyle(
        'Subhead',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=10,
        leading=14,
        textColor=dark_color
    )

    story = []

    # Name and Header
    story.append(Paragraph(resume.full_name or "Student Name", title_style))
    contact_parts = []
    if resume.email: contact_parts.append(resume.email)
    if resume.phone: contact_parts.append(resume.phone)
    if resume.location: contact_parts.append(resume.location)
    if resume.linkedin: contact_parts.append(f"LinkedIn: {resume.linkedin}")
    if resume.github: contact_parts.append(f"GitHub: {resume.github}")

    story.append(Paragraph(" | ".join(contact_parts), contact_style))
    story.append(HRFlowable(width="100%", thickness=1.5, color=primary_color, spaceBefore=0, spaceAfter=8))

    # Summary
    if resume.summary:
        story.append(Paragraph("PROFESSIONAL SUMMARY", section_heading))
        story.append(Paragraph(resume.summary, body_style))
        story.append(Spacer(1, 8))

    # Technical Skills
    skills_data = []
    try:
        skills_data = json.loads(resume.skills_json) if resume.skills_json else []
    except Exception:
        skills_data = [resume.skills_json] if resume.skills_json else []

    if skills_data:
        story.append(Paragraph("TECHNICAL SKILLS", section_heading))
        if isinstance(skills_data, list):
            skills_str = ", ".join(str(s) for s in skills_data)
        else:
            skills_str = str(skills_data)
        story.append(Paragraph(skills_str, body_style))
        story.append(Spacer(1, 8))

    # Education
    education_data = []
    try:
        education_data = json.loads(resume.education_json) if resume.education_json else []
    except Exception:
        education_data = []

    if education_data:
        story.append(Paragraph("EDUCATION", section_heading))
        for edu in education_data:
            deg = edu.get('degree', 'Degree')
            inst = edu.get('institution', 'Institution')
            yr = edu.get('year', '')
            score = edu.get('score', '')
            details = f"<b>{deg}</b> - {inst}"
            if yr or score:
                details += f" ({yr}{' | CGPA: ' + str(score) if score else ''})"
            story.append(Paragraph(details, subhead_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # Projects
    projects_data = []
    try:
        projects_data = json.loads(resume.projects_json) if resume.projects_json else []
    except Exception:
        projects_data = []

    if projects_data:
        story.append(Paragraph("KEY PROJECTS", section_heading))
        for proj in projects_data:
            title = proj.get('title', 'Project')
            tech = proj.get('tech', '')
            desc = proj.get('description', '')
            p_head = f"<b>{title}</b>" + (f" | <i>{tech}</i>" if tech else "")
            story.append(Paragraph(p_head, subhead_style))
            if desc:
                story.append(Paragraph(f"• {desc}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # Experience / Internships
    exp_data = []
    try:
        exp_data = json.loads(resume.experience_json) if resume.experience_json else []
    except Exception:
        exp_data = []

    if exp_data:
        story.append(Paragraph("EXPERIENCE & INTERNSHIPS", section_heading))
        for exp in exp_data:
            role = exp.get('role', 'Intern')
            comp = exp.get('company', 'Company')
            duration = exp.get('duration', '')
            desc = exp.get('description', '')
            e_head = f"<b>{role}</b> - {comp}" + (f" ({duration})" if duration else "")
            story.append(Paragraph(e_head, subhead_style))
            if desc:
                story.append(Paragraph(f"• {desc}", body_style))
            story.append(Spacer(1, 4))
        story.append(Spacer(1, 6))

    # Certifications & Achievements
    certs_data = []
    try:
        certs_data = json.loads(resume.certifications_json) if resume.certifications_json else []
    except Exception:
        certs_data = []

    if certs_data:
        story.append(Paragraph("CERTIFICATIONS & ACHIEVEMENTS", section_heading))
        for cert in certs_data:
            c_text = cert if isinstance(cert, str) else cert.get('title', '')
            if c_text:
                story.append(Paragraph(f"• {c_text}", body_style))
        story.append(Spacer(1, 4))

    doc.build(story)
    buffer.seek(0)
    return buffer
