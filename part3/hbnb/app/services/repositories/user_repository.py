from __future__ import annotations

from hbnb.app.persistence.repository import SQLAlchemyRepository
from hbnb.app.models.user import User


class UserRepository(SQLAlchemyRepository):
    """
    UserRepository extends SQLAlchemyRepository with User-specific methods.
    """

    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email: str) -> User | None:
        """
        Get a user by email address.
        
        Args:
            email: The email address to search for
            
        Returns:
            User object if found, None otherwise
        """
        return self.model.query.filter_by(email=email).first()
