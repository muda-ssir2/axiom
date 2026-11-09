import os
from flask import Flask, render_template
from flask_login import LoginManager
from flask_wtf.csrf import CSRFProtect
from config import Config
from models import db, User

csrf = CSRFProtect()

def create_app(config_class=Config):
    app = Flask(__name__)
    app.config.from_object(config_class)

    # Ensure upload folder and instance folder exist
    os.makedirs(os.path.join(app.root_path, 'instance'), exist_ok=True)
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

    # Initialize extensions
    db.init_app(app)
    csrf.init_app(app)

    login_manager = LoginManager()
    login_manager.login_view = 'auth.login'
    login_manager.login_message = "Please sign in to access your AXIOMPATH dashboard and features."
    login_manager.login_message_category = "info"
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return db.session.get(User, int(user_id))

    # Register Blueprints
    from routes.auth import auth_bp
    from routes.main import main_bp
    from routes.student import student_bp
    from routes.jobs import jobs_bp
    from routes.preparation import prep_bp
    from routes.resume import resume_bp
    from routes.admin import admin_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(student_bp)
    app.register_blueprint(jobs_bp)
    app.register_blueprint(prep_bp)
    app.register_blueprint(resume_bp)
    app.register_blueprint(admin_bp)

    csrf.exempt(resume_bp)

    # Global Template Context Processor
    @app.context_processor
    def inject_global_vars():
        return {
            'app_name': 'AXIOMPATH',
            'tagline': 'Think Beyond. Get Hired.',
            'current_year': 2026
        }

    # Custom Error Handlers
    @app.errorhandler(404)
    def page_not_found(e):
        return render_template('404.html'), 404

    @app.errorhandler(500)
    def internal_server_error(e):
        return render_template('500.html'), 500

    return app

app = create_app()

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    print("AXIOMPATH Portal server running at http://127.0.0.1:5000")
    app.run(debug=True, host='127.0.0.1', port=5000)
