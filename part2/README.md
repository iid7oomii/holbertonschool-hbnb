# HBnB – Business Logic and API (Part 2)

## Overview

This project is **Part 2** of the HBnB application.  
The goal of this part is to implement:

- Core **Business Logic classes**
- A **Facade layer** to connect Business Logic with the API
- RESTful **API endpoints** using Flask and flask-restx
- An **in-memory repository** for persistence
- Full **CRUD operations** for Users, Amenities, Places, and Reviews
- Automated and manual **API testing**

Authentication (JWT) and database persistence are **intentionally excluded** and will be implemented in **Part 3**.

---

## Implemented Features

### Business Logic Layer
Implemented core entities with validation and relationships:

- **User**
- **Amenity**
- **Place**
- **Review**

Common attributes are inherited from a base model:
- `id` (UUID)
- `created_at`
- `updated_at`

Relationships:
- A **User** can own multiple **Places**
- A **Place** can have multiple **Amenities**
- A **Place** can have multiple **Reviews**
- A **Review** is linked to one **User** and one **Place**

---

### API Layer (v1)

Base path:
**/api/v1**


All endpoints follow RESTful conventions and return proper HTTP status codes.

---

## API Endpoints

### Users
| Method | Endpoint | Description |
|------|--------|-------------|
| POST | `/users/` | Create a user |
| GET | `/users/` | Retrieve all users |
| GET | `/users/<user_id>` | Retrieve a user by ID |
| PUT | `/users/<user_id>` | Update user information |

> DELETE is **not implemented** for users in this part.

---

### Amenities
| Method | Endpoint | Description |
|------|--------|-------------|
| POST | `/amenities/` | Create an amenity |
| GET | `/amenities/` | Retrieve all amenities |
| GET | `/amenities/<amenity_id>` | Retrieve an amenity by ID |
| PUT | `/amenities/<amenity_id>` | Update an amenity |

---

### Places
| Method | Endpoint | Description |
|------|--------|-------------|
| POST | `/places/` | Create a place |
| GET | `/places/` | Retrieve all places |
| GET | `/places/<place_id>` | Retrieve place details |
| PUT | `/places/<place_id>` | Update place information |

Each place response includes:
- Owner details
- Associated amenities
- Associated reviews (when applicable)

---

### Reviews
| Method | Endpoint | Description |
|------|--------|-------------|
| POST | `/reviews/` | Create a review |
| GET | `/reviews/` | Retrieve all reviews |
| GET | `/reviews/<review_id>` | Retrieve review by ID |
| PUT | `/reviews/<review_id>` | Update a review |
| DELETE | `/reviews/<review_id>` | Delete a review |
| GET | `/places/<place_id>/reviews` | Get reviews for a place |

> Reviews are the **only entity that supports DELETE** in this part.

---

## Project Structure

```text
part2/
├── run.py
├── requirements.txt
├── README.md
├── TESTING_GUIDE.md
├── curl_tests.sh
├── test_api.py
├── test_user_endpoints.py
├── test_amenity_endpoints.py
├── test_place_endpoints.py
└── hbnb/
    └── app/
        ├── __init__.py
        ├── api/
        │   └── v1/
        │       ├── __init__.py
        │       ├── users.py
        │       ├── amenities.py
        │       ├── places.py
        │       └── reviews.py
        ├── models/
        │   ├── __init__.py
        │   ├── base_model.py
        │   ├── user.py
        │   ├── amenity.py
        │   ├── place.py
        │   └── review.py
        ├── services/
        │   ├── __init__.py
        │   └── facade.py
        └── persistence/
            ├── __init__.py
            └── repository.py
```

---

## Requirements

- Python 3.10+
- Flask
- flask-restx
- pytest
- requests

Install dependencies:
```bash
pip install -r requirements.txt
```

## How to Run the Application
cd part2
python run.py

**Server runs on:**
http://127.0.0.1:5000

**Swagger documentation:**
http://127.0.0.1:5000/api/v1/

## Testing

**Automated Tests**
pytest test_api.py -v

**Individual Endpoint Tests**

python test_user_endpoints.py

python test_amenity_endpoints.py

python test_place_endpoints.py


