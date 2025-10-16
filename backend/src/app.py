#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


import sys
from flask import Flask, send_from_directory
from config import Config
from extensions import db
from src.api.trips import trips_bp


def create_app(config_class=Config):
    app = Flask(__name__, static_folder='../frontend', static_url_path='')
    app.config.from_object(config_class)

    # Initialize extensions
    db.init_app(app)

    # Register blueprints
    app.register_blueprint(trips_bp, url_prefix='/api/trips')

    # Create tables if they don't exist
    with app.app_context():
        try:
            db.create_all()
        except Exception as e:
            print(f"Database initialization error: {e}")

    # Serve frontend files
    @app.route('/')
    def index():
        return send_from_directory('../frontend', 'index.html')
    
    @app.route('/<path:path>')
    def serve_static(path):
        # Serve static files (JS, CSS, images, etc.)
        if os.path.exists(os.path.join('../frontend', path)):
            return send_from_directory('../frontend', path)
        # If file doesn't exist, return index.html (for SPA routing)
        return send_from_directory('../frontend', 'index.html')

    @app.route('/api/health')
    def health():
        return {"status": "healthy"}

    # Error handlers
    @app.errorhandler(Exception)
    def handle_exception(e):
        app.logger.error(f"Unhandled exception: {str(e)}", exc_info=True)
        return {"error": str(e), "type": type(e).__name__}, 500

    return app


if __name__ == '__main__':
    app = create_app()
    print(f"Starting server on http://{Config.HOST}:{Config.PORT}")
    print("Frontend and API available at the same origin - no CORS needed!")
    app.run(
        host=Config.HOST,
        port=Config.PORT,
        debug=Config.DEBUG
    )