# 🚗 Car Dealership Inventory System

A production-style Car Dealership Inventory System built using **FastAPI**, **PostgreSQL**, **SQLAlchemy 2.0**, **Alembic**, **JWT Authentication**, **React**, and **Test-Driven Development (TDD)**.

This project is being developed using a clean layered architecture following industry best practices and SOLID principles.

---

### 📅 Planned

- User Registration
- User Login
- JWT Authentication
- Vehicle CRUD API
- Inventory Management
- Role-Based Authorization
- React Frontend
- Unit & Integration Testing

---

# 🛠 Tech Stack

## Backend

- Python 3.12
- FastAPI
- PostgreSQL
- SQLAlchemy 2.0
- Alembic
- Pydantic
- JWT Authentication
- Passlib
- python-dotenv
- Pytest

## Frontend

- React
- React Router
- Axios

---

# 📁 Project Structure

```text
car-dealership-inventory-system/
│
├── backend/
│   ├── alembic/
│   ├── app/
│   │   ├── api/
│   │   ├── core/
│   │   ├── models/
│   │   ├── repositories/
│   │   ├── schemas/
│   │   ├── services/
│   │   ├── dependencies.py
│   │   └── main.py
│   │
│   ├── tests/
│   ├── requirements.txt
│   ├── alembic.ini
│   └── .env.example
│
├── frontend/
│
├── .gitignore
└── README.md
```

---

# 🏗 Architecture

The backend follows a layered architecture.

```
Client
   │
   ▼
FastAPI Router
   │
   ▼
Service Layer
   │
   ▼
Repository Layer
   │
   ▼
SQLAlchemy ORM
   │
   ▼
PostgreSQL
```

---

# 🗄 Database

Current entities:

- User
- Vehicle

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/<your-username>/<repository-name>.git
```

---

## 2. Navigate to Backend

```bash
cd backend
```

---

## 3. Create Virtual Environment

### Windows

```bash
python -m venv .venv
.venv\Scripts\activate
```

### Linux / macOS

```bash
python3 -m venv .venv
source .venv/bin/activate
```

---

## 4. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 5. Configure Environment Variables

Create a `.env` file using `.env.example`.

---

## 6. Run Database Migrations

```bash
alembic upgrade head
```

---

## 7. Start Development Server

```bash
uvicorn app.main:app --reload
```

---

# 🧪 Testing

Testing will be implemented using **Pytest** following the **Test-Driven Development (TDD)** approach.

To run tests:

```bash
pytest
```

---

# 🤖 My AI Usage

This project was developed with assistance from **ChatGPT (OpenAI)**.

### How AI was used

- Assisted in configuring FastAPI, SQLAlchemy 2.0, Alembic, and PostgreSQL.
- Helped generate initial boilerplate code for models and configuration.
- Explained SQLAlchemy, Alembic migrations, and project setup.
- Assisted in debugging configuration and migration issues.

### What I implemented

- Planned the overall project architecture.
- Set up the development environment.
- Created and organized the project structure.
- Configured PostgreSQL and Alembic.
- Wrote, reviewed, tested, and modified the generated code.
- Debugged and verified the application locally.

### Reflection

AI greatly sped up the initial setup and helped clarify backend concepts and best practices. I went through each generated solution, made adjustments when needed, and used the explanations to gain a better understanding of the implementation instead of just copying code.

---

# 📖 Development Roadmap

- Project Setup
- PostgreSQL Configuration
- SQLAlchemy Models
- Alembic Migration

---

# 👨‍💻 Author

**Prashant Zala**
