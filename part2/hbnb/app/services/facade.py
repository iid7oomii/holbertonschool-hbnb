from hbnb.app.persistence.repository import InMemoryRepository
from hbnb.app.models.user import User


class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # ===== User Management Methods =====

    def create_user(self, user_data):
        """Create a new user"""
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        """Get a user by ID"""
        return self.user_repo.get(user_id)

    def get_all_users(self):
        """Get all users"""
        return self.user_repo.get_all()

    def get_user_by_email(self, email):
        """Get a user by email"""
        return self.user_repo.get_by_attribute('email', email)

    def update_user(self, user_id, user_data):
        """Update a user's information"""
        user = self.user_repo.get(user_id)
        if not user:
            return None

        # Update user attributes
        if 'first_name' in user_data:
            user.first_name = user_data['first_name']
        if 'last_name' in user_data:
            user.last_name = user_data['last_name']
        if 'email' in user_data:
            user.email = user_data['email']
        if 'is_admin' in user_data:
            user.is_admin = user_data['is_admin']

        # Validate the updated user
        user.validate()
        user.save()

        # Update in repository
        self.user_repo.update(user_id, user_data)
        return user

    # ===== Place Management Methods =====

    def get_place(self, place_id):
        """Get a place by ID"""
        pass
