# Testing Guide for HBnB API - Part 2

## Quick Start

### 1. Install Dependencies

```bash
cd part2
pip install -r requirements.txt
pip install pytest pytest-cov
```

### 2. Start the Server

```bash
python run.py
```

The server will start on `http://localhost:5000`

### 3. Run Tests

#### Option A: Automated Tests (pytest)

```bash
# Run all tests
pytest test_api.py -v

# Run with coverage report
pytest test_api.py -v --cov=hbnb --cov-report=html

# Run specific test class
pytest test_api.py::TestUserEndpoints -v
```

#### Option B: Manual Tests (cURL)

```bash
# Make script executable (Linux/Mac only)
chmod +x curl_tests.sh

# Run all cURL tests
bash curl_tests.sh
```

#### Option C: Individual Python Test Scripts

```bash
# Test each endpoint separately
python test_user_endpoints.py
python test_amenity_endpoints.py
python test_place_endpoints.py
python test_review_endpoints.py
```

### 4. View API Documentation

Open your browser and navigate to:

```
http://localhost:5000/api/v1/
```

This will open the interactive Swagger UI where you can:

- View all endpoints
- See request/response schemas
- Test endpoints directly in the browser
- View validation rules

---

## Test Files Overview

### Automated Testing

- **`test_api.py`** - Comprehensive pytest suite with 40+ tests
  - Tests all CRUD operations
  - Tests validation rules
  - Tests error handling
  - Tests relationships between entities

### Manual Testing Scripts

- **`curl_tests.sh`** - Bash script with 24+ cURL tests
  - Tests all endpoints
  - Includes success and error cases
  - Colored output for easy reading
  - Creates test data automatically

### Endpoint-Specific Tests

- **`test_user_endpoints.py`** - User endpoint tests
- **`test_amenity_endpoints.py`** - Amenity endpoint tests
- **`test_place_endpoints.py`** - Place endpoint tests
- **`test_review_endpoints.py`** - Review endpoint tests

### Documentation

- **`TESTING_REPORT.md`** - Comprehensive testing report
  - Test results summary
  - Validation implementation details
  - Edge cases handled
  - HTTP status codes used

---

## Test Coverage

### Endpoints Tested

✅ Users (POST, GET, PUT)  
✅ Amenities (POST, GET, PUT)  
✅ Places (POST, GET, PUT)  
✅ Reviews (POST, GET, PUT, DELETE)

### Validation Tests

✅ Email format validation  
✅ String length validation  
✅ Numeric range validation (price, rating, coordinates)  
✅ Required fields validation  
✅ Unique constraints (email, amenity name)  
✅ Relationship validation (foreign keys)

### Error Handling Tests

✅ 400 Bad Request (invalid input)  
✅ 404 Not Found (non-existent resource)  
✅ 409 Conflict (duplicate data)  
✅ 200 OK (success)  
✅ 201 Created (resource created)

---

## Expected Test Results

When you run `pytest test_api.py -v`, you should see:

```
test_api.py::TestUserEndpoints::test_create_user_success PASSED
test_api.py::TestUserEndpoints::test_create_user_duplicate_email PASSED
test_api.py::TestUserEndpoints::test_create_user_invalid_email PASSED
test_api.py::TestUserEndpoints::test_get_all_users PASSED
test_api.py::TestUserEndpoints::test_get_user_by_id PASSED
test_api.py::TestUserEndpoints::test_get_nonexistent_user PASSED
test_api.py::TestUserEndpoints::test_update_user PASSED
...
==================== 40+ passed in X.XXs ====================
```

When you run `bash curl_tests.sh`, you should see:

```
========================================
USER ENDPOINT TESTS
========================================

Test: 1. Create User (POST /api/v1/users/)
{
  "id": "...",
  "first_name": "John",
  ...
}
✓ SUCCESS

...

========================================
TEST SUMMARY
========================================
All tests completed!
```

---

## Troubleshooting

### Server Not Running

```
Error: Cannot connect to server
```

**Solution**: Start the server with `python run.py`

### Import Errors

```
ModuleNotFoundError: No module named 'flask_restx'
```

**Solution**: Install dependencies with `pip install -r requirements.txt`

### Permission Denied (curl_tests.sh)

```
bash: ./curl_tests.sh: Permission denied
```

**Solution**: Run `chmod +x curl_tests.sh` or use `bash curl_tests.sh`

---

## Additional Commands

### View Coverage Report

After running pytest with coverage:

```bash
# Open HTML coverage report
open htmlcov/index.html  # Mac
xdg-open htmlcov/index.html  # Linux
start htmlcov/index.html  # Windows
```

### Run Specific Tests

```bash
# Run only user tests
pytest test_api.py::TestUserEndpoints -v

# Run only validation tests
pytest test_api.py::TestValidations -v

# Run tests matching a pattern
pytest test_api.py -k "duplicate" -v
```

### Stop Server

Press `Ctrl+C` in the terminal where the server is running

---

## Next Steps

After running all tests successfully:

1. ✅ Review the [TESTING_REPORT.md](TESTING_REPORT.md) for detailed results
2. ✅ Check Swagger documentation at http://localhost:5000/api/v1/
3. ✅ Try interactive testing with Swagger UI
4. ✅ Move on to Part 3 (Database Integration)

---

**Happy Testing!** 🎉
