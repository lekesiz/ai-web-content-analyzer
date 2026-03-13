import os
from flask import Flask, send_from_directory
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

# Path to React build output
REACT_BUILD_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'react')


def create_app(config_name='development'):
    app = Flask(__name__, static_folder='static')

    from app.config import config
    app.config.from_object(config[config_name])

    db.init_app(app)

    # Register API blueprints
    from app.routes.analysis import analysis_bp
    from app.routes.history import history_bp

    app.register_blueprint(analysis_bp, url_prefix='/api')
    app.register_blueprint(history_bp)

    # Serve React app - static assets from build
    @app.route('/assets/<path:filename>')
    def react_assets(filename):
        return send_from_directory(os.path.join(REACT_BUILD_DIR, 'assets'), filename)

    # Catch-all route: serve React index.html for client-side routing
    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def serve_react(path):
        # Don't intercept API routes or existing static files
        if path.startswith('api/'):
            return app.send_static_file(path)

        # Serve React's index.html for all frontend routes
        react_index = os.path.join(REACT_BUILD_DIR, 'index.html')
        if os.path.exists(react_index):
            return send_from_directory(REACT_BUILD_DIR, 'index.html')

        # Fallback: if React not built yet, show a message
        return '<h1>Frontend not built. Run: cd frontend && npm run build</h1>', 404

    return app
