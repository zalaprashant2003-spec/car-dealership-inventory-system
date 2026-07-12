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
- Invoice & Billing Flow
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
- Vite
- React Router
- Axios
- Lucide React

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
│   ├── public/
│   ├── src/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── AuthContext.jsx
│   │   ├── api.js
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
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

- User (Roles: ADMIN, SALESPERSON, CUSTOMER)
- Vehicle

---

# 🚀 Getting Started

## 1. Clone Repository

```bash
git clone https://github.com/zalaprashant2003-spec/car-dealership-inventory-system.git
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

## 8. Start Frontend Server

```bash
cd ../frontend
npm install
npm run dev
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

This project was developed with assistance from AI tools as productivity and learning aids. All generated code was reviewed, understood, modified where necessary, tested, and verified before being included in the project.

### How AI was used

- **Backend setup (ChatGPT + Myself)**
  - Used ChatGPT to guide the initial setup of FastAPI, SQLAlchemy, Alembic, JWT authentication, and PostgreSQL.
  - Reviewed, understood, implemented, tested, and verified all generated code before using it.

- **Database schema (ChatGPT)**
  - Used ChatGPT to discuss entity relationships and model design.
  - Reviewed the suggestions, adapted them to the project requirements, and verified the final implementation.

- **Daily development (GitHub Copilot + Antigravity)**
  - Used GitHub Copilot and Antigravity primarily for boilerplate generation, code completion, and repetitive coding tasks.
  - Reviewed, modified, tested, and verified every accepted suggestion.

- **Test-Driven Development (ChatGPT + Gemini)**
  - Used ChatGPT and Gemini to discuss test cases, testing strategies, and TDD concepts.
  - Implemented the tests, validated the expected behavior, and ensured they met the project requirements.

- **UI/UX brainstorming (Gemini + Antigravity)**
  - Used Gemini and Antigravity to explore layout ideas, component organization, and design improvements.
  - Made the final UI decisions and implemented the interface myself.

- **Debugging (ChatGPT)**
  - Used ChatGPT to analyze errors, identify possible root causes, and understand debugging approaches.
  - Verified each solution locally before applying any changes.

### My Contribution

- Designed the overall project architecture and development roadmap.
- Set up the complete development environment.
- Implemented the backend and frontend features.
- Configured PostgreSQL, SQLAlchemy, Alembic, authentication, and project structure.
- Reviewed, understood, modified, tested, and verified all AI-generated code before using it.
- Debugged issues, validated functionality, and ensured the application behaved as expected.


### Reflection

AI tools helped speed up development by assisting with setup, explanations, debugging, testing strategies, and repetitive coding tasks. Rather than copying generated code directly, I reviewed every suggestion, understood how it worked, adapted it to the project's requirements, and verified the implementation through testing and local validation.

---

# 📖 Development Roadmap

- Project Setup
- PostgreSQL Configuration
- SQLAlchemy Models
- Alembic Migration
- Core CRUD APIs
- React Frontend Integration
- Role-Based Access Control
- Invoice & Billing Flow

---

# 💻 Author

**Prashant Zala**
