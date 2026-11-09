import os

BASE_DIR = os.path.abspath(os.path.dirname(__file__))

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'axiompath-hyperdrive-key-2026-production-ready'
    SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL') or \
        f"sqlite:///{os.path.join(BASE_DIR, 'instance', 'axiompath.db')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = None  # Prevent CSRF token expiry during long test sessions
    UPLOAD_FOLDER = os.path.join(BASE_DIR, 'static', 'uploads')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max upload
