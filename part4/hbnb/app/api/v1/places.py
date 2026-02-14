"""Place API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from flask import request
from hbnb.app.services.facade import HBnBFacade
import os
from werkzeug.utils import secure_filename

api = Namespace('places', description='Place operations')

facade = HBnBFacade()


def is_admin():
    """Helper function to check if the current user is an admin"""
    claims = get_jwt()
    return claims.get('is_admin', False)

# Define the place model for input validation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title', min_length=1, max_length=100),
    'description': fields.String(description='Place description', default=''),
    'price': fields.Float(required=True, description='Price per night', min=0.01),
    'latitude': fields.Float(required=True, description='Latitude', min=-90, max=90),
    'longitude': fields.Float(required=True, description='Longitude', min=-180, max=180),
    'location': fields.String(description='Location name', default=''),
    'owner_id': fields.String(required=True, description='Owner user ID'),
    'amenities': fields.List(fields.String, description='List of amenity IDs', default=[])
})

# Define the place response model
place_response_model = api.model('PlaceResponse', {
    'id': fields.String(description='Place ID'),
    'title': fields.String(description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(description='Price per night'),
    'latitude': fields.Float(description='Latitude'),
    'longitude': fields.Float(description='Longitude'),
    'location': fields.String(description='Location name'),
    'owner_id': fields.String(description='Owner user ID'),
    'owner': fields.Nested(api.model('PlaceOwner', {
        'id': fields.String(description='Owner ID'),
        'first_name': fields.String(description='Owner first name'),
        'last_name': fields.String(description='Owner last name'),
        'email': fields.String(description='Owner email')
    })),
    'amenities': fields.List(fields.Nested(api.model('PlaceAmenity', {
        'id': fields.String(description='Amenity ID'),
        'name': fields.String(description='Amenity name')
    }))),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})


@api.route('/')
class PlaceList(Resource):
    """Handles operations on the place collection"""

    @api.doc('list_places')
    @api.response(200, 'List of places retrieved successfully')
    def get(self):
        """Get list of all places"""
        places = facade.get_all_places()
        result = []
        for place in places:
            place_dict = {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'location': getattr(place, 'location', ''),
                'owner_id': place.owner_id,
                'amenities': [
                    {'id': amenity.id, 'name': amenity.name}
                    for amenity in place.amenities
                ],
                'reviews': [],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }
            
            # Safely get owner details
            try:
                if hasattr(place, 'owner') and place.owner:
                    place_dict['owner'] = {
                        'id': place.owner_id,
                        'first_name': place.owner.first_name,
                        'last_name': place.owner.last_name,
                        'email': place.owner.email
                    }
                else:
                    place_dict['owner'] = None
            except:
                place_dict['owner'] = None
            
            # Safely get reviews
            try:
                place_dict['reviews'] = [
                    {
                        'id': review.id,
                        'text': review.text,
                        'rating': review.rating,
                        'user_id': getattr(review.user, 'id', getattr(review, 'user_id', None)),
                        'user': {
                            'id': review.user.id,
                            'first_name': review.user.first_name,
                            'last_name': review.user.last_name
                        } if hasattr(review, 'user') and review.user else None
                    }
                    for review in place.reviews
                ]
            except:
                place_dict['reviews'] = []
            
            result.append(place_dict)
        
        return result

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create a new place (requires authentication)"""
        place_data = api.payload
        
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        
        # Ensure the owner_id in the payload matches the authenticated user
        if place_data['owner_id'] != current_user_id:
            api.abort(401, 'Unauthorized: You can only create places for yourself')

        # Validate owner exists
        owner = facade.get_user(place_data['owner_id'])
        if not owner:
            api.abort(404, 'Owner not found')

        # Validate amenities if provided
        amenity_ids = place_data.get('amenities', [])
        amenities = []
        for amenity_id in amenity_ids:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                api.abort(404, f'Amenity with ID {amenity_id} not found')
            amenities.append(amenity)

        try:
            new_place = facade.create_place(place_data)
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'location': getattr(new_place, 'location', ''),
                'owner_id': new_place.owner.id,
                'owner': {
                    'id': new_place.owner.id,
                    'first_name': new_place.owner.first_name,
                    'last_name': new_place.owner.last_name,
                    'email': new_place.owner.email
                },
                'amenities': [
                    {'id': amenity.id, 'name': amenity.name}
                    for amenity in new_place.amenities
                ],
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    """Handles operations on a single place"""

    @api.doc('get_place')
    @api.response(200, 'Place details retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place details by ID"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        result = {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'location': getattr(place, 'location', ''),
            'owner_id': place.owner_id,
            'amenities': [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ],
            'reviews': [],
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat()
        }
        
        # Safely get owner details
        try:
            if hasattr(place, 'owner') and place.owner:
                result['owner'] = {
                    'id': place.owner_id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                }
            else:
                result['owner'] = None
        except:
            result['owner'] = None
        
        # Safely get reviews
        try:
            result['reviews'] = [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': getattr(review.user, 'id', getattr(review, 'user_id', None)),
                    'user': {
                        'id': review.user.id,
                        'first_name': review.user.first_name,
                        'last_name': review.user.last_name
                    } if hasattr(review, 'user') and review.user else None
                }
                for review in place.reviews
            ]
        except:
            result['reviews'] = []

        return result

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Unauthorized to modify this place')
    @jwt_required()
    def put(self, place_id):
        """Update place information (requires authentication and ownership)"""
        place_data = api.payload
        
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()

        # Check if place exists
        existing_place = facade.get_place(place_id)
        if not existing_place:
            api.abort(404, 'Place not found')
        
        # Debug: print the IDs for troubleshooting
        print(f"\n[DEBUG] Update Place:")
        print(f"  Current User ID (from token): {current_user_id}")
        print(f"  Place Owner ID: {existing_place.owner.id}")
        print(f"  Match: {existing_place.owner.id == current_user_id}")
        print(f"  Is Admin: {is_admin()}")
        
        # Check if the current user is the owner of the place or is admin
        if str(existing_place.owner.id) != str(current_user_id) and not is_admin():
            api.abort(403, 'Unauthorized: You can only modify your own places')

        # Validate owner if being updated
        if 'owner_id' in place_data:
            owner = facade.get_user(place_data['owner_id'])
            if not owner:
                api.abort(404, 'Owner not found')

        # Validate amenities if being updated
        if 'amenities' in place_data:
            amenity_ids = place_data['amenities']
            for amenity_id in amenity_ids:
                amenity = facade.get_amenity(amenity_id)
                if not amenity:
                    api.abort(404, f'Amenity with ID {amenity_id} not found')

        try:
            updated_place = facade.update_place(place_id, place_data)
            return {
                'id': updated_place.id,
                'title': updated_place.title,
                'description': updated_place.description,
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'location': getattr(updated_place, 'location', ''),
                'owner_id': updated_place.owner.id,
                'owner': {
                    'id': updated_place.owner.id,
                    'first_name': updated_place.owner.first_name,
                    'last_name': updated_place.owner.last_name,
                    'email': updated_place.owner.email
                },
                'amenities': [
                    {'id': amenity.id, 'name': amenity.name}
                    for amenity in updated_place.amenities
                ],
                'created_at': updated_place.created_at.isoformat(),
                'updated_at': updated_place.updated_at.isoformat()
            }, 200
        except ValueError as e:
            api.abort(400, str(e))
    
    @api.doc('delete_place')
    @api.response(200, 'Place deleted successfully')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized to delete this place')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (requires authentication and ownership)"""
        # Get the current user from JWT token
        current_user_id = get_jwt_identity()
        
        # Check if place exists
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')
        
        # Check if the current user is the owner of the place or is admin
        if place.owner.id != current_user_id and not is_admin():
            api.abort(403, 'Unauthorized: You can only delete your own places')
        
        # Delete the place
        facade.place_repo.delete(place_id)
        return {'message': 'Place deleted successfully'}, 200


@api.route('/upload-image')
class PlaceImageUpload(Resource):
    """Handles place image upload"""

    @api.doc('upload_place_image')
    @api.response(200, 'Image uploaded successfully')
    @api.response(400, 'Invalid file or missing data')
    @api.response(401, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Upload an image for a place"""
        current_user_id = get_jwt_identity()
        
        # Check if image file is in request
        if 'image' not in request.files:
            api.abort(400, 'No image file provided')
        
        file = request.files['image']
        place_title = request.form.get('place_title', '')
        
        if file.filename == '':
            api.abort(400, 'No file selected')
        
        # Validate file type
        allowed_extensions = {'png', 'jpg', 'jpeg', 'gif'}
        filename = secure_filename(file.filename)
        file_ext = filename.rsplit('.', 1)[1].lower() if '.' in filename else ''
        
        if file_ext not in allowed_extensions:
            api.abort(400, 'Invalid file type. Allowed: PNG, JPG, JPEG, GIF')
        
        # Create filename based on place title
        if place_title:
            safe_title = secure_filename(place_title)
            new_filename = f"{safe_title}.{file_ext}"
        else:
            new_filename = filename
        
        # Save to images folder
        try:
            base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))))
            images_dir = os.path.join(base_dir, 'web_client', 'images')
            
            # Create images directory if it doesn't exist
            os.makedirs(images_dir, exist_ok=True)
            
            file_path = os.path.join(images_dir, new_filename)
            file.save(file_path)
            
            return {
                'message': 'Image uploaded successfully',
                'filename': new_filename,
                'path': f'images/{new_filename}'
            }, 200
        except Exception as e:
            api.abort(500, f'Error saving image: {str(e)}')
