# 🏥 ClinicOS

> A modern, scalable Hospital Management System built with **FastAPI**, **PostgreSQL**, and **Clean Architecture**.

---

## 📖 Overview

ClinicOS is a production-style Hospital Management System being built from scratch using modern backend engineering practices.

The goal of this project is to build software that is:

- Scalable
- Maintainable
- Modular
- Production Ready

Instead of putting everything into one file, ClinicOS follows a layered architecture similar to enterprise applications.

---

## 🚀 Tech Stack

| Technology | Purpose |
|------------|---------|
| FastAPI    | REST API Framework |
| PostgreSQL | Database |
| SQLAlchemy | ORM |
| Alembic    | Database Migrations |
| Pydantic   | Validation |
| Poetry     | Dependency Management |
| Uvicorn    | ASGI Server |
| Git&GitHub | Version Control |

---

## 🏗 Architecture

```
                Client
                   │
                   ▼
              FastAPI API
                   │
                   ▼
            Service Layer
          (Business Logic)
                   │
                   ▼
          Repository Layer
          (Database Access)
                   │
                   ▼
             PostgreSQL
```

---

## 📂 Project Structure

```
backend/
│
├── alembic/
├── app/
│   ├── db/
│   ├── enums/
│   ├── models/
│   └── modules/
│       ├── patients/
│       │   ├── api.py
│       │   ├── models.py
│       │   ├── repository.py
│       │   ├── schemas.py
│       │   ├── service.py
│       │   └── exceptions.py
│       │
│       ├── doctors/
│       ├── appointments/
│       ├── billing/
│       └── laboratory/
│
└── tests/
```

---

## ✅ Features Completed

### Infrastructure

- [x] FastAPI Setup
- [x] PostgreSQL Integration
- [x] SQLAlchemy ORM
- [x] Alembic Migrations
- [x] Environment Configuration

### Patient Module

- [x] Patient Model
- [x] Patient Schema
- [x] Create Patient API
- [x] List Patients API
- [x] Automatic Patient Code Generation
- [x] UUID Primary Keys

---

## 🚧 Features In Progress

- [ ] Get Patient by ID
- [ ] Update Patient
- [ ] Soft Delete Patient
- [ ] Pagination
- [ ] Search Patients
- [ ] Global Exception Handling
- [ ] Authentication
- [ ] Doctor Module
- [ ] Appointment Module
- [ ] Billing Module
- [ ] Laboratory Module

---

## ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/Atuliya007/ClinicOS.git
```

Go into backend

```bash
cd backend
```

Install dependencies

```bash
poetry install
```

Activate virtual environment

```bash
poetry shell
```

Run migrations

```bash
py -m alembic upgrade head
```

Start server

```bash
py -m uvicorn app.main:app --reload
```

---

## 📚 API Documentation

Swagger UI

```
http://127.0.0.1:8000/docs
```

---

## 🎯 Project Goals

- Learn Backend Engineering
- Learn Clean Architecture
- Build a Production Ready Hospital ERP
- Deploy to Cloud
- Build Authentication & Authorization
- Dockerize the Application
- CI/CD Pipeline
- Automated Testing

---

## 👨‍💻 Author

**Atuliya Bansal**

Built with ❤️ while learning Backend Engineering.