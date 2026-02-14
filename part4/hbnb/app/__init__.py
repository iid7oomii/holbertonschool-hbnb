from flask import Flask, send_from_directory, redirect
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from hbnb.app.extensions import bcrypt, jwt
from flask_cors import CORS
import os

db = SQLAlchemy()


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_class: Configuration class to use (default: DevelopmentConfig)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__, static_folder=None)
    app.config.from_object(config_class)
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    # Enable CORS for all origins
    CORS(app, resources={r"/*": {"origins": "*"}})
    
    # Get web_client absolute path
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    web_client_path = os.path.join(base_dir, 'web_client')
    print(f"📂 Web client path: {web_client_path}")
    print(f"📂 Exists: {os.path.exists(web_client_path)}")
    
    # Serve frontend files BEFORE API setup
    @app.route('/', endpoint='home_page')
    def home():
        try:
            return send_from_directory(web_client_path, 'index.html')
        except Exception as e:
            return f"Error loading index.html: {e}", 500
    
    @app.route('/index.html', endpoint='index_html_page')
    def index_page():
        return send_from_directory(web_client_path, 'index.html')
    
    @app.route('/login.html', endpoint='login_html_page')
    def login_page():
        return send_from_directory(web_client_path, 'login.html')
    
    @app.route('/register.html', endpoint='register_html_page')
    def register_page():
        return send_from_directory(web_client_path, 'register.html')
    
    @app.route('/place.html', endpoint='place_html_page')
    def place_page():
        return send_from_directory(web_client_path, 'place.html')
    
    @app.route('/add_review.html', endpoint='add_review_html_page')
    def add_review_page():
        return send_from_directory(web_client_path, 'add_review.html')
    
    @app.route('/add_place.html', endpoint='add_place_html_page')
    def add_place_page():
        return send_from_directory(web_client_path, 'add_place.html')
    
    @app.route('/admin.html', endpoint='admin_html_page')
    def admin_page():
        return send_from_directory(web_client_path, 'admin.html')
    
    @app.route('/css/<path:filename>', endpoint='css_files')
    def serve_css(filename):
        return send_from_directory(os.path.join(web_client_path, 'css'), filename)
    
    @app.route('/scripts/<path:filename>', endpoint='script_files')
    def serve_scripts(filename):
        return send_from_directory(os.path.join(web_client_path, 'scripts'), filename)
    
    @app.route('/images/<path:filename>', endpoint='image_files')
    def serve_images(filename):
        return send_from_directory(os.path.join(web_client_path, 'images'), filename)
    
    # API setup - disable doc on root to avoid conflicts
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/docs",  # Move docs away from root
    )

    # Import and register namespaces
    from hbnb.app.api.v1.users import api as users_ns
    from hbnb.app.api.v1.amenities import api as amenities_ns
    from hbnb.app.api.v1.places import api as places_ns
    from hbnb.app.api.v1.reviews import api as reviews_ns

    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')

    return app
