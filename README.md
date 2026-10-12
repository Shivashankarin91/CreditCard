# Credit Card Payment System

A full-stack junior developer project for managing user authentication, saved payment cards, and payment transactions using **Django**, **FastAPI**, and **MySQL**.

> **Project status:** Development project. Verify each endpoint and security requirement locally before describing it as production-ready.

## Table of Contents

- [Overview](#overview)
- [Technology Stack](#technology-stack)
- [Modules and Features](#modules-and-features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Project Structure](#project-structure)
- [Setup and Installation](#setup-and-installation)
- [Environment Configuration](#environment-configuration)
- [Database Migrations](#database-migrations)
- [Run the Application](#run-the-application)
- [API Testing](#api-testing)
- [Security Practices](#security-practices)
- [Troubleshooting](#troubleshooting)
- [Future Improvements](#future-improvements)

## Overview

The Credit Card Payment System demonstrates how separate backend services can work together:

- **Django** handles user authentication, card management, and administrative functionality.
- **FastAPI** provides transaction-related API endpoints.
- **MySQL** stores application data.
- **JWT authentication** protects endpoints that require a signed-in user.

The exact endpoint paths, request fields, and response formats depend on the implementation in this repository. Confirm them in the project's URL configuration and API documentation.

## Technology Stack

- Python
- Django
- Django REST Framework (if configured in the project)
- FastAPI
- MySQL
- JSON Web Tokens (JWT)
- Uvicorn (for running FastAPI)
- Virtual environments (`venv`)

## Modules and Features

### Module 1 — User Authentication (Django)

- User registration
- User login using JWT authentication
- Logout/token invalidation, if configured
- Password hashing using Django's password-hashing framework
- Protected routes

### Module 2 — Card Management (Django)

- Add a saved card
- View saved cards
- Delete a saved card
- Associate saved cards with their owner

Only expose the minimum card information needed by the application. Do not store CVV/CVC.

### Module 3/4 — Transactions (FastAPI and Django integration)

- Create a transaction
- Track transaction status
- View transaction history, if implemented
- Validate transaction amounts and request data
- Keep transaction ownership and authorization checks in place

**Integration note:** If Django and FastAPI write to different database tables, their transaction records will not automatically appear in one another's history. Confirm that both services use the intended schema and transaction model.

### Module 5 — Admin Panel

- Django admin interface
- Administrative management of registered models
- Daily transaction summary, if configured
- Admin-only access to administrative pages

### Module 6 — Database (MySQL)

The application may use tables for:

- Users (the actual table depends on the configured Django user model)
- Saved cards
- Transactions
- Django admin activity logs
- Application-specific admin logs, if implemented

Django's built-in admin log table is normally `django_admin_log`. Actual application table names depend on the model names and any explicit `db_table` settings.

### Module 8 — Security Rules

- Do not store CVV/CVC
- Hash passwords; never store plain-text passwords
- Verify JWT signatures and expiration
- Validate and constrain user input
- Use Django ORM or parameterized SQL to help prevent SQL injection
- Restrict records and actions to authorized users
- Keep secrets out of source control and logs

## Architecture

```text
Client / API testing tool
        |
        +---- Django backend (default: http://127.0.0.1:8000)
        |       +-- Registration and login
        |       +-- Saved card management
        |       +-- Django admin
        |
        +---- FastAPI backend (default: http://127.0.0.1:8001)
                +-- Transaction API
                        |
                        v
                  MySQL database
```

This is a conceptual overview. Verify the actual data flow and whether both backends use the same tables before relying on cross-service transaction history.

## Prerequisites

Install or prepare:

- Python version supported by the installed Django and FastAPI dependencies
- MySQL Server
- Git (optional)
- Postman or another HTTP client (optional)

Check Python and pip:

```powershell
python --version
python -m pip --version
```

## Project Structure

Your repository may differ. A typical structure based on this project is:

```text
credit_card_payment_system/
├── django_backend/
│   ├── manage.py
│   ├── config/
│   ├── users/
│   ├── cards/
│   ├── transactions/
│   ├── transaction_management/
│   ├── admin_logs/
│   └── venv/
└── fastapi_backend/
    ├── main.py
    └── ...
```

Keep your actual folder names and app names if they differ. Do not commit virtual environments, local database dumps, or secret configuration files.

## Setup and Installation

### 1. Clone or open the project

If using Git:

```powershell
git clone <repository-url>
cd credit_card_payment_system
```

If you already have the project locally, open its existing folder instead.

### 2. Configure the Django environment

Open PowerShell and enter the Django directory:

```powershell
cd django_backend
```

Create and activate a virtual environment if one does not already exist:

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

Install the project's dependencies if a `requirements.txt` exists:

```powershell
python -m pip install -r requirements.txt
```

If there is no dependency file, install the packages listed in the project documentation and source imports. Avoid guessing versions for an existing working environment.

### 3. Configure MySQL

Create a MySQL database named `credit_card_db` if it does not already exist:

```sql
CREATE DATABASE credit_card_db
  CHARACTER SET utf8mb4
  COLLATE utf8mb4_unicode_ci;
```

Configure Django's `DATABASES` setting with the database name, host, port, username, and password appropriate for your local MySQL installation.

Typical local connection values used during development:

- Database: `credit_card_db`
- Host: `localhost`
- Port: `3306`

Use a dedicated database user with only the permissions the application needs. Do not put real credentials in this README or commit them to source control.

### 4. Configure environment variables

Use a local `.env` file or environment variables for secrets if your project supports them. For example, the variable names might look like:

```dotenv
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DB_NAME=credit_card_db
DB_USER=your_local_database_user
DB_PASSWORD=your_local_database_password
DB_HOST=localhost
DB_PORT=3306
```

These are example names only; the application must explicitly load them. Match the variable names to the existing settings code. Do not commit `.env` files.

If FastAPI verifies Django-issued JWTs, configure both services to use compatible token verification settings, including the expected signing algorithm and signing key or public key. Do not hard-code or expose production secrets. Prefer a well-managed secret store in deployed environments.

### 5. Apply Django migrations

From `django_backend`, run:

```powershell
python manage.py check
python manage.py showmigrations
python manage.py makemigrations
python manage.py migrate
```

Review generated migrations before applying them. Do not delete database tables or use `--fake` to work around migration errors without first diagnosing the cause.

Create an administrator account if needed:

```powershell
python manage.py createsuperuser
```

## Run the Application

Open **two separate PowerShell terminals**.

### Terminal 1 — Django

```powershell
cd "path\to\credit_card_payment_system\django_backend"
.\venv\Scripts\Activate.ps1
python manage.py runserver 127.0.0.1:8000
```

Django development server: <http://127.0.0.1:8000/>

Django admin (if enabled): <http://127.0.0.1:8000/admin/>

### Terminal 2 — FastAPI

Use the actual FastAPI folder and Python environment in your repository. If `main.py` contains the FastAPI application object named `app`, the command is typically:

```powershell
cd "path\to\credit_card_payment_system\fastapi_backend"
python -m uvicorn main:app --reload --host 127.0.0.1 --port 8001
```

FastAPI base URL: <http://127.0.0.1:8001/>

Interactive API documentation (when enabled): <http://127.0.0.1:8001/docs>

If the FastAPI app is in a different module or the object has another name, adjust `main:app` accordingly. The reload option is intended for local development, not production.

## API Testing

Use Postman or the interactive FastAPI documentation to test the routes actually defined in your project.

| Operation | Method | Example path |
|---|---|---|
| Register | POST | `/api/auth/register/` |
| Login | POST | Check Django URL configuration |
| Add saved card | POST | Check card URL configuration |
| List saved cards | GET | Check card URL configuration |
| Delete saved card | DELETE | Check card URL configuration |
| Create transaction | POST | `/api/transactions/` |
| Transaction history | GET | Check transaction URL configuration |

Paths above are examples based on the development workflow. Confirm exact routes, trailing slashes, payload fields, and response formats in your code.

### Suggested test sequence

1. Register a new test user.
2. Log in and obtain a JWT access token.
3. Call a protected endpoint without a token; it should reject the request.
4. Call the same endpoint with a valid token; it should return only data the user is authorized to access.
5. Add a test card using non-real test data.
6. List saved cards and verify sensitive fields are not returned.
7. Delete the test card and verify it is no longer listed.
8. Create a test transaction and verify the response and stored status.
9. Send invalid inputs, such as a negative amount or malformed field, and confirm the API rejects them.
10. Check that one user cannot access another user's cards or transactions.

Do not test with real card details or production credentials.

## Security Practices

### CVV/CVC

- Never persist CVV/CVC in a database, log, cache, or API response.
- Do not retain CVV/CVC after authorization.
- Prefer a payment provider's hosted fields or tokenization instead of handling raw card data directly.

### Passwords

- Use Django's password APIs, such as `create_user()` and `set_password()`.
- Verify passwords using Django's authentication framework or `check_password()`.
- Never save plain-text passwords or attempt to decrypt password hashes.

### JWT

- Verify the token signature and expiration.
- Restrict accepted signing algorithms; do not trust the algorithm specified by an unverified token.
- Keep signing keys secret and consistent across services that verify the same tokens.
- Protect sensitive endpoints and enforce per-user authorization.
- Use short-lived access tokens and a safe refresh/revocation strategy where appropriate.

### Input validation

- Validate required fields, types, lengths, and allowed values.
- Validate transaction amounts as positive, bounded decimal values.
- Validate expiry information and supported card metadata.
- Return safe error messages without leaking secrets or internal stack traces.

### SQL injection

- Prefer Django ORM queries and SQLAlchemy expressions.
- Use parameterized queries when raw SQL is necessary.
- Never concatenate untrusted input into SQL statements.
- Use a database account with least-privilege permissions.

### General deployment security

- Set `DEBUG = False` in production and configure `ALLOWED_HOSTS`.
- Use HTTPS in deployed environments.
- Keep secrets and tokens out of logs and source control.
- Apply supported security updates and back up the database securely.
- Do not expose Django's or Uvicorn's development servers directly to the public internet.

## Troubleshooting

### Registration returns `401 Unauthorized`

- Inspect the response body to determine the reason.
- Confirm the URL resolves to the expected registration view.
- If registration is intended to be public, check its Django REST Framework permission settings. `AllowAny` is commonly used for public registration, but confirm the view and any custom authentication checks before changing permissions.
- Check whether a global authentication/permission policy or custom middleware is rejecting the request.
- Do not disable authentication for the entire application to fix one endpoint.

### MySQL reports that a table does not exist

- Confirm Django is connected to the intended database.
- Run `python manage.py showmigrations`.
- Review `python manage.py migrate --plan`.
- Generate and apply the correct migration for the app.
- Do not manually create duplicate tables or drop existing tables as a first fix.

### FastAPI cannot verify a Django JWT

- Check that the token was issued by the expected service.
- Compare the configured signing key or public key, algorithm, issuer, and audience where applicable.
- Check token expiration and the expected token type.
- Never paste a real JWT or signing key into an issue or public repository.

### A transaction is missing from a Django report

- Confirm which database table each service writes to.
- Check whether the Django report queries `transactions_transaction` while FastAPI writes to a separate table.
- Align the schema or implement an intentional integration path rather than assuming separate tables synchronize automatically.

## Future Improvements

- Add automated unit and integration tests.
- Add API schema and endpoint documentation.
- Integrate a compliant payment gateway in test/sandbox mode.
- Add transaction reconciliation and audit trails without storing sensitive authentication data.
- Add rate limiting and abuse protection to authentication endpoints.
- Add CI checks, structured monitoring, and production deployment configuration.

## Disclaimer

This project is intended for learning and demonstration. It is not a certified payment processing system. Before handling real payments or cardholder data, use a compliant payment provider and obtain the necessary security and compliance review.
