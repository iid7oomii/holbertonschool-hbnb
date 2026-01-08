from hbnb.app.models.user import User
from hbnb.app.models.place import Place
from hbnb.app.models.review import Review
from hbnb.app.models.amenity import Amenity


def main():
    user = User(first_name="Abdullah", last_name="AlSalem", email="a@b.com")
    assert user.is_admin is False

    place = Place(
        title="Nice Apartment",
        description="Near downtown",
        price=250.0,
        latitude=24.7136,
        longitude=46.6753,
        owner=user,
    )

    wifi = Amenity(name="WiFi")
    pool = Amenity(name="Pool")

    place.add_amenity(wifi)
    place.add_amenity(pool)
    assert len(place.amenities) == 2

    review = Review(text="Great place!", rating=5, user=user, place=place)
    assert len(place.reviews) == 1
    assert place.reviews[0] == review

    # test update + validation
    place.update({"price": 300})
    assert place.price == 300.0

    print("✅ All model tests passed!")


if __name__ == "__main__":
    main()