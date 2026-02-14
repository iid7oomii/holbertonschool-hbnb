# HBnB Web Client - Part 4

## 🎯 Overview
Complete web client for HBnB application with authentication, place listings, detailed views, and review submission.

## 📋 Features Implemented

### ✅ Task Requirements Completed:
1. **Login Form** (`login.html`)
   - Email and password fields
   - JWT token storage in cookies
   - Redirect to index on success
   - Error message display

2. **List of Places** (`index.html`)
   - Display all places as cards
   - Price filter (Under $50, $100, $200, All)
   - Show/hide login link based on authentication
   - "View Details" button for each place

3. **Place Details** (`place.html`)
   - Extended place information
   - Host details
   - Amenities list
   - Reviews display
   - "Add Review" button (authenticated users only)

4. **Add Review Form** (`add_review.html`)
   - Authentication check (redirects if not logged in)
   - Review text and rating (1-5)
   - Submit to API with JWT token
   - Success/error messages

### 🎨 CSS Requirements Met:
- **Fixed Parameters:**
  - Margin: 20px for place and review cards ✅
  - Padding: 10px within cards ✅
  - Border: 1px solid (gold color) ✅
  - Border Radius: 10px ✅

- **Custom Styling:**
  - Color Palette: Black, Gold (#FFD700), Dark Red (#8B0000)
  - Modern, elegant design
  - Hover effects and transitions

## 🚀 How to Use

### 1. Start the Backend Server
```bash
cd C:\Users\User\holbertonschool-hbnb\part4
python run.py
```
Server will run on: `http://127.0.0.1:8000`

### 2. Open the Web Client
Open `index.html` in your browser:
```
file:///C:/Users/User/holbertonschool-hbnb/part4/web_client/index.html
```

Or use Live Server extension in VS Code.

### 3. Login Credentials

**Admin Account:**
- Email: `admin@hbnb.com`
- Password: `admin123`

**Regular User:**
- Email: `john@example.com`
- Password: `password123`

## 📝 Testing Workflows

### Test 1: View Places (No Auth Required)
1. Open `index.html`
2. View the list of places
3. Use price filter to filter by price
4. Click "View Details" on any place

### Test 2: Login
1. Click "Login" button
2. Enter email and password
3. On success, redirected to index
4. "Login" button changes to "Logout"

### Test 3: Add Review (Auth Required)
1. Make sure you're logged in
2. Click "View Details" on a place
3. Click "Add a Review" button
4. Fill in review text and rating (1-5)
5. Submit review
6. Redirected back to place details with new review

### Test 4: Logout
1. Click "Logout" button
2. Page reloads
3. "Logout" button changes back to "Login"
4. "Add Review" button no longer visible on place details

## 🛠 Technical Details

### API Endpoints Used:
- `POST /api/v1/users/login` - User authentication
- `GET /api/v1/places/` - List all places
- `GET /api/v1/places/:id` - Get place details
- `POST /api/v1/reviews/` - Submit a review

### Files Structure:
```
web_client/
├── index.html          # Home page with places list
├── login.html          # Login form
├── place.html          # Place details page
├── add_review.html     # Add review form
├── css/
│   └── styles.css      # All styling
├── scripts/
│   ├── index.js        # Home page logic
│   ├── login.js        # Login functionality
│   ├── place.js        # Place details logic
│   └── add_review.js   # Review submission
└── images/
    └── (logo and icons)
```

## ✅ Requirements Checklist

### HTML Structure:
- ✅ Semantic HTML5 elements
- ✅ Header with logo and login button
- ✅ Navigation links
- ✅ Footer with copyright
- ✅ Forms with proper labels and inputs

### CSS Classes (As Required):
- ✅ `.logo`
- ✅ `.login-button`
- ✅ `.place-card`
- ✅ `.details-button`
- ✅ `.place-details`
- ✅ `.place-info`
- ✅ `.review-card`
- ✅ `.add-review`
- ✅ `.form`

### JavaScript Functionality:
- ✅ Cookie management (`getCookie()`)
- ✅ JWT token storage
- ✅ Authentication checks
- ✅ AJAX requests with Fetch API
- ✅ Dynamic DOM manipulation
- ✅ Client-side filtering
- ✅ Error handling

## 🎨 Design Choices

- **Color Scheme:** Luxurious black, gold, and dark red
- **Typography:** Segoe UI, Roboto, Arial
- **Layout:** Responsive, centered content
- **Effects:** Smooth transitions, hover effects, shadows

## 📌 Notes

- Make sure the backend server is running before using the web client
- If you see "No places available", run `python add_sample_data.py` to populate the database
- The application uses cookies for session management
- CORS is enabled on the backend to allow cross-origin requests

## 🔧 Troubleshooting

**Issue:** Can't see places
- **Solution:** Make sure server is running and database has data

**Issue:** Login not working
- **Solution:** Check console for errors, verify server is running

**Issue:** Can't add review
- **Solution:** Make sure you're logged in first

**Issue:** "Failed to fetch" errors
- **Solution:** Check that API URL is correct (http://127.0.0.1:8000)

---

**Date:** February 13, 2026
**Status:** ✅ All Requirements Met
