from flask import Flask
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app(config_name='development'):
    app = Flask(__name__)

    from app.config import config
    app.config.from_object(config[config_name])

    db.init_app(app)

    from app.routes.main import main_bp
    from app.routes.analysis import analysis_bp
    from app.routes.history import history_bp

    app.register_blueprint(main_bp)
    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(history_bp)

    return app
