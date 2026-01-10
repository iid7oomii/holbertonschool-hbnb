# 🏠 HBnB Evolution - Holberton School Project

## 📋 Project Overview

**HBnB Evolution** is a comprehensive educational project to build an AirBnB-like application, developed in progressive stages. The project aims to apply best practices in software engineering, system design, and REST API development.

---

## 🎯 Project Objectives

- Build a robust architecture using **3-Layer Architecture Pattern**
- Implement **Facade Pattern** for complexity management and layer separation
- Create a professional **REST API** using Flask and Flask-RestX
- Comprehensive documentation using **UML Diagrams** (Mermaid)
- Write comprehensive **automated tests**
- Apply **Business Rules** and **Data Validation**

---

## 📂 Project Structure

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
└── README.md              # This File
```

---

## 🏗️ Architecture

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

## 📦 Part 1: Technical Documentation (UML)

### Contents

- **Package Diagram**: Illustrates layers and their relationships
- **Class Diagram**: Class design (User, Place, Review, Amenity)
- **Sequence Diagrams**: Operation flow visualization:
  - User Registration
  - Place Creation
  - Review Submission
  - Fetching List of Places

### Available Documentation

- [📄 README - Part 1](part1/README.md)
- [📊 Package Diagram](part1/Diagram/1-Diagram_package.md)
- [🎨 Business Logic Diagram](part1/Diagram/2-Diagram_BussinessLogic.md)
- [🔄 Sequence Diagrams](part1/Diagram/)

### Business Rules

#### 👤 Users

- Each user has: `first_name`, `last_name`, `email`, `password`, `is_admin`
- Email **must be unique**
- Operations: Create, Update, Delete

#### 🏘️ Places

- Place information: `title`, `description`, `price`, `latitude`, `longitude`
- Each place belongs to an **owner** (User)
- Can be linked to multiple **amenities**
- Operations: Full CRUD

#### ⭐ Reviews

- Each review is linked to a **Place** and a **User**
- Contains: `rating`, `comment`
- Users **cannot** review their own places

#### 🛋️ Amenities

- Simple information: `name`, `description`
- Can be associated with multiple places

---

## 🚀 Part 2: Business Logic & API Implementation

### Technologies Used

- **Flask**: Web Framework
- **Flask-RestX**: REST API + Swagger Documentation
- **Python 3.x**: Programming Language
- **Pytest**: Automated Testing
- **In-Memory Storage**: (Temporary - will be replaced with database in Part 3)

### Implemented Features

✅ Full **CRUD Operations** for all entities  
✅ Comprehensive **Data Validation**  
✅ **Business Rules Enforcement**  
✅ **RESTful API Design**  
✅ **Swagger/OpenAPI Documentation**  
✅ **Automated Testing**  
✅ **Error Handling**

### API Endpoints

#### Base URL

```
http://localhost:5000/api/v1
```

#### 👥 Users API

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
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "is_admin": false
}
```

---

#### 🛋️ Amenities API

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

#### 🏠 Places API

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

#### ⭐ Reviews API

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

## 🛠️ Installation & Setup

### Prerequisites

- Python 3.8+
- pip
- Virtual Environment (recommended)

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

## 🧪 الاختبار (Testing)

### اختبارات Pytest

<div dTesting

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

See حالات HTTP والأخطاء

| Status Code          | المعنى           | متى يظهر         |
| -------------------- | ---------------- | ---------------- |
| `200 OK`             | نجاح العملية     | GET, PUT         |
| `201 Created`        | تم الإنشاء بنجاح | POST             |
| `204 No Content`     | حُذف بنجاح       | DELETE           |
| `400 Bad Request`    | بيانات غير صحيحة | Validation Error |
| `404 Not Found`      | المورد غير موجود | Wrong ID         |
| `409 Conflict`       | تضارب بالبيانات  | Duplicate email  |
| `500 Internal Error` | خطأ في السيرفر   | Server Error     |

---HTTP Status Codes & Errors

| Status Code          | Meaning              | When It Appears  |
| -------------------- | -------------------- | ---------------- |
| `200 OK`             | Operation successful | GET, PUT         |
| `201 Created`        | Successfully created | POST             |
| `204 No Content`     | Successfully deleted | DELETE           |
| `400 Bad Request`    | Invalid data         | Validation Error |
| `404 Not Found`      | Resource not found   | Wrong ID         |
| `409 Conflict`       | Data conflict        | Duplicate email  |
| `500 Internal Error` | Server error acters  |

- ✅ Password: minimum 6 characters

#### Places

- ✅ Title: 1-100 characters
- ✅ Applied Validation Rulesive
- ✅ Latitude: -90 to 90
- ✅ Longitude: -180 to 180
- ✅ Owner must exist

#### Reviews

- ✅ Rating: 1 to 5 stars
- ✅ Text: 1-1000 characters
- ✅ User cannot review their own place

#### Amenities

- ✅ Name: 1-50 characters
- ✅ Name uniqueness

---

## 🎨 Design Patterns المستخدمة

### 1. Facade Pattern

- **HBnBFacade**: نقطة دخول موحدة للـ Business Logic
- يُخفي التعقيد الداخلي عن طبقة API
- يُسهّل الصيانة والاختبار

### 2. Repository Pattern

- **InMemoryRepository**: abstraction فوق طبقة التخزين
- سهولة استبدال التخزين المؤقت بقاعدة بيانات لاحقاً
- فصل منطق الأعمال عن Used

### 1. Facade Pattern

- **HBnBFacade**: Unified entry point for Business Logic
- Hides internal complexity from API layer
- Simplifies maintenance and testing

### 2. Repository Pattern

- **InMemoryRepository**: Abstraction over storage layer
- Easy to replace temporary storage with database later
- Separates business logic from storage

### 3. RESTful Design

- Proper use of HTTP MethodsQLAlchemy + PostgreSQL/MySQL)
- 👤 **User Sessions**
- 🔒 **Password Hashing** (bcrypt)
- 📧 **Email Validation**
- 🖼️ **Image Upload** for places
- 🔍 **Advanced Search & Filtering**
- 📄 **Pagination**
  Coming Soon

Upcoming Features:

- 🔐 **Authentication & Authorization** (JWT)
- 💾 **Database Integration** (SQLAlchemy + PostgreSQL/MySQL)
- 👤 **User Sessions**
- 🔒 **Password Hashing** (bcrypt)
- 📧 **Email Validation**
- 🖼️ **Image Upload** for places
- 🔍 **Advanced Search & Filtering**
- 📄 **Pagination**

---

## 👥 Team](part1/README.md) - التصميم المعماري و UML

- [📄 Part 2 README](part2/README.md) - تفاصيل API والتطبيق
- [📖 Testing Guide](part2/TESTING_GUIDE.md) - دليل الاختبار الشامل

### الResources & Documentation

### Internal Documentation

- [📄 Part 1 README](part1/README.md) - Architecture Design & UML
- [📄 Part 2 README](part2/README.md) - API Details & Implementation
- [📖 Testing Guide](part2/TESTING_GUIDE.md) - Comprehensive Testing Guide

### External Resources

## 🐛 استكشاف الأخطاء (Troubleshooting)

### مشكلة: 404 Not Found

````bash
# تأكد من استخدام الـ base URL الصحيح
http://localhost:5000/api/v1/users/  ✅
http://localhost:5000/users/         ❌
```Troubleshooting

### Issue: 404 Not Found

```bash
# Make sure to use the correct base URL
http://localhost:5000/api/v1/users/  ✅
http://localhost:5000/users/         ❌
````

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

## 📄 License

This project is educational and owned by **Holberton School**.

---

## 📧 Contact

For questions and inquiries, contact the project team

</div>
