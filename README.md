## Project Name :
    FastAPI backend for a --Simple E-commerce System--

## Project Description :
    This is a backend API built with FastAPI for a simple e-commerce system. This project  focused on learning, how real APIs are structured: clean modules, validation, database transactions, and basic security. Handling authentication,
    products, orders, and role-based access control.

## Features :
    - User authentication using JWT
    - Role-based access (Admin / Customer)
    - Product management (Admin only)
    - Order management
    - Secure password hashing

## Tech Stack :
    - Python
    - FastAPI
    - SQLAlchemy
    - PostgreSQL
    - JWT Authentication
    - Pydantic

## Project Structure :

    Simple E-commerce System/
    │
    ├── app/
    │   ├── repositories/
    │   ├── routers/
    │   ├── services/
    │   ├── config.py
    │   ├── database.py
    │   ├── hashing.py
    │   ├── JWToken.py
    │   ├── main.py
    │   ├── models.py
    │   ├── oauth2.py
    │   └── schemas.py
    │
    ├── requirements.txt
    ├── .gitignore
    └── README.md

## Installation :
    1. Clone the repository
        git clone
        https://github.com/mosaraf-in/E-Commerce-Backend-with-FastAPI.git
    
    2. Go to project directory
        cd E-Commerce-Backend-with-FastAPI
    
    3. Create virtual environments
        python -m venv venv
    
    4. Activate virtual environment
        ---CMD---
        # Windows --> venv\Scripts\activate
        # Linux / Mac --> source venv/bin/activate
        ---powershell--
        venv\Scripts\Activate
    
    5. Install dependencies
        pip install -r requirements.txt

## Run the project :
    uvicorn app.main:app --reload



