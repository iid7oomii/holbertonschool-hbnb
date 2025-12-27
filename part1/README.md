\

# HBnB Evolution — Part 1: Technical Documentation (UML)

## Team

- ABDULAZIZ ALRASHDI
- ABDULRAHMAN ALGHAMDI
- ABDULLAH ALSALEM

## Context & Objective

This document provides the technical blueprint for **HBnB Evolution**, a simplified AirBnB-like application.
The goal of Part 1 is to document the **architecture**, **business logic design**, and **layer interactions** using **UML** (via Mermaid diagrams), so implementation in later parts is straightforward.

## Scope (Simplified Product)

The system supports four primary domains:

- **User Management**: register, update profile, delete; differentiate admins.
- **Place Management**: CRUD for places; each place belongs to an owner (user) and can be linked to amenities.
- **Review Management**: CRUD reviews; reviews are created by users for places.
- **Amenity Management**: CRUD amenities; amenities can be associated with places.

## Business Rules & Requirements

### Shared / Cross-cutting

- Each object has a **unique ID**.
- For audit reasons, each entity stores **creation** and **update** timestamps.
- Persistence is required but the concrete database and its implementation are planned for **Part 3**.

### User

- Attributes: first name, last name, email, password, is_admin.
- Operations: register, update, delete.
- Email must be unique.

### Place

- Attributes: title, description, price, latitude, longitude.
- Belongs to an **owner** (User).
- Has a list of **amenities**.
- Operations: create, update, delete, list.

### Review

- Associated with a **place** and a **user**.
- Attributes: rating, comment.
- Operations: create, update, delete, list by place.

### Amenity

- Attributes: name, description.
- Operations: create, update, delete, list.

## Architecture Overview (Layered + Facade)

The application follows a **3-layer architecture**:

1. **Presentation Layer**

   - API / controllers / routes (HTTP endpoints).
   - Validates request format and authentication context.
   - Delegates to a single entry-point: a **Facade**.

2. **Business Logic Layer**

   - Domain entities (User, Place, Review, Amenity).
   - Use-cases / services that enforce business rules.
   - A **Facade** orchestrates use-cases and hides internal complexity from the API.

3. **Persistence Layer**
   - Repository interfaces and implementations.
   - Handles storage/retrieval (DB specifics deferred to Part 3).

### Why Facade?

- Provides a **stable API** for the Presentation layer.
- Centralizes orchestration and cross-cutting concerns (transactions, validation orchestration, etc.).
- Keeps controllers thin and avoids coupling the API to internal service/repository details.

---

## 1) High-Level Package Diagram (3 Layers + Facade)

```mermaid
flowchart TB
  %% High-level packages (layered) + Facade communication

  subgraph Presentation[Presentation Layer]
    API[API / Controllers]
  end

  subgraph Business[Business Logic Layer]
    FACADE[HBnBFacade]
    SVC[Use-Case Services]
    DOM[Domain Models]
  end

  subgraph Persistence[Persistence Layer]
    REPO[Repository Interfaces]
    DB[(Database<br/>(Part 3))]
  end

  API -->|calls| FACADE
  FACADE -->|orchestrates| SVC
  SVC -->|uses| DOM
  SVC -->|CRUD via| REPO
  REPO -->|persists| DB
```

---

## 2) Detailed Class Diagram (Business Logic Layer)

Notes:

- All entities inherit audit fields: `id`, `created_at`, `updated_at`.
- `Place` has a many-to-many relationship with `Amenity`.
- `Review` is associated to exactly one `User` and one `Place`.

```mermaid
classDiagram
	direction LR

	class BaseEntity {
		+UUID id
		+datetime created_at
		+datetime updated_at
	}

	class User {
		+string first_name
		+string last_name
		+string email
		+string password_hash
		+bool is_admin
		+register()
		+update_profile()
		+delete()
	}

	class Place {
		+string title
		+string description
		+decimal price
		+float latitude
		+float longitude
		+create()
		+update()
		+delete()
	}

	class Review {
		+int rating
		+string comment
		+create()
		+update()
		+delete()
	}

	class Amenity {
		+string name
		+string description
		+create()
		+update()
		+delete()
	}

	BaseEntity <|-- User
	BaseEntity <|-- Place
	BaseEntity <|-- Review
	BaseEntity <|-- Amenity

	%% Relationships
	User "1" --> "0..*" Place : owns
	Place "1" --> "0..*" Review : has
	User "1" --> "0..*" Review : writes

	%% Many-to-many between Place and Amenity
	Place "0..*" -- "0..*" Amenity : amenities

	%% Facade + services + repositories (still part of business logic documentation)
	class HBnBFacade {
		+register_user(data)
		+update_user(user_id, data)
		+delete_user(user_id)
		+create_place(owner_id, data)
		+update_place(place_id, data)
		+delete_place(place_id)
		+list_places()
		+submit_review(user_id, place_id, data)
		+list_reviews_by_place(place_id)
		+create_amenity(data)
		+update_amenity(amenity_id, data)
		+delete_amenity(amenity_id)
		+list_amenities()
	}

	class UserService {
		+register(data)
		+update(user_id, data)
		+delete(user_id)
	}

	class PlaceService {
		+create(owner_id, data)
		+update(place_id, data)
		+delete(place_id)
		+list()
	}

	class ReviewService {
		+create(user_id, place_id, data)
		+update(review_id, data)
		+delete(review_id)
		+list_by_place(place_id)
	}

	class AmenityService {
		+create(data)
		+update(amenity_id, data)
		+delete(amenity_id)
		+list()
	}

	class IUserRepository {
		<<interface>>
		+create(User)
		+get_by_id(user_id)
		+get_by_email(email)
		+update(User)
		+delete(user_id)
	}

	class IPlaceRepository {
		<<interface>>
		+create(Place)
		+get_by_id(place_id)
		+list()
		+update(Place)
		+delete(place_id)
	}

	class IReviewRepository {
		<<interface>>
		+create(Review)
		+get_by_id(review_id)
		+list_by_place(place_id)
		+update(Review)
		+delete(review_id)
	}

	class IAmenityRepository {
		<<interface>>
		+create(Amenity)
		+get_by_id(amenity_id)
		+list()
		+update(Amenity)
		+delete(amenity_id)
	}

	HBnBFacade --> UserService
	HBnBFacade --> PlaceService
	HBnBFacade --> ReviewService
	HBnBFacade --> AmenityService

	UserService --> IUserRepository
	PlaceService --> IPlaceRepository
	ReviewService --> IReviewRepository
	AmenityService --> IAmenityRepository
```

---

## 3) Sequence Diagrams (API Calls)

Legend:

- Presentation: API / Controller
- Business: Facade + Services
- Persistence: Repositories + DB

### 3.1 User Registration

```mermaid
sequenceDiagram
	autonumber
	participant Client
	participant API as Presentation: API
	participant Facade as Business: HBnBFacade
	participant UserSvc as Business: UserService
	participant UserRepo as Persistence: IUserRepository
	participant DB as Persistence: Database

	Client->>API: POST /users (first,last,email,password)
	API->>Facade: register_user(data)
	Facade->>UserSvc: register(data)
	UserSvc->>UserRepo: get_by_email(email)
	UserRepo->>DB: SELECT user by email
	DB-->>UserRepo: result
	alt email already exists
		UserRepo-->>UserSvc: user found
		UserSvc-->>Facade: error (duplicate email)
		Facade-->>API: error
		API-->>Client: 409 Conflict
	else email available
		UserSvc->>UserRepo: create(User)
		UserRepo->>DB: INSERT user
		DB-->>UserRepo: new id
		UserRepo-->>UserSvc: created
		UserSvc-->>Facade: user DTO
		Facade-->>API: user DTO
		API-->>Client: 201 Created
	end
```

### 3.2 Place Creation

```mermaid
sequenceDiagram
	autonumber
	participant Client
	participant API as Presentation: API
	participant Facade as Business: HBnBFacade
	participant PlaceSvc as Business: PlaceService
	participant PlaceRepo as Persistence: IPlaceRepository
	participant AmenityRepo as Persistence: IAmenityRepository
	participant DB as Persistence: Database

	Client->>API: POST /places (owner_id, title, price, lat, lon, amenities[])
	API->>Facade: create_place(owner_id, data)
	Facade->>PlaceSvc: create(owner_id, data)

	Note over PlaceSvc: Validate price, latitude/longitude ranges
	alt amenities provided
		PlaceSvc->>AmenityRepo: validate amenities exist (ids)
		AmenityRepo->>DB: SELECT amenities by ids
		DB-->>AmenityRepo: found list
		AmenityRepo-->>PlaceSvc: ok / missing
	end

	PlaceSvc->>PlaceRepo: create(Place)
	PlaceRepo->>DB: INSERT place + link amenities
	DB-->>PlaceRepo: new place id
	PlaceRepo-->>PlaceSvc: created
	PlaceSvc-->>Facade: place DTO
	Facade-->>API: place DTO
	API-->>Client: 201 Created
```

### 3.3 Review Submission

```mermaid
sequenceDiagram
	autonumber
	participant Client
	participant API as Presentation: API
	participant Facade as Business: HBnBFacade
	participant ReviewSvc as Business: ReviewService
	participant PlaceRepo as Persistence: IPlaceRepository
	participant ReviewRepo as Persistence: IReviewRepository
	participant DB as Persistence: Database

	Client->>API: POST /places/{place_id}/reviews (user_id, rating, comment)
	API->>Facade: submit_review(user_id, place_id, data)
	Facade->>ReviewSvc: create(user_id, place_id, data)
	ReviewSvc->>PlaceRepo: get_by_id(place_id)
	PlaceRepo->>DB: SELECT place
	DB-->>PlaceRepo: result
	alt place not found
		PlaceRepo-->>ReviewSvc: null
		ReviewSvc-->>Facade: error (place not found)
		Facade-->>API: error
		API-->>Client: 404 Not Found
	else place exists
		Note over ReviewSvc: Validate rating range (e.g., 1..5)
		ReviewSvc->>ReviewRepo: create(Review)
		ReviewRepo->>DB: INSERT review
		DB-->>ReviewRepo: new review id
		ReviewRepo-->>ReviewSvc: created
		ReviewSvc-->>Facade: review DTO
		Facade-->>API: review DTO
		API-->>Client: 201 Created
	end
```

### 3.4 Fetch Places List

```mermaid
sequenceDiagram
	autonumber
	participant Client
	participant API as Presentation: API
	participant Facade as Business: HBnBFacade
	participant PlaceSvc as Business: PlaceService
	participant PlaceRepo as Persistence: IPlaceRepository
	participant DB as Persistence: Database

	Client->>API: GET /places
	API->>Facade: list_places()
	Facade->>PlaceSvc: list()
	PlaceSvc->>PlaceRepo: list()
	PlaceRepo->>DB: SELECT places
	DB-->>PlaceRepo: rows
	PlaceRepo-->>PlaceSvc: place list
	PlaceSvc-->>Facade: place DTO list
	Facade-->>API: place DTO list
	API-->>Client: 200 OK
```

---

## Documentation Notes / Implementation Guidance

- **Validation** belongs primarily to the Business Logic layer (services), while the Presentation layer handles request-shape validation and authentication context.
- Audit fields (`created_at`, `updated_at`) are set/updated on create/update operations.
- Repository interfaces decouple business logic from storage technology; concrete DB work is deferred to Part 3.

## Mermaid Rendering

If diagrams do not render in your viewer, ensure Mermaid support is enabled in Markdown preview (VS Code Mermaid extensions may help), or paste the Mermaid blocks into https://mermaid.live.
