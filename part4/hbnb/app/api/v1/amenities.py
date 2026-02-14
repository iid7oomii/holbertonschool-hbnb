"""Amenity API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt
from hbnb.app.services.facade import HBnBFacade

api = Namespace('amenities', description='Amenity operations')

facade = HBnBFacade()


def is_admin():
    """Helper function to check if the current user is an admin"""
    claims = get_jwt()
    return claims.get('is_admin', False)

# Define the amenity model for input validation
amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Amenity name', min_length=1, max_length=50)
})

# Define the amenity response model
amenity_response_model = api.model('AmenityResponse', {
    'id': fields.String(description='Amenity ID'),
    'name': fields.String(description='Amenity name'),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})


@api.route('/')
class AmenityList(Resource):
    """Handles operations on the amenity collection"""

    @api.doc('list_amenities')
    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get list of all amenities"""
        amenities = facade.get_all_amenities()
        return [
            {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat(),
                'updated_at': amenity.updated_at.isoformat()
            }
            for amenity in amenities
        ], 200

    @api.doc('create_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity with this name already exists')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (requires admin privileges)"""
        # Check if user is admin
        if not is_admin():
            api.abort(403, 'Admin privileges required')
        
        amenity_data = api.payload

        # Check if amenity with same name already exists
        existing_amenity = facade.get_amenity_by_name(amenity_data['name'])
        if existing_amenity:
            api.abort(409, 'Amenity with this name already exists')

        try:
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat(),
                'updated_at': new_amenity.updated_at.isoformat()
            }, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    """Handles operations on a single amenity"""

    @api.doc('get_amenity')
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            api.abort(404, 'Amenity not found')

        return {
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat(),
            'updated_at': amenity.updated_at.isoformat()
        }, 200

    @api.doc('update_amenity')
    @api.expect(amenity_model, validate=True)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(409, 'Amenity with this name already exists')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity information (requires admin privileges)"""
        # Check if user is admin
        if not is_admin():
            api.abort(403, 'Admin privileges required')
        
        amenity_data = api.payload

        # Check if amenity exists
        existing_amenity = facade.get_amenity(amenity_id)
        if not existing_amenity:
            api.abort(404, 'Amenity not found')

        # Check if name is being changed to one that already exists
        if 'name' in amenity_data:
            amenity_with_name = facade.get_amenity_by_name(
                amenity_data['name'])
            if amenity_with_name and amenity_with_name.id != amenity_id:
                api.abort(409, 'Amenity with this name already exists')

        try:
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat(),
                'updated_at': updated_amenity.updated_at.isoformat()
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
