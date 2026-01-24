from flask import Flask
from flask_restx import Api
from hbnb.app.extensions import bcrypt, jwt


def create_app(config_class="config.DevelopmentConfig"):
    """
    Application factory for creating Flask app instances.
    
    Args:
        config_class: Configuration class to use (default: DevelopmentConfig)
    
    Returns:
        Flask application instance
    """
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    
    api = Api(
        app,
        version="1.0",
        title="HBnB API",
        description="HBnB Application API",
        doc="/api/v1/",
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
