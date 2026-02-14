#  HBnB Evolution - Part 4: Web Client

##  Overview

**HBnB Evolution Part 4** is a complete full-stack web application that connects a modern, interactive frontend with a Flask REST API backend. This project demonstrates advanced web development concepts including JWT authentication, role-based access control, real-time interactions, and stunning visual effects.

###  Key Highlights

-  **Modern UI/UX**: Animated Aurora shader background using Three.js WebGL
-  **Secure Authentication**: JWT-based authentication with cookie storage
-  **Admin Panel**: Full user management system for administrators
-  **Image Upload**: Complete image upload system for places
-  **Responsive Design**: Works seamlessly on desktop, tablet, and mobile
-  **Real-time Filtering**: Client-side price filtering without page reloads
-  **Liquid Button Effects**: Smooth, animated button interactions
-  **Authorization System**: Owner and admin-based delete permissions

---

##  Features

### Frontend Features
-  **7 Interactive Pages**: Home, Login, Register, Place Details, Add Review, Add Place, Admin Panel
-  **Dynamic Content Loading**: Fetch data from API and render dynamically
-  **Client-Side Filtering**: Filter places by price without server requests
-  **Authentication Flow**: Secure login/register with JWT tokens
-  **Image Upload**: Multi-part form data upload for place images
-  **Review System**: Add and delete reviews with authorization checks
-  **Admin Dashboard**: Manage users, create admins, delete users
-  **Three.js Background**: Animated Aurora Borealis shader effect

### Backend Features
-  **RESTful API**: Comprehensive API with Flask-RESTX
-  **JWT Authentication**: Secure token-based authentication
-  **SQLAlchemy ORM**: Database abstraction with SQLite
-  **Role-Based Access**: Admin and regular user roles
-  **CORS Support**: Cross-origin resource sharing enabled
-  **Image Handling**: Server-side image upload and storage
-  **Seed Data**: Auto-load initial data on startup
-  **Session Management**: Proper SQLAlchemy session cleanup

---

##  Quick Start

### Prerequisites
- Python 3.11+
- pip (Python package manager)
- Modern web browser (Chrome, Firefox, Edge)

### Installation

1. **Clone the Repository**
```bash
cd holbertonschool-hbnb/part4
```

2. **Install Dependencies**
```bash
pip install -r requirements.txt
```

3. **Initialize Database**
```bash
python init_db.py
```

4. **Run the Application**
```bash
python run.py
```

5. **Open in Browser**
```
http://127.0.0.1:8000/
```

---

##  Project Structure

```
part4/
├── web_client/                      # Frontend Application
│   ├── index.html                   # Home page (places list)
│   ├── login.html                   # Login page
│   ├── register.html                # Registration page
│   ├── place.html                   # Place details page
│   ├── add_review.html              # Add review page
│   ├── add_place.html               # Add place page
│   ├── admin.html                   # Admin panel page
│   │
│   ├── css/
│   │   └── styles.css               # Complete styling (420 lines)
│   │
│   ├── scripts/
│   │   ├── index.js                 # Home page logic
│   │   ├── login.js                 # Login functionality
│   │   ├── register.js              # Registration logic
│   │   ├── place.js                 # Place details & reviews
│   │   ├── add_review.js            # Review submission
│   │   ├── add_place.js             # Place creation
│   │   ├── admin.js                 # Admin panel logic
│   │   └── animated-background.js   # Three.js shader
│   │
│   └── images/                      # All images (23 files)
│       ├── logo.png                 # App logo
│       ├── icon.png                 # Favicon
│       ├── star.png                 # Rating stars
│       ├── trach.png                # Delete icon
│       ├── [6 Place Images]         # Place photos
│       └── [13 Amenity Icons]       # Amenity PNG icons
│
├── hbnb/                            # Backend Application
│   └── app/
│       ├── __init__.py              # Flask app factory + CORS
│       ├── extensions.py            # SQLAlchemy & JWT setup
│       │
│       ├── api/v1/                  # REST API Endpoints
│       │   ├── users.py             # User CRUD + login/register
│       │   ├── places.py            # Place CRUD + image upload
│       │   ├── reviews.py           # Review CRUD + authorization
│       │   └── amenities.py         # Amenity endpoints
│       │
│       ├── models/                  # Data Models
│       │   ├── user.py              # User (+ is_admin field)
│       │   ├── place.py             # Place (+ location field)
│       │   ├── review.py            # Review
│       │   ├── amenity.py           # Amenity
│       │   └── base_model.py        # Base class
│       │
│       ├── persistence/             # Data Layer
│       │   └── repository.py        # SQLAlchemy repository
│       │
│       └── services/                # Business Logic
│           ├── facade.py            # Facade pattern
│           └── repositories/
│               └── user_repository.py
│
├── config.py                        # Flask configuration
├── run.py                           # Application entry point
├── init_db.py                       # Database initialization
├── load_seed_data.py                # Seed data loader
├── seed_data.json                   # Initial data (3 users, 6 places, 6 amenities, 4 reviews)
├── requirements.txt                 # Python dependencies
├── development.db                   # SQLite database
└── README.md                        # This file
```

---

##  Pages Overview

### 1. **Home Page** (`index.html`)
- Displays all places as interactive cards
- Price filter dropdown (All, $10, $50, $100)
- Dynamic navigation based on login status
- Admin button for admin users only
- Animated Aurora background

### 2. **Login Page** (`login.html`)
- Email and password fields
- JWT token storage in cookies
- Error handling with user feedback
- Auto-redirect to home after login

### 3. **Registration Page** (`register.html`)
- First name, last name, email, password
- Automatic login after successful registration
- Email validation and duplicate checking
- Password strength requirements

### 4. **Place Details** (`place.html`)
- Complete place information display
- Host details section
- Amenities with custom icons
- Reviews list with user names and ratings
- Delete buttons (owner/admin only)
- Add review button (authenticated users)

### 5. **Add Review** (`add_review.html`)
- Text area for review content
- Star rating selector (1-5)
- Authentication required
- Redirect to place page after submission

### 6. **Add Place** (`add_place.html`)
- Title, description, location fields
- Price input
- Image file upload
- Amenities selection (checkboxes)
- Authentication required
- Real-time validation

### 7. **Admin Panel** (`admin.html`)
- User list table (name, email, admin status)
- Delete user functionality
- Add new admin user form
- Admin-only access with redirect

---

##  Authentication & Authorization

### User Roles
- **Regular User**: Can create places, add reviews, delete own content
- **Admin**: Full access including user management and delete any content

### Authentication Flow
```
1. User submits login form
   ↓
2. POST /api/v1/users/login
   ↓
3. Backend validates credentials
   ↓
4. Generate JWT token (1 hour expiration)
   ↓
5. Frontend stores token in cookie
   ↓
6. All subsequent requests include:
   Authorization: Bearer {token}
```

### Test Accounts
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

---

## 🔌 API Endpoints

### Users
- `POST /api/v1/users/` - Create new user
- `POST /api/v1/users/login` - Login (returns JWT)
- `GET /api/v1/users/` - List all users (admin only)
- `GET /api/v1/users/{id}` - Get user details
- `PUT /api/v1/users/{id}` - Update user (owner/admin)
- `DELETE /api/v1/users/{id}` - Delete user (admin only)

### Places
- `GET /api/v1/places/` - List all places
- `POST /api/v1/places/` - Create place (auth required)
- `GET /api/v1/places/{id}` - Get place details
- `PUT /api/v1/places/{id}` - Update place (owner/admin)
- `DELETE /api/v1/places/{id}` - Delete place (owner/admin)
- `POST /api/v1/places/upload-image` - Upload place image (auth required)

### Reviews
- `GET /api/v1/reviews/` - List all reviews
- `POST /api/v1/reviews/` - Create review (auth required)
- `GET /api/v1/reviews/{id}` - Get review details
- `PUT /api/v1/reviews/{id}` - Update review (owner/admin)
- `DELETE /api/v1/reviews/{id}` - Delete review (owner/admin)

### Amenities
- `GET /api/v1/amenities/` - List all amenities
- `POST /api/v1/amenities/` - Create amenity (admin only)
- `GET /api/v1/amenities/{id}` - Get amenity details
- `PUT /api/v1/amenities/{id}` - Update amenity (admin only)

---

##  Technical Stack

### Frontend
- **HTML5**: Semantic markup
- **CSS3**: Modern styling with animations
- **Vanilla JavaScript**: ES6+ features
- **Three.js (r128)**: WebGL shader for background
- **Fetch API**: Async HTTP requests

### Backend
- **Flask 3.0.0**: Python web framework
- **Flask-RESTX**: REST API framework
- **Flask-JWT-Extended**: JWT authentication
- **Flask-CORS**: Cross-origin resource sharing
- **SQLAlchemy**: ORM for database
- **SQLite**: Database engine
- **Werkzeug**: Password hashing

### Design Patterns
- **Facade Pattern**: Simplified interface to complex subsystems
- **Repository Pattern**: Data access abstraction
- **Factory Pattern**: Flask app factory
- **MVC Pattern**: Model-View-Controller architecture

---

##  Design System

### Color Palette
- **Primary Background**: `#000000` (Black)
- **Text on Dark**: `#ffffff` (White)
- **Text on Light**: `#000000` (Black)
- **Accent**: `#FFD700` (Gold)
- **Button Background**: `#ffffff` (White)
- **Button Hover Fill**: `#D3D3D3` (Light Gray)
- **Border**: `#333333` (Dark Gray)

### Liquid Button Effect
```css
/* White button with bottom-to-top gray fill on hover */
- Initial: White background
- Hover: Light gray fills from bottom
- Animation: 0.5s smooth transition
- Transform: Scale 1.05
```

### Typography
- **Font Family**: System fonts (Arial, Helvetica, sans-serif)
- **Heading Size**: 2em - 2.5em
- **Body Text**: 1em
- **Line Height**: 1.6

---

##  Database Schema

### Users Table
```sql
id          TEXT PRIMARY KEY
email       TEXT UNIQUE NOT NULL
password    TEXT NOT NULL
first_name  TEXT NOT NULL
last_name   TEXT NOT NULL
is_admin    BOOLEAN DEFAULT FALSE
created_at  DATETIME
updated_at  DATETIME
```

### Places Table
```sql
id          TEXT PRIMARY KEY
title       TEXT NOT NULL
description TEXT
price       FLOAT NOT NULL
latitude    FLOAT NOT NULL
longitude   FLOAT NOT NULL
location    TEXT
owner_id    TEXT (Foreign Key → Users)
created_at  DATETIME
updated_at  DATETIME
```

### Reviews Table
```sql
id          TEXT PRIMARY KEY
text        TEXT NOT NULL
rating      INTEGER (1-5)
user_id     TEXT (Foreign Key → Users)
place_id    TEXT (Foreign Key → Places)
created_at  DATETIME
updated_at  DATETIME
```

### Amenities Table
```sql
id          TEXT PRIMARY KEY
name        TEXT UNIQUE NOT NULL
created_at  DATETIME
updated_at  DATETIME
```

---

## 🧪 Testing

### Manual Testing

1. **Test Authentication**
```bash
# Login as admin
curl -X POST http://127.0.0.1:8000/api/v1/users/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@hbnb.io","password":"admin123"}'
```

2. **Test Place Creation**
```bash
# Create a new place (requires JWT token)
curl -X POST http://127.0.0.1:8000/api/v1/places/ \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"Test Place","description":"Test","price":100,"latitude":0,"longitude":0,"location":"Test City"}'
```

3. **Test Image Upload**
```bash
# Upload image (requires JWT token)
curl -X POST http://127.0.0.1:8000/api/v1/places/upload-image \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -F "image=@path/to/image.png" \
  -F "place_title=Test Place"
```

### Browser Testing Checklist
- [ ] Home page loads with 6 places
- [ ] Price filter works without reload
- [ ] Login with admin@hbnb.io
- [ ] Admin button appears after login
- [ ] Admin panel shows user list
- [ ] Create new place with image
- [ ] Add review to place
- [ ] Delete own review
- [ ] Admin can delete any review
- [ ] Delete own place
- [ ] Admin can delete any place
- [ ] Logout and login again
- [ ] Data persists after restart

---

##  Troubleshooting

### Port Already in Use
```bash
# Windows
netstat -ano | findstr :8000
taskkill /PID <PID> /F

# Or change port in run.py
app.run(host='127.0.0.1', port=8001, debug=True)
```

### CORS Errors
```python
# Already configured in app/__init__.py
# If issues persist, check browser console for exact origin
CORS(app, resources={
    r"/api/*": {
        "origins": ["http://127.0.0.1:8000", "http://localhost:8000"]
    }
})
```

### Database Locked
```bash
# Stop all Python processes
# Delete database and reinitialize
del development.db
python init_db.py
python run.py
```

### JWT Token Expired
```javascript
// Tokens expire after 1 hour
// Simply log in again to get a new token
// Token stored in cookie: document.cookie
```

---

##  Future Enhancements

### Planned Features
- [ ] Edit place functionality
- [ ] User profile page
- [ ] Favorite places system
- [ ] Search functionality (by name, location)
- [ ] Pagination for places list
- [ ] Email verification
- [ ] Password reset flow
- [ ] Image optimization (WebP format)
- [ ] Real-time notifications
- [ ] Booking system

### Performance Optimizations
- [ ] Lazy loading for images
- [ ] Virtual scrolling for long lists
- [ ] Redis caching for API responses
- [ ] PostgreSQL migration for production
- [ ] CDN for static assets
- [ ] API rate limiting

---

##  Authors

**Holberton School Project**
- Developed as part of HBnB Evolution curriculum
- Part 4: Web Client Implementation
- By Abdulrahman Alghamdi

---

##  License

This project is licensed under the MIT License.

---

##  Acknowledgments

- **Three.js**: For amazing WebGL rendering
- **Flask**: For robust backend framework
- **SQLAlchemy**: For powerful ORM
- **Holberton School**: For project guidance

---

##  Additional Documentation

For more detailed information, see:
- **[instractions](../instractions)**: Complete technical documentation with error solutions and interview prep
- **Frontend Guide**: HTML/CSS/JavaScript implementation details
- **Backend Guide**: Flask API architecture and patterns
- **Authentication Guide**: JWT implementation and security

---

##  Quick Links

- **Application**: http://127.0.0.1:8000/
- **API Documentation**: http://127.0.0.1:8000/api/v1/
- **Admin Panel**: http://127.0.0.1:8000/admin.html
- **GitHub**: [Repository link](https://github.com/iid7oomii/holbertonschool-hbnb/tree/main)

---

**Built with love for HBnB Project**
