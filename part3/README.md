# HBnB Evolution - Part 3

## Enhanced Backend with Authentication and Database Integration

### Overview
This part introduces JWT authentication, role-based access control, and database integration using SQLAlchemy.

### Setup

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Run the Application
```bash
python3 run.py
```

The application will run on `http://localhost:5000`

### Configuration
The application uses a configuration system defined in `config.py`:
- **DevelopmentConfig**: Development environment with DEBUG enabled
- Configuration can be changed via `FLASK_ENV` environment variable

### Project Structure
```
part3/
├── config.py              # Configuration classes
├── run.py                 # Application entry point
├── requirements.txt       # Dependencies
└── hbnb/
    └── app/
        ├── __init__.py   # Application factory
        ├── api/          # REST API endpoints
        ├── models/       # Data models
        ├── persistence/  # Data layer
        └── services/     # Business logic
```

### Tasks Completed
- [x] Task 0: Application Factory Configuration
- [x] Task 1: User Model with Password Hashing (bcrypt)
- [x] Task 2: JWT Authentication Implementation
- [x] Task 3: Authenticated User Access Endpoints
- [x] Task 4: Administrator Access Endpoints

### Features

#### Authentication & Authorization
- **JWT-based Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Role-Based Access Control**: Admin and regular user roles
- **Protected Endpoints**: Authentication required for sensitive operations

#### Admin Privileges
- Create and manage users
- Create and modify amenities
- Bypass ownership restrictions on places and reviews
- Full system administration capabilities

#### API Endpoints
All endpoints are documented and accessible at `/api/v1/`

### Testing

#### Quick Test
```bash
# Run the PowerShell test script
.\test_admin_features.ps1

# Or use the bash script (Git Bash/WSL)
./test_admin_features.sh
```

#### Manual Testing
See [ADMIN_FEATURES.md](ADMIN_FEATURES.md) for detailed testing instructions.

### Documentation
- **ADMIN_FEATURES.md**: Comprehensive guide to admin features
- **TESTING_GUIDE.md**: General API testing guide
