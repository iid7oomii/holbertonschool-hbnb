from __future__ import annotations

from typing import Any, List

from hbnb.app.models.base_model import BaseModel
from hbnb.app.models.user import User
from hbnb.app.models.amenity import Amenity


class Place(BaseModel):
    """
    Place entity:
    - title (required, max 100)
    - description (optional)
    - price (positive float)
    - latitude  (-90..90)
    - longitude (-180..180)
    - owner (User instance)
    Relationships:
    - reviews: list of Review
    - amenities: list of Amenity
    """

    def __init__(
        self,
        title: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User,
        description: str = "",
        **kwargs: Any,
    ):
        super().__init__(**kwargs)

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner

        self.reviews: List[Any] = []      # will contain Review objects
        self.amenities: List[Amenity] = []

        self.validate()

    def add_review(self, review: Any) -> None:
        # avoid duplicates
        if review not in self.reviews:
            self.reviews.append(review)
            self.save()

    def add_amenity(self, amenity: Amenity) -> None:
        if amenity not in self.amenities:
            self.amenities.append(amenity)
            self.save()

    def validate(self) -> None:
        if not isinstance(self.title, str) or not self.title.strip():
            raise ValueError("title is required")
        if len(self.title) > 100:
            raise ValueError("title must be at most 100 characters")

        if not isinstance(self.description, str):
            raise ValueError("description must be a string")

        if not isinstance(self.price, (int, float)) or float(self.price) <= 0:
            raise ValueError("price must be a positive number")
        self.price = float(self.price)

        if not isinstance(self.latitude, (int, float)):
            raise ValueError("latitude must be a number")
        if not (-90 <= float(self.latitude) <= 90):
            raise ValueError("latitude must be between -90 and 90")
        self.latitude = float(self.latitude)

        if not isinstance(self.longitude, (int, float)):
            raise ValueError("longitude must be a number")
        if not (-180 <= float(self.longitude) <= 180):
            raise ValueError("longitude must be between -180 and 180")
        self.longitude = float(self.longitude)

        if not isinstance(self.owner, User):
            raise ValueError("owner must be a User instance")