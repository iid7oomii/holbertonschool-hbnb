# HBnB Evolution - Part 3

## Enhanced Backend with Authentication and Database Integration

### Overview
This part introduces JWT authentication, role-based access control, and database integration using SQLAlchemy.

### Setup

#### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

#### 2. Initialize Database
```bash
python init_db.py
```

#### 3. Run the Application
```bash
python run.py
```

The application will run on `http://localhost:8000`

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
- [x] Task 5: SQLAlchemy Repository Infrastructure
- [x] Task 6: User Entity Mapped to SQLAlchemy Model

### Features

#### Authentication & Authorization
- **JWT-based Authentication**: Secure token-based authentication
- **Password Hashing**: Bcrypt for secure password storage
- **Role-Based Access Control**: Admin and regular user roles
- **Protected Endpoints**: Authentication required for sensitive operations

#### Database Integration (Task 6)
- **SQLAlchemy ORM**: Database abstraction layer
- **SQLite Database**: Development database (development.db)
- **User Persistence**: User data stored in database with persistence
- **Repository Pattern**: SQLAlchemyRepository for User model
- **Data Integrity**: Unique constraints on email, automatic timestamps

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
- **TASK6_TESTING_GUIDE.md**: SQLAlchemy User Model testing guide with Thunder Client examples

### Database
- **development.db**: SQLite database file (created after running init_db.py)
- **User table**: Fully mapped with SQLAlchemy
- **Other entities**: Currently using InMemoryRepository (will be migrated in future tasks)
