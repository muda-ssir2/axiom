from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

def get_utc_now():
    return datetime.now(timezone.utc)

db = SQLAlchemy()

class User(UserMixin, db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    role = db.Column(db.String(20), default='student', nullable=False)  # 'student' or 'admin'
    phone = db.Column(db.String(20), nullable=True)
    avatar_url = db.Column(db.String(255), nullable=True)
    created_at = db.Column(db.DateTime, default=get_utc_now)
    is_active_account = db.Column(db.Boolean, default=True)

    # Relationships
    profile = db.relationship('StudentProfile', backref='user', uselist=False, cascade='all, delete-orphan')
    applications = db.relationship('Application', backref='applicant', cascade='all, delete-orphan', lazy='dynamic')
    saved_jobs = db.relationship('SavedJob', backref='user', cascade='all, delete-orphan', lazy='dynamic')
    test_results = db.relationship('TestResult', backref='student', cascade='all, delete-orphan', lazy='dynamic')
    resumes = db.relationship('Resume', backref='owner', cascade='all, delete-orphan', lazy='dynamic')

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    @property
    def is_admin(self):
        return self.role == 'admin'

    def __repr__(self):
        return f"<User {self.email} ({self.role})>"


class StudentProfile(db.Model):
    __tablename__ = 'student_profiles'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=False)
    headline = db.Column(db.String(180), default="Aspiring Software Engineer")
    college = db.Column(db.String(180), default="National Institute of Technology")
    degree = db.Column(db.String(120), default="B.Tech in Computer Science & Engineering")
    graduation_year = db.Column(db.Integer, default=2026)
    cgpa = db.Column(db.Float, default=8.6)
    bio = db.Column(db.Text, nullable=True)
    skills = db.Column(db.Text, default="Python, Data Structures, SQL, React, Flask, Git")
    target_role = db.Column(db.String(100), default="Full Stack Developer")
    github_url = db.Column(db.String(200), default="https://github.com")
    linkedin_url = db.Column(db.String(200), default="https://linkedin.com")
    portfolio_url = db.Column(db.String(200), nullable=True)
    resume_filename = db.Column(db.String(255), nullable=True)
    updated_at = db.Column(db.DateTime, default=get_utc_now, onupdate=get_utc_now)

    @property
    def completion_percentage(self):
        fields = [
            self.headline, self.college, self.degree, self.graduation_year,
            self.cgpa, self.bio, self.skills, self.target_role,
            self.github_url, self.linkedin_url
        ]
        filled = sum(1 for f in fields if f)
        pct = int((filled / len(fields)) * 100)
        return min(max(pct, 20), 100)

    @property
    def skills_list(self):
        if not self.skills:
            return []
        return [s.strip() for s in self.skills.split(',') if s.strip()]


class Company(db.Model):
    __tablename__ = 'companies'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False, unique=True)
    slug = db.Column(db.String(150), nullable=False, unique=True)
    logo_initials = db.Column(db.String(6), default="AP")
    logo_bg_color = db.Column(db.String(20), default="#0ea5e9")
    website = db.Column(db.String(200), nullable=True)
    location = db.Column(db.String(100), default="Bengaluru, India")
    industry = db.Column(db.String(100), default="Fintech & SaaS")
    employee_count = db.Column(db.String(50), default="500-1,000")
    about = db.Column(db.Text, nullable=True)
    is_verified = db.Column(db.Boolean, default=True)

    jobs = db.relationship('Job', backref='company', cascade='all, delete-orphan', lazy='dynamic')


class Job(db.Model):
    __tablename__ = 'jobs'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'), nullable=False)
    role_category = db.Column(db.String(80), default="Software Engineering")  # Frontend, Backend, Full Stack, Data Science, DevOps, QA
    job_type = db.Column(db.String(50), default="Full-Time")  # Full-Time, Internship, Contract
    location = db.Column(db.String(100), default="Bengaluru, KA")
    workplace_type = db.Column(db.String(40), default="Hybrid")  # Remote, Hybrid, Onsite
    experience_level = db.Column(db.String(50), default="Fresher (0-1 yrs)")  # Fresher (0-1 yrs), 1-3 yrs, 3-5 yrs
    min_salary = db.Column(db.Float, default=6.0)  # In LPA
    max_salary = db.Column(db.Float, default=12.0) # In LPA
    salary_display = db.Column(db.String(80), default="₹8.0 - ₹14.0 LPA")
    description = db.Column(db.Text, nullable=False)
    requirements = db.Column(db.Text, nullable=False)
    skills_required = db.Column(db.String(255), default="Python, SQL, DSA, REST APIs")
    openings = db.Column(db.Integer, default=5)
    deadline = db.Column(db.DateTime, nullable=True)
    is_featured = db.Column(db.Boolean, default=False)
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    applications = db.relationship('Application', backref='job', cascade='all, delete-orphan', lazy='dynamic')
    saved_by = db.relationship('SavedJob', backref='job', cascade='all, delete-orphan', lazy='dynamic')

    @property
    def skills_list(self):
        if not self.skills_required:
            return []
        return [s.strip() for s in self.skills_required.split(',') if s.strip()]


class Application(db.Model):
    __tablename__ = 'applications'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    cover_note = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(50), default="Applied")  # Applied, Under Review, Shortlisted, Interview Scheduled, Offer Extended, Rejected
    admin_feedback = db.Column(db.Text, nullable=True)
    applied_at = db.Column(db.DateTime, default=get_utc_now)
    updated_at = db.Column(db.DateTime, default=get_utc_now, onupdate=get_utc_now)

    # Unique constraint so a user applies once per job
    __table_args__ = (db.UniqueConstraint('job_id', 'user_id', name='uq_job_user_application'),)


class SavedJob(db.Model):
    __tablename__ = 'saved_jobs'

    id = db.Column(db.Integer, primary_key=True)
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    saved_at = db.Column(db.DateTime, default=get_utc_now)

    __table_args__ = (db.UniqueConstraint('job_id', 'user_id', name='uq_job_user_save'),)


class Course(db.Model):
    __tablename__ = 'courses'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(180), nullable=False, unique=True)
    description = db.Column(db.Text, nullable=False)
    category = db.Column(db.String(60), default="Technical")  # Technical, Aptitude, System Design, Communication
    level = db.Column(db.String(40), default="Beginner to Intermediate")
    icon = db.Column(db.String(50), default="fa-code")
    badge_color = db.Column(db.String(30), default="#06b6d4")
    duration_hours = db.Column(db.Integer, default=24)
    enrolled_count = db.Column(db.Integer, default=1240)
    rating = db.Column(db.Float, default=4.8)
    is_popular = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)

    lessons = db.relationship('Lesson', backref='course', cascade='all, delete-orphan', order_by='Lesson.order_num', lazy='dynamic')


class Lesson(db.Model):
    __tablename__ = 'lessons'

    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    title = db.Column(db.String(180), nullable=False)
    order_num = db.Column(db.Integer, default=1)
    duration_mins = db.Column(db.Integer, default=20)
    content = db.Column(db.Text, nullable=False)
    code_example = db.Column(db.Text, nullable=True)
    key_takeaways = db.Column(db.Text, nullable=True)


class Test(db.Model):
    __tablename__ = 'tests'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(180), nullable=False)
    slug = db.Column(db.String(180), nullable=False, unique=True)
    category = db.Column(db.String(80), nullable=False)  # Quantitative Aptitude, Logical Reasoning, Verbal Ability, Technical Coding, Full Placement Mock
    description = db.Column(db.Text, nullable=False)
    duration_mins = db.Column(db.Integer, default=25)
    total_marks = db.Column(db.Integer, default=50)
    passing_marks = db.Column(db.Integer, default=30)
    difficulty = db.Column(db.String(30), default="Medium")
    is_active = db.Column(db.Boolean, default=True)

    questions = db.relationship('Question', backref='test', cascade='all, delete-orphan', lazy='dynamic')
    results = db.relationship('TestResult', backref='test', cascade='all, delete-orphan', lazy='dynamic')


class Question(db.Model):
    __tablename__ = 'questions'

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    question_text = db.Column(db.Text, nullable=False)
    option_a = db.Column(db.Text, nullable=False)
    option_b = db.Column(db.Text, nullable=False)
    option_c = db.Column(db.Text, nullable=False)
    option_d = db.Column(db.Text, nullable=False)
    correct_option = db.Column(db.String(5), nullable=False)  # 'A', 'B', 'C', 'D'
    explanation = db.Column(db.Text, nullable=True)
    category = db.Column(db.String(80), default="Quantitative")
    marks = db.Column(db.Integer, default=2)


class TestResult(db.Model):
    __tablename__ = 'test_results'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    score = db.Column(db.Float, default=0.0)
    total_questions = db.Column(db.Integer, default=10)
    correct_answers = db.Column(db.Integer, default=0)
    wrong_answers = db.Column(db.Integer, default=0)
    unanswered = db.Column(db.Integer, default=0)
    percentage = db.Column(db.Float, default=0.0)
    time_taken_seconds = db.Column(db.Integer, default=0)
    answers_json = db.Column(db.Text, nullable=True)  # JSON string of user choices
    passed = db.Column(db.Boolean, default=False)
    taken_at = db.Column(db.DateTime, default=get_utc_now)


class Resume(db.Model):
    __tablename__ = 'resumes'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    title = db.Column(db.String(120), default="Full Stack Resume")
    template_name = db.Column(db.String(50), default="modern_cyber")
    full_name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    phone = db.Column(db.String(30), nullable=False)
    location = db.Column(db.String(100), default="Bengaluru, India")
    github = db.Column(db.String(200), nullable=True)
    linkedin = db.Column(db.String(200), nullable=True)
    portfolio = db.Column(db.String(200), nullable=True)
    summary = db.Column(db.Text, nullable=True)
    education_json = db.Column(db.Text, nullable=True)
    experience_json = db.Column(db.Text, nullable=True)
    projects_json = db.Column(db.Text, nullable=True)
    skills_json = db.Column(db.Text, nullable=True)
    certifications_json = db.Column(db.Text, nullable=True)
    achievements_json = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, default=get_utc_now)
    updated_at = db.Column(db.DateTime, default=get_utc_now, onupdate=get_utc_now)


class Testimonial(db.Model):
    __tablename__ = 'testimonials'

    id = db.Column(db.Integer, primary_key=True)
    student_name = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(100), nullable=False)
    company_placed = db.Column(db.String(120), nullable=False)
    package_lpa = db.Column(db.String(40), default="14.5 LPA")
    quote = db.Column(db.Text, nullable=False)
    college = db.Column(db.String(150), default="NIT Trichy")
    graduation_year = db.Column(db.Integer, default=2025)
    avatar_initials = db.Column(db.String(6), default="RS")
    is_featured = db.Column(db.Boolean, default=True)


class ContactMessage(db.Model):
    __tablename__ = 'contact_messages'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    email = db.Column(db.String(150), nullable=False)
    subject = db.Column(db.String(200), nullable=False)
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=get_utc_now)
    is_resolved = db.Column(db.Boolean, default=False)
