from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, TextAreaField, SelectField, FloatField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from models import User

class LoginForm(FlaskForm):
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Sign In')


class RegisterForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Email Address', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    password = PasswordField('Password', validators=[
        DataRequired(),
        Length(min=6, message="Password must be at least 6 characters long")
    ])
    confirm_password = PasswordField('Confirm Password', validators=[
        DataRequired(),
        EqualTo('password', message="Passwords must match")
    ])
    agree_terms = BooleanField('I agree to the Terms of Service & Privacy Policy', validators=[DataRequired()])
    submit = SubmitField('Create Account')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data.lower().strip()).first()
        if user:
            raise ValidationError('An account with this email address already exists.')


class ProfileForm(FlaskForm):
    name = StringField('Full Name', validators=[DataRequired(), Length(min=2, max=100)])
    phone = StringField('Phone Number', validators=[Optional(), Length(max=20)])
    headline = StringField('Professional Headline', validators=[Optional(), Length(max=180)])
    college = StringField('College / University', validators=[Optional(), Length(max=180)])
    degree = StringField('Degree & Branch', validators=[Optional(), Length(max=120)])
    graduation_year = IntegerField('Graduation Year', validators=[Optional()])
    cgpa = FloatField('CGPA / Percentage', validators=[Optional()])
    target_role = StringField('Target Role', validators=[Optional(), Length(max=100)])
    skills = TextAreaField('Key Skills (comma separated)', validators=[Optional()])
    bio = TextAreaField('Short Bio / About Me', validators=[Optional()])
    github_url = StringField('GitHub Profile URL', validators=[Optional()])
    linkedin_url = StringField('LinkedIn Profile URL', validators=[Optional()])
    portfolio_url = StringField('Portfolio Website URL', validators=[Optional()])
    submit = SubmitField('Save Profile Changes')


class ContactForm(FlaskForm):
    name = StringField('Your Name', validators=[DataRequired(), Length(min=2, max=100)])
    email = StringField('Your Email', validators=[DataRequired(), Email()])
    subject = StringField('Subject', validators=[DataRequired(), Length(min=3, max=150)])
    message = TextAreaField('Message', validators=[DataRequired(), Length(min=10, max=2000)])
    submit = SubmitField('Send Message')


class JobForm(FlaskForm):
    title = StringField('Job Title', validators=[DataRequired(), Length(max=180)])
    company_id = SelectField('Hiring Company', coerce=int, validators=[DataRequired()])
    role_category = SelectField('Category', choices=[
        ('Software Engineering', 'Software Engineering'),
        ('Frontend Development', 'Frontend Development'),
        ('Backend Development', 'Backend Development'),
        ('Full Stack Development', 'Full Stack Development'),
        ('Data Science & AI', 'Data Science & AI'),
        ('Cloud & DevOps', 'Cloud & DevOps'),
        ('QA & Automation', 'QA & Automation'),
        ('Product & Analytics', 'Product & Analytics')
    ], validators=[DataRequired()])
    job_type = SelectField('Job Type', choices=[
        ('Full-Time', 'Full-Time'),
        ('Internship', 'Internship'),
        ('Contract', 'Contract')
    ], default='Full-Time')
    location = StringField('Location', validators=[DataRequired()])
    workplace_type = SelectField('Workplace Type', choices=[
        ('Remote', 'Remote'),
        ('Hybrid', 'Hybrid'),
        ('Onsite', 'Onsite')
    ], default='Hybrid')
    experience_level = SelectField('Experience Level', choices=[
        ('Fresher (0-1 yrs)', 'Fresher (0-1 yrs)'),
        ('1-3 yrs', '1-3 yrs'),
        ('3-5 yrs', '3-5 yrs')
    ], default='Fresher (0-1 yrs)')
    salary_display = StringField('Salary Display (e.g. ₹8.0 - ₹14.0 LPA)', validators=[DataRequired()])
    min_salary = FloatField('Min Salary (LPA)', default=6.0)
    max_salary = FloatField('Max Salary (LPA)', default=12.0)
    skills_required = StringField('Skills Required (comma separated)', validators=[DataRequired()])
    openings = IntegerField('Openings Count', default=3)
    description = TextAreaField('Job Description', validators=[DataRequired()])
    requirements = TextAreaField('Requirements & Eligibility', validators=[DataRequired()])
    is_featured = BooleanField('Feature on Homepage')
    is_active = BooleanField('Active Listing', default=True)
    submit = SubmitField('Save Job Listing')
