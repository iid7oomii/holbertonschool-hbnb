"""Place API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from hbnb.app.services.facade import HBnBFacade

api = Namespace('places', description='Place operations')

facade = HBnBFacade()

# Define the place model for input validation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title', min_length=1, max_length=100),
    'description': fields.String(description='Place description', default=''),
    'price': fields.Float(required=True, description='Price per night', min=0.01),
    'latitude': fields.Float(required=True, description='Latitude', min=-90, max=90),
    'longitude': fields.Float(required=True, description='Longitude', min=-180, max=180),
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
        return [
            {
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.owner.id,
                'owner': {
                    'id': place.owner.id,
                    'first_name': place.owner.first_name,
                    'last_name': place.owner.last_name,
                    'email': place.owner.email
                },
                'amenities': [
                    {'id': amenity.id, 'name': amenity.name}
                    for amenity in place.amenities
                ],
                'reviews': [
                    {
                        'id': review.id,
                        'text': review.text,
                        'rating': review.rating,
                        'user_id': review.user.id
                    }
                    for review in place.reviews
                ],
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            }
            for place in places
        ], 200

    @api.doc('create_place')
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Owner not found')
    def post(self):
        """Create a new place"""
        place_data = api.payload

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

        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.owner.id,
            'owner': {
                'id': place.owner.id,
                'first_name': place.owner.first_name,
                'last_name': place.owner.last_name,
                'email': place.owner.email
            },
            'amenities': [
                {'id': amenity.id, 'name': amenity.name}
                for amenity in place.amenities
            ],
            'reviews': [
                {
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user.id
                }
                for review in place.reviews
            ],
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat()
        }, 200

    @api.doc('update_place')
    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update place information"""
        place_data = api.payload

        # Check if place exists
        existing_place = facade.get_place(place_id)
        if not existing_place:
            api.abort(404, 'Place not found')

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
