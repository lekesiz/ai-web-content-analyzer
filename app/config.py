import os
from dotenv import load_dotenv

BASE_DIR = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))

# Load .env from project root only (dev fallback; prod uses platform env vars)
load_dotenv(os.path.join(BASE_DIR, '.env'))


def _resolve_database_uri() -> str:
    """Pick the right DB URL for the current environment.

    Priority:
      1. DATABASE_URL env var (Railway/Heroku PostgreSQL convention)
      2. Writable SQLite under SQLITE_DIR if set
      3. Default SQLite at <project>/instance/analyzer.db (dev)

    Railway sometimes emits 'postgres://' which SQLAlchemy 2.x rejects;
    we normalize it to 'postgresql://'.
    """
    url = os.getenv('DATABASE_URL')
    if url:
        if url.startswith('postgres://'):
            url = url.replace('postgres://', 'postgresql://', 1)
        return url

    # Fallback to SQLite. On Railway, the project root is read-only
    # outside /tmp and /app, but /app/instance gets shipped with the
    # build so we can still write there if the directory exists.
    db_dir = os.getenv('SQLITE_DIR') or os.path.join(BASE_DIR, 'instance')
    try:
        os.makedirs(db_dir, exist_ok=True)
    except OSError:
        # If the chosen dir is not writable (read-only FS), fall back
        # to /tmp which is writable on every PaaS we care about.
        db_dir = '/tmp'
        os.makedirs(db_dir, exist_ok=True)

    return f"sqlite:///{os.path.join(db_dir, 'analyzer.db')}"


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-secret-key')
    SQLALCHEMY_DATABASE_URI = _resolve_database_uri()
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')


class DevelopmentConfig(Config):
    DEBUG = True


class ProductionConfig(Config):
    DEBUG = False


class TestingConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'


config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'testing': TestingConfig,
}
