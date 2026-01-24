"""
User API endpoints for HBnB application
"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from hbnb.app.services.facade import HBnBFacade

api = Namespace('users', description='User operations')

# Create a facade instance
facade = HBnBFacade()

# Define the user model for input validation and documentation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user', min_length=1, max_length=50),
    'last_name': fields.String(required=True, description='Last name of the user', min_length=1, max_length=50),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status', default=False)
})

# Define the login model
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Define the user response model (without password)
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='First name'),
    'last_name': fields.String(description='Last name'),
    'email': fields.String(description='Email address'),
    'is_admin': fields.Boolean(description='Admin status'),
    'created_at': fields.DateTime(description='Creation date'),
    'updated_at': fields.DateTime(description='Last update date')
})


@api.route('/')
class UserList(Resource):
    """Handles operations on the user collection"""

    @api.doc('list_users')
    @api.marshal_list_with(user_response_model)
    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return users, 200

    @api.doc('create_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model, code=201)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    def post(self):
        """Register a new user"""
        user_data = api.payload

        # Check if email already exists
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            api.abort(409, 'Email already registered')

        try:
            new_user = facade.create_user(user_data)
            return new_user, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    """Handles operations on a single user"""

    @api.doc('get_user')
    @api.marshal_with(user_response_model)
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user details by ID"""
        user = facade.get_user(user_id)
        if not user:
            api.abort(404, 'User not found')
        return user, 200

    @api.doc('update_user')
    @api.expect(user_model, validate=True)
    @api.marshal_with(user_response_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Email already registered')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def put(self, user_id):
        """Update user information (requires authentication)"""
        user_data = api.payload
        
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        
        # Users can only update their own profile (unless admin)
        if current_user_id != user_id:
            api.abort(401, 'Unauthorized to update this user')

        # Check if user exists
        existing_user = facade.get_user(user_id)
        if not existing_user:
            api.abort(404, 'User not found')

        # Check if email is being changed to one that already exists
        if 'email' in user_data and user_data['email'] != existing_user.email:
            user_with_email = facade.get_user_by_email(user_data['email'])
            if user_with_email:
                api.abort(409, 'Email already registered')

        try:
            updated_user = facade.update_user(user_id, user_data)
            return updated_user, 200
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/login')
class UserLogin(Resource):
    """Handles user login and JWT token generation"""

    @api.doc('user_login')
    @api.expect(login_model, validate=True)
    @api.response(200, 'Login successful')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return JWT token"""
        credentials = api.payload
        
        # Get user by email
        user = facade.get_user_by_email(credentials['email'])
        
        # Verify user exists and password is correct
        if not user or not user.verify_password(credentials['password']):
            api.abort(401, 'Invalid credentials')
        
        # Create JWT token with user identity and additional claims
        additional_claims = {
            'is_admin': user.is_admin
        }
        access_token = create_access_token(
            identity=str(user.id),
            additional_claims=additional_claims
        )
        
        return {
            'access_token': access_token,
            'user': {
                'id': user.id,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name,
                'is_admin': user.is_admin
            }
        }, 200
