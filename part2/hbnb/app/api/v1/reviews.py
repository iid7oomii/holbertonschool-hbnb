"""Review API endpoints for HBnB application"""
from flask_restx import Namespace, Resource, fields
from hbnb.app.services.facade import HBnBFacade

api = Namespace('reviews', description='Review operations')

facade = HBnBFacade()

# Define the review model for input validation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text', min_length=1),
    'rating': fields.Integer(required=True, description='Rating (1-5)', min=1, max=5),
    'user_id': fields.String(required=True, description='User ID who wrote the review'),
    'place_id': fields.String(required=True, description='Place ID being reviewed')
})

# Define the review response model
review_response_model = api.model('ReviewResponse', {
    'id': fields.String(description='Review ID'),
    'text': fields.String(description='Review text'),
    'rating': fields.Integer(description='Rating'),
    'user_id': fields.String(description='User ID'),
    'place_id': fields.String(description='Place ID'),
    'user': fields.Nested(api.model('ReviewUser', {
        'id': fields.String(description='User ID'),
        'first_name': fields.String(description='User first name'),
        'last_name': fields.String(description='User last name')
    })),
    'created_at': fields.String(description='Creation date'),
    'updated_at': fields.String(description='Last update date')
})


@api.route('/')
class ReviewList(Resource):
    """Handles operations on the review collection"""

    @api.doc('list_reviews')
    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Get list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'place_id': review.place.id,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                },
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }
            for review in reviews
        ], 200

    @api.doc('create_review')
    @api.expect(review_model, validate=True)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'User or Place not found')
    def post(self):
        """Create a new review"""
        review_data = api.payload

        # Validate user exists
        user = facade.get_user(review_data['user_id'])
        if not user:
            api.abort(404, 'User not found')

        # Validate place exists
        place = facade.get_place(review_data['place_id'])
        if not place:
            api.abort(404, 'Place not found')

        try:
            new_review = facade.create_review(review_data)
            return {
                'id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user.id,
                'place_id': new_review.place.id,
                'user': {
                    'id': new_review.user.id,
                    'first_name': new_review.user.first_name,
                    'last_name': new_review.user.last_name
                },
                'created_at': new_review.created_at.isoformat(),
                'updated_at': new_review.updated_at.isoformat()
            }, 201
        except ValueError as e:
            api.abort(400, str(e))


@api.route('/<review_id>')
@api.param('review_id', 'The review identifier')
class ReviewResource(Resource):
    """Handles operations on a single review"""

    @api.doc('get_review')
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        return {
            'id': review.id,
            'text': review.text,
            'rating': review.rating,
            'user_id': review.user.id,
            'place_id': review.place.id,
            'user': {
                'id': review.user.id,
                'first_name': review.user.first_name,
                'last_name': review.user.last_name
            },
            'created_at': review.created_at.isoformat(),
            'updated_at': review.updated_at.isoformat()
        }, 200

    @api.doc('update_review')
    @api.expect(review_model, validate=True)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update review information"""
        review_data = api.payload

        # Check if review exists
        existing_review = facade.get_review(review_id)
        if not existing_review:
            api.abort(404, 'Review not found')

        # Validate user if being updated
        if 'user_id' in review_data:
            user = facade.get_user(review_data['user_id'])
            if not user:
                api.abort(404, 'User not found')

        # Validate place if being updated
        if 'place_id' in review_data:
            place = facade.get_place(review_data['place_id'])
            if not place:
                api.abort(404, 'Place not found')

        try:
            updated_review = facade.update_review(review_id, review_data)
            return {
                'id': updated_review.id,
                'text': updated_review.text,
                'rating': updated_review.rating,
                'user_id': updated_review.user.id,
                'place_id': updated_review.place.id,
                'user': {
                    'id': updated_review.user.id,
                    'first_name': updated_review.user.first_name,
                    'last_name': updated_review.user.last_name
                },
                'created_at': updated_review.created_at.isoformat(),
                'updated_at': updated_review.updated_at.isoformat()
            }, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.doc('delete_review')
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        review = facade.get_review(review_id)
        if not review:
            api.abort(404, 'Review not found')

        facade.delete_review(review_id)
        return {'message': 'Review deleted successfully'}, 200


@api.route('/places/<place_id>/reviews')
@api.param('place_id', 'The place identifier')
class PlaceReviewList(Resource):
    """Handles operations for reviews of a specific place"""

    @api.doc('get_place_reviews')
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        place = facade.get_place(place_id)
        if not place:
            api.abort(404, 'Place not found')

        reviews = facade.get_reviews_by_place(place_id)
        return [
            {
                'id': review.id,
                'text': review.text,
                'rating': review.rating,
                'user_id': review.user.id,
                'user': {
                    'id': review.user.id,
                    'first_name': review.user.first_name,
                    'last_name': review.user.last_name
                },
                'created_at': review.created_at.isoformat(),
                'updated_at': review.updated_at.isoformat()
            }
            for review in reviews
        ], 200
