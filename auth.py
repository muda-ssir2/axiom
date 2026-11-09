from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_user, logout_user, login_required, current_user
from models import db, User, StudentProfile
from forms import LoginForm, RegisterForm

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('student.dashboard'))

    form = RegisterForm()
    if form.validate_on_submit():
        user = User(
            name=form.name.data.strip(),
            email=form.email.data.lower().strip(),
            phone=form.phone.data.strip() if form.phone.data else None,
            role='student'
        )
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.flush()  # To get user.id

        # Create basic student profile
        profile = StudentProfile(
            user_id=user.id,
            headline="Aspiring Tech Professional | Placement Candidate",
            college="Engineering & Tech Institute",
            degree="B.Tech Computer Science / IT",
            graduation_year=2026,
            skills="Python, SQL, Data Structures, Problem Solving"
        )
        db.session.add(profile)
        db.session.commit()

        login_user(user)
        flash(f"Welcome aboard, {user.name}! Your AXIOMPATH journey begins now.", "success")
        return redirect(url_for('student.dashboard'))

    return render_template('register.html', form=form)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.is_admin:
            return redirect(url_for('admin.dashboard'))
        return redirect(url_for('student.dashboard'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data.lower().strip()).first()
        if user and user.check_password(form.password.data):
            if not user.is_active_account:
                flash("Your account has been deactivated. Please contact support.", "danger")
                return render_template('login.html', form=form)

            login_user(user, remember=form.remember.data)
            flash(f"Welcome back, {user.name}!", "success")

            next_page = request.args.get('next')
            if next_page and next_page.startswith('/'):
                return redirect(next_page)

            if user.is_admin:
                return redirect(url_for('admin.dashboard'))
            return redirect(url_for('student.dashboard'))
        else:
            flash("Invalid email or password. Please verify your credentials.", "danger")

    return render_template('login.html', form=form)


@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash("You have been signed out safely. Come back anytime!", "info")
    return redirect(url_for('main.index'))
