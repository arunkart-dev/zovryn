# Finance Data Processing and Access Control Backend

A production-ready backend for a finance dashboard system built with **Django REST Framework** and **JWT authentication**. The system supports financial record management, role-based access control, and summary-level analytics — designed to be clean, maintainable, and logically structured.

---

## Table of Contents

- [Overview](#overview)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Features](#features)
- [Role-Based Access Control](#role-based-access-control)
- [API Endpoints](#api-endpoints)
- [Setup and Installation](#setup-and-installation)
- [Testing the API](#testing-the-api)
- [Design Decisions](#design-decisions)
- [Assumptions](#assumptions)

---

## Overview

This backend powers a finance dashboard where different users interact with financial data based on their assigned role. It supports three roles — **Viewer**, **Analyst**, and **Admin** — each with clearly defined permissions enforced at the API level.

Key capabilities:
- JWT-based authentication with role embedded in the token
- Full CRUD for financial records with filtering, search, and pagination
- Dashboard analytics: totals, category breakdowns, and monthly trends
- Role-based access control enforced on every endpoint
- Clean modular app structure with separation of concerns

---

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python 3.13 |
| Framework | Django 5.x + Django REST Framework |
| Authentication | JWT via `djangorestframework-simplejwt` |
| Database | SQLite (development) |
| Filtering | `django-filter` |
| Pagination | DRF `PageNumberPagination` |

---

## Project Structure

```
finance/
├── manage.py
├── finance_backend/
│   ├── settings.py
│   └── urls.py
└── django_apps/
    ├── users/          # User model, registration, JWT login
    ├── records/        # Financial records CRUD, filtering, pagination
    ├── dashboard/      # Analytics and summary APIs
    └── roles/          # Permission classes for RBAC
```

Each app is self-contained with its own `models.py`, `serializers.py`, `views.py`, and `urls.py`.

---

## Features

### 1. User and Role Management
- Register users with a role (`viewer`, `analyst`, `admin`)
- JWT login with role embedded in the access token payload
- Admin can list, update, and delete users
- Users can view their own profile via `/api/users/me/`
- `is_active` flag to enable or disable accounts

### 2. Financial Records Management
- Full CRUD — create, read, update, delete financial records
- Each record stores: `amount`, `type` (income/expense), `category`, `date`, `notes`
- Records are linked to the user who owns them
- Admins see all records; viewers and analysts see only their own

### 3. Filtering, Search, and Pagination
- Filter records by `type`, `category`, `date`
- Search records by `notes` or `category`
- Order records by `amount` or `date`
- Paginated responses — 5 records per page, maximum 50

### 4. Dashboard Analytics
- Total income, total expense, net balance
- Category-wise income and expense breakdown
- Monthly trends (income vs expense per month)
- All computed dynamically using Django ORM aggregation

### 5. Role-Based Access Control
- Custom permission classes in `django_apps/roles/permissions.py`
- Every view explicitly declares its required permission
- Clean, readable access control with no ambiguity

### 6. Validation and Error Handling
- Serializer-level validation (e.g. amount must be greater than 0)
- Meaningful error messages with correct HTTP status codes
- 401 for unauthenticated, 403 for unauthorized, 400 for bad input

---

## Role-Based Access Control

| Endpoint | Viewer | Analyst | Admin |
|---|---|---|---|
| `POST /api/users/login/` | ✅ | ✅ | ✅ |
| `GET /api/users/me/` | ✅ | ✅ | ✅ |
| `GET /api/records/` | ✅ | ✅ | ✅ |
| `POST /api/records/` | ❌ 403 | ❌ 403 | ✅ |
| `PUT /api/records/<id>/` | ❌ 403 | ❌ 403 | ✅ |
| `DELETE /api/records/<id>/` | ❌ 403 | ❌ 403 | ✅ |
| `GET /api/dashboard/analytics/` | ❌ 403 | ✅ | ✅ |
| `GET /api/users/` | ❌ 403 | ❌ 403 | ✅ |

---

## API Endpoints

### Auth

| Method | Endpoint | Description | Access |
|---|---|---|---|
| POST | `/api/users/` | Register a new user | Public |
| POST | `/api/users/login/` | Login, returns JWT tokens | Public |
| GET | `/api/users/me/` | Get current user profile | Any authenticated |
| POST | `/api/auth/refresh/` | Refresh access token | Any authenticated |

### Users (Admin only)

| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/users/` | List all users |
| GET | `/api/users/<id>/` | Get user by ID |
| PUT | `/api/users/<id>/` | Update user |
| DELETE | `/api/users/<id>/` | Delete user |

### Financial Records

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/records/` | List records | Viewer, Analyst, Admin |
| POST | `/api/records/` | Create a record | Admin only |
| GET | `/api/records/<id>/` | Get record by ID | Viewer, Analyst, Admin |
| PUT | `/api/records/<id>/` | Update a record | Admin only |
| DELETE | `/api/records/<id>/` | Delete a record | Admin only |

**Query parameters for filtering:**
```
/api/records/?type=income
/api/records/?category=salary
/api/records/?date=2025-01-01
/api/records/?search=salary
/api/records/?ordering=-amount
/api/records/?page=2&page_size=10
```

### Dashboard

| Method | Endpoint | Description | Access |
|---|---|---|---|
| GET | `/api/dashboard/analytics/` | Summary analytics | Analyst, Admin |

**Response includes:**
- `totals` — total income, total expense, net balance
- `category_income` — income grouped by category
- `category_expense` — expense grouped by category
- `monthly` — month-wise income and expense breakdown

---

## Setup and Installation

### Prerequisites
- Python 3.10+
- pip

### 1. Clone the repository
```bash
git clone https://github.com/arunkart-dev/zovryn.git
cd zovryn
```

### 2. Create and activate a virtual environment
```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Mac/Linux
source venv/bin/activate
```

### 3. Install dependencies
```bash
pip install django djangorestframework djangorestframework-simplejwt django-filter
```

### 4. Run migrations
```bash
python manage.py migrate
```

### 5. Start the server
```bash
python manage.py runserver
```

The API will be available at `http://127.0.0.1:8000/`

---

## Testing the API

Use **Postman** or any API client.

### Step 1 — Register a user
```
POST http://127.0.0.1:8000/api/users/
Content-Type: application/json

{
    "username": "alice",
    "password": "pass1234",
    "role": "viewer"
}
```

### Step 2 — Login
```
POST http://127.0.0.1:8000/api/users/login/
Content-Type: application/json

{
    "username": "alice",
    "password": "pass1234"
}
```

Response:
```json
{
    "access": "<access_token>",
    "refresh": "<refresh_token>",
    "role": "viewer",
    "username": "alice"
}
```

### Step 3 — Use the token
In Postman, go to **Authorization → Bearer Token** and paste the `access` token.

```
GET http://127.0.0.1:8000/api/records/
Authorization: Bearer <access_token>
```

---

## Design Decisions

**JWT over session auth** — JWT is stateless; the user's role travels inside the token itself, so no database lookup is needed on every request to check permissions.

**Custom permission classes** — Instead of Django's built-in permission system, custom classes (`IsViewerOrAbove`, `IsAnalystOrAdmin`, `IsAdminUser`) are used. Each view explicitly declares its own permission, making access control transparent and easy to audit.

**Queryset-level data isolation** — Viewers and analysts only see their own records. This is enforced in `get_queryset()` rather than the serializer, which is more reliable and consistent across all actions (list, retrieve, etc.).

**Dynamic analytics** — Dashboard data is computed on the fly using Django ORM aggregation (`Sum`, `TruncMonth`). This avoids data duplication and always reflects the current state of the database.

**Modular app structure** — Each concern lives in its own app (`users`, `records`, `dashboard`, `roles`). This makes the codebase easy to navigate, test, and extend independently.

**SQLite for development** — Simple to set up with zero configuration. Easily switchable to PostgreSQL for production by changing the `DATABASES` setting in `settings.py`.

---

## Assumptions

1. Role is assigned at registration time by providing the `role` field.
2. Viewers and analysts can only see and interact with their own records.
3. Admins have visibility over all records across all users.
4. Access token lifetime is 60 minutes; refresh token lifetime is 7 days.
5. The `user` field on a record must be provided explicitly when an admin creates a record on behalf of another user.
6. Dashboard analytics are scoped to the requesting user (each user sees their own financial summary).
