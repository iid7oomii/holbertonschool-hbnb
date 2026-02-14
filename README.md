#  HBnB Evolution - Holberton School Project

##  Project Overview

**HBnB Evolution** is a comprehensive educational project to build an AirBnB-like application, developed in progressive stages. The project aims to apply best practices in software engineering, system design, and REST API development.

---

##  Project Objectives

- Build a robust architecture using **3-Layer Architecture Pattern**
- Implement **Facade Pattern** for complexity management and layer separation
- Create a professional **REST API** using Flask and Flask-RestX
- Comprehensive documentation using **UML Diagrams** (Mermaid)
- Write comprehensive **automated tests**
- Apply **Business Rules** and **Data Validation**

---

##  Project Structure

```
holbertonschool-hbnb/
├── part1/                  # Technical Documentation & UML
│   ├── Diagram/           # UML Diagrams (Package, Business Logic, Sequence)
│   └── README.md          # Architecture & Design Documentation
│
├── part2/                  # Business Logic & API Implementation
│   ├── hbnb/              # Main Application Code
│   │   └── app/
│   │       ├── api/       # API Endpoints (Flask-RestX)
│   │       ├── models/    # Domain Models (User, Place, Review, Amenity)
│   │       ├── services/  # Business Logic (Facade Pattern)
│   │       └── persistence/ # In-Memory Repository
│   ├── run.py             # Server Entry Point
│   ├── requirements.txt   # Required Dependencies
│   ├── test_*.py          # API Tests
│   └── curl_tests.sh      # cURL Tests
│
├── part3/                  # Enhanced Backend with Authentication & Database
│   ├── hbnb/              # Backend Application
│   │   └── app/
│   │       ├── api/       # REST API with JWT Authentication
│   │       ├── models/    # SQLAlchemy Models
│   │       ├── services/  # Facade Pattern
│   │       └── persistence/ # SQLAlchemy Repository
│   ├── config.py          # Flask Configuration
│   ├── run.py             # Application Entry Point
│   ├── init_db.py         # Database Initialization
│   ├── requirements.txt   # Backend Dependencies
│   └── README.md          # Backend Documentation
│
├── part4/                  # Complete Web Client (Full Stack)
│   ├── web_client/        # Frontend Application
│   │   ├── css/           # Styling (Liquid Button Effect)
│   │   ├── scripts/       # JavaScript (8 modules + Three.js)
│   │   ├── images/        # Assets (23 images)
│   │   └── *.html         # 7 HTML Pages
│   ├── hbnb/              # Backend (from Part 3)
│   ├── seed_data.json     # Initial Data (3 users, 6 places)
│   ├── run.py             # Server (port 8000)
│   └── README.md          # Complete Documentation
│
├── instractions           # Technical Documentation & Interview Prep
└── README.md              # This File
```

---

##  Architecture

### 3-Layer Architecture

```
┌─────────────────────────────────────┐
│   Presentation Layer (API)          │
│   - Flask Routes                    │
│   - Request/Response Handling       │
│   - Input Validation                │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Business Logic Layer (Facade)     │
│   - HBnBFacade                      │
│   - Domain Models (User, Place...)  │
│   - Business Rules & Validation     │
└──────────────┬──────────────────────┘
               │
               ▼
┌─────────────────────────────────────┐
│   Persistence Layer (Repository)    │
│   - InMemoryRepository (Part 2)     │
│   - Database (Part 3 - Coming Soon) │
└─────────────────────────────────────┘
```

---

##  Part 1: Technical Documentation (UML)

### Contents

- **Package Diagram**: Illustrates layers and their relationships
- **Class Diagram**: Class design (User, Place, Review, Amenity)
- **Sequence Diagrams**: Operation flow visualization:
  - User Registration
  - Place Creation
  - Review Submission
  - Fetching List of Places

### Available Documentation

- [ README - Part 1](part1/README.md)
- [ Package Diagram](part1/Diagram/1-Diagram_package.md)
- [ Business Logic Diagram](part1/Diagram/2-Diagram_BussinessLogic.md)
- [ Sequence Diagrams](part1/Diagram/)

### Business Rules

####  Users

- Each user has: `first_name`, `last_name`, `email`, `password`, `is_admin`
- Email **must be unique**
- Operations: Create, Update, Delete

####  Places

- Place information: `title`, `description`, `price`, `latitude`, `longitude`
- Each place belongs to an **owner** (User)
- Can be linked to multiple **amenities**
- Operations: Full CRUD

####  Reviews

- Each review is linked to a **Place** and a **User**
- Contains: `rating`, `comment`
- Users **cannot** review their own places

####  Amenities

- Simple information: `name`, `description`
- Can be associated with multiple places

---

##  Part 2: Business Logic & API Implementation

### Technologies Used

- **Flask**: Web Framework
- **Flask-RestX**: REST API + Swagger Documentation
- **Python 3.x**: Programming Language
- **Pytest**: Automated Testing
- **In-Memory Storage**: (Temporary - will be replaced with database in Part 3)

### Implemented Features

 Full **CRUD Operations** for all entities  
 Comprehensive **Data Validation**  
 **Business Rules Enforcement**  
 **RESTful API Design**  
 **Swagger/OpenAPI Documentation**  
 **Automated Testing**  
 **Error Handling**

### API Endpoints

#### Base URL

```
http://localhost:5000/api/v1
```

####  Users API

| Method | Endpoint           | Description              |
| ------ | ------------------ | ------------------------ |
| `POST` | `/users/`          | Create a new user        |
| `GET`  | `/users/`          | Retrieve all users       |
| `GET`  | `/users/<user_id>` | Retrieve a specific user |
| `PUT`  | `/users/<user_id>` | Update user information  |

**Example - Create User:**

```json
POST /api/v1/users/
{
  "first_name": "Abdulrahman",
  "last_name": "Alghamdi",
  "email": "Abdulrahman@example.com",
  "is_admin": false
}
```

---

####  Amenities API

| Method | Endpoint                  | Description                 |
| ------ | ------------------------- | --------------------------- |
| `POST` | `/amenities/`             | Create a new amenity        |
| `GET`  | `/amenities/`             | Retrieve all amenities      |
| `GET`  | `/amenities/<amenity_id>` | Retrieve a specific amenity |
| `PUT`  | `/amenities/<amenity_id>` | Update an amenity           |

**Example:**

```json
POST /api/v1/amenities/
{
  "name": "WiFi"
}
```

---

####  Places API

| Method | Endpoint             | Description              |
| ------ | -------------------- | ------------------------ |
| `POST` | `/places/`           | Create a new place       |
| `GET`  | `/places/`           | Retrieve all places      |
| `GET`  | `/places/<place_id>` | Retrieve place details   |
| `PUT`  | `/places/<place_id>` | Update place information |

**Example:**

```json
POST /api/v1/places/
{
  "title": "Beautiful Apartment in Paris",
  "description": "Spacious apartment with amazing view",
  "price": 150.0,
  "latitude": 48.8566,
  "longitude": 2.3522,
  "owner_id": "uuid-of-owner",
  "amenities": ["uuid-of-amenity-1", "uuid-of-amenity-2"]
}
```

---

####  Reviews API

| Method   | Endpoint                     | Description                |
| -------- | ---------------------------- | -------------------------- |
| `POST`   | `/reviews/`                  | Create a review            |
| `GET`    | `/reviews/`                  | Retrieve all reviews       |
| `GET`    | `/reviews/<review_id>`       | Retrieve a specific review |
| `PUT`    | `/reviews/<review_id>`       | Update a review            |
| `DELETE` | `/reviews/<review_id>`       | Delete a review            |
| `GET`    | `/places/<place_id>/reviews` | Get reviews for a place    |

**Example:**

```json
POST /api/v1/reviews/
{
  "text": "Amazing place!",
  "rating": 5,
  "user_id": "uuid-of-user",
  "place_id": "uuid-of-place"
}
```

---

## 🔐 Part 3: Backend with Authentication & Database

### Key Features

- **JWT Authentication**: Secure token-based authentication with 1-hour expiration
- **Password Hashing**: Bcrypt for secure password storage
- **Role-Based Access Control**: Admin and regular user roles
- **SQLAlchemy ORM**: Database abstraction layer with SQLite
- **Session Management**: Proper database connection lifecycle
- **Protected Endpoints**: Authentication required for sensitive operations

### Technologies Added

```python
Flask-JWT-Extended    # JWT authentication
SQLAlchemy           # ORM for database
bcrypt               # Password hashing
Flask-CORS           # Cross-origin support
```

### Database Schema

- **Users Table**: email (unique), password_hash, first_name, last_name, is_admin
- **Places Table**: title, description, price, location, owner_id (FK)
- **Reviews Table**: text, rating, user_id (FK), place_id (FK)
- **Amenities Table**: name (unique)

### Authentication Flow

1. User submits credentials → POST /api/v1/users/login
2. Backend validates password hash
3. Generate JWT token (contains user_id, email, is_admin)
4. Frontend stores token in cookie
5. Protected routes require: `Authorization: Bearer {token}`

### Admin Privileges

- ✅ Create and manage users
- ✅ Delete any user, place, or review
- ✅ Bypass ownership restrictions
- ✅ Full system administration

### Quick Start (Part 3)

```bash
cd part3
pip install -r requirements.txt
python init_db.py
python run.py
# Server runs on http://127.0.0.1:8000
```

---

## 🌐 Part 4: Complete Web Client (Full Stack)

### 🎨 Frontend Features

- **7 Interactive Pages**: Home, Login, Register, Place Details, Add Review, Add Place, Admin Panel
- **Modern UI/UX**: Animated Aurora shader background using Three.js WebGL
- **Liquid Button Effects**: Smooth animated button interactions with bottom-to-top fill
- **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
- **Client-Side Filtering**: Filter places by price without server requests
- **Dynamic Content**: Real-time data loading from API

### 🎯 Pages Overview

1. **index.html**: Home page with places list and price filter
2. **login.html**: Login form with JWT token storage
3. **register.html**: User registration with auto-login
4. **place.html**: Place details with reviews, delete buttons (owner/admin)
5. **add_review.html**: Review submission form (authenticated users)
6. **add_place.html**: Create new place with image upload
7. **admin.html**: User management panel (admin only)

### 🚀 Frontend Technologies

- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: ES6+ features, async/await
- **Three.js (r128)**: WebGL shader for animated background
- **Fetch API**: Async HTTP requests

### 🔐 Authentication & Authorization

- **JWT Storage**: Cookie-based with 1-hour expiration
- **Role-Based UI**: Different views for admin vs regular users
- **Protected Actions**: Delete buttons only visible to owners/admins
- **Automatic Redirects**: Unauthenticated users redirected to login

### 🖼️ Image Upload System

- **Multi-part Form Data**: File upload with metadata
- **Server-Side Storage**: Images saved to `web_client/images/`
- **Dynamic Display**: Fetched via `<img src="images/{title}.png">`
- **23 Assets**: 6 place images, 13 amenity icons, 4 UI icons

### 🎨 Design System

- **Color Palette**: Black background (#000000), White text, Gold accents
- **Liquid Button Effect**: White → Light gray fill on hover (0.5s animation)
- **Aurora Background**: WebGL shader with animated color waves
- **Typography**: System fonts with 1.6 line-height

### 📊 Integration Points

```
Frontend (port 8000)  ←→  Backend API (port 8000)
     │                          │
     ├─ Login/Register  →  JWT Authentication
     ├─ Fetch Places    →  GET /api/v1/places/
     ├─ Add Place       →  POST /api/v1/places/
     ├─ Upload Image    →  POST /api/v1/places/upload-image
     ├─ Add Review      →  POST /api/v1/reviews/
     ├─ Delete Review   →  DELETE /api/v1/reviews/{id}
     └─ Admin Panel     →  GET/DELETE /api/v1/users/
```

### 📦 Seed Data (3 Test Accounts)

```javascript
// Admin Account
Email: admin@hbnb.com
Password: admin123

// Regular User 1
Email: saleh@hero.com
Password: hero123

// Regular User 2
Email: Ahmed@Alghamdi.com
Password: ahmed123
```

### 🎯 Quick Start (Part 4)

```bash
cd part4
pip install -r requirements.txt
python init_db.py
python run.py
# Open browser: http://127.0.0.1:8000/
```

### ✨ Key Achievements

- ✅ Complete CRUD operations with authorization
- ✅ Image upload and display
- ✅ Three.js animated background (130 lines)
- ✅ Client-side price filtering
- ✅ Admin panel for user management
- ✅ Fully responsive design
- ✅ 10+ technical challenges solved
- ✅ Comprehensive documentation for interviews

---

##  Installation & Setup

### Prerequisites

- Python 3.11+
- pip
- Virtual Environment (recommended)
- Modern web browser (Chrome, Firefox, Edge)

### Installation Steps

```bash
# 1. Navigate to Part 2 folder
cd holbertonschool-hbnb/part2

# 2. Create virtual environment
python -m venv .venv

# 3. Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
source .venv/bin/activate

# 4. Install dependencies
pip install -r requirements.txt

# 5. Run the server
python run.py
```

### Accessing the Application

- **API Base URL**: http://localhost:5000/api/v1/
- **Swagger Documentation**: http://localhost:5000/api/v1/
- **Health Check**: http://localhost:5000/api/v1/users/

---

##  Testing

### Pytest Tests

```bash
# Run all tests
pytest

# Tests with code coverage
pytest --cov=hbnb --cov-report=html

# Test specific file
pytest test_user_endpoints.py -v

# Test specific endpoint
pytest test_place_endpoints.py::test_create_place -v
```

### cURL Tests

```bash
# Run automated cURL tests
bash curl_tests.sh
```

### Manual Testing (Thunder Client / Postman)

See: [ TESTING_GUIDE.md](part2/TESTING_GUIDE.md)

---

##  HTTP Status Codes & Errors

| Status Code          | Meaning              | When It Appears  |
| -------------------- | -------------------- | ---------------- |
| `200 OK`             | Operation successful | GET, PUT         |
| `201 Created`        | Successfully created | POST             |
| `204 No Content`     | Successfully deleted | DELETE           |
| `400 Bad Request`    | Invalid data         | Validation Error |
| `404 Not Found`      | Resource not found   | Wrong ID         |
| `409 Conflict`       | Data conflict        | Duplicate email  |
| `500 Internal Error` | Server error         | Server Error     |

---

##  Data Validation

### Applied Validation Rules

#### Users

-  Email format validation (must contain @)
-  Email uniqueness
-  First name and last name: 1-50 characters
-  Password: minimum 6 characters

#### Places

-  Title: 1-100 characters
-  Price: must be positive
-  Latitude: -90 to 90
-  Longitude: -180 to 180
-  Owner must exist

#### Reviews

-  Rating: 1 to 5 stars
-  Text: 1-1000 characters
-  User cannot review their own place

#### Amenities

-  Name: 1-50 characters
-  Name uniqueness

---

##  Design Patterns Used

### 1. Facade Pattern

- **HBnBFacade**: Unified entry point for Business Logic
- Hides internal complexity from API layer
- Simplifies maintenance and testing

### 2. Repository Pattern

- **InMemoryRepository**: Abstraction over storage layer
- Easy to replace temporary storage with database later
- Separates business logic from storage

### 3. RESTful Design

- Proper use of HTTP Methods
- Resource-based URLs
- Stateless communication
- Proper status codes

---

##  Part 3 - Coming Soon

Upcoming Features:

-  **Authentication & Authorization** (JWT)
-  **Database Integration** (SQLAlchemy + PostgreSQL/MySQL)
-  **User Sessions**
-  **Password Hashing** (bcrypt)
-  **Email Validation**
-  **Image Upload** for places
-  **Advanced Search & Filtering**
-  **Pagination**

---

##  Team

- **ABDULAZIZ ALRASHDI**
- **ABDULRAHMAN ALGHAMDI**
- **ABDULLAH ALSALEM**

---

##  Resources & Documentation

### Internal Documentation

- [📋 Part 1 README](part1/README.md) - Architecture Design & UML
- [🔧 Part 2 README](part2/README.md) - API Details & Implementation
- [🔐 Part 3 README](part3/README.md) - Authentication & Database Integration
- [🌐 Part 4 README](part4/README.md) - Complete Web Client (Full Stack)
- [📚 Technical Documentation](instractions) - Complete Implementation Guide & Interview Prep
- [✅ Testing Guide](part2/TESTING_GUIDE.md) - Comprehensive Testing Guide

### External Resources

- [Flask Documentation](https://flask.palletsprojects.com/)
- [Flask-RestX](https://flask-restx.readthedocs.io/)
- [REST API Best Practices](https://restfulapi.net/)
- [UML Diagrams with Mermaid](https://mermaid.js.org/)

---

##  Troubleshooting

### Issue: 404 Not Found

```bash
# Make sure to use the correct base URL
http://localhost:5000/api/v1/users/  ✅
http://localhost:5000/users/         ❌
```

### Issue: Server Not Running

```bash
# Check the port
netstat -ano | findstr :5000

# Or use a different port
flask run --port 5001
```

### Issue: Import Errors

```bash
# Make sure to activate virtual environment
.venv\Scripts\activate

# Reinstall dependencies
pip install -r requirements.txt
```

---

##  License

This project is educational and owned by **Holberton School**.

---

##  Contact

For questions and inquiries, contact the project team.

---

<div align="center">

**Built with love for Holberton School**
