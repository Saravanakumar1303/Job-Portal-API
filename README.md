# JobPortal API – Django REST Framework

JobPortal API is a backend REST API for a simple job recruitment platform.

The application connects two types of users:

- Job Seekers who create profiles, upload resumes and apply for jobs
- Recruiters who create and manage job postings and review applications

The main purpose of this project was to build a backend system with authentication, role-based access control, file uploads, job management and an application workflow using Django REST Framework.

The project uses PostgreSQL for data storage and Docker for containerized development.

---

# Project Overview

A job portal usually has two different types of users with different responsibilities.

A Job Seeker should be able to:

- Create an account
- Manage their profile
- Upload a resume
- View available jobs
- Apply for jobs
- Track their applications

A Recruiter should be able to:

- Create an account
- Create job postings
- Update their own job postings
- Delete their own job postings
- View applications received for their jobs
- Update the status of an application

The API uses role-based permissions to keep these responsibilities separate.

The overall workflow is:

    User Registration
          ↓
    User selects role
          ↓
    Authentication
          ↓
    ┌───────────────────┐
    │                   │
    ▼                   ▼
    Job Seeker       Recruiter
    │                   │
    ├─ Upload Resume    ├─ Create Job
    ├─ View Jobs        ├─ Update Job
    ├─ Apply            ├─ Delete Job
    └─ Track Status     └─ Review Applications
                              │
                              ▼
                       Update Application
                              Status

---

# Main Features

## 1. Custom User Model

The project uses a custom Django User model based on `AbstractUser`.

Instead of relying completely on Django's default user model, the application adds fields required for the job portal.

The User model contains:

- First name
- Last name
- Username
- Email
- Password
- Role
- Profile photo
- Created timestamp

The email field is unique and is used as the authentication identifier.

The available roles are:

    jobseeker
    recruiter

This role is later used by the API permission system to control access to different operations.

---

# 2. Role-Based Access Control

The application separates users based on their role.

## Job Seeker

A Job Seeker can:

- View available jobs
- Upload a resume
- Apply for jobs
- View their own applications
- Track application status
- Manage their profile

## Recruiter

A Recruiter can:

- Create jobs
- Update their own jobs
- Delete their own jobs
- View applications received for their jobs
- Update application status

This prevents users from performing actions that do not belong to their role.

For example:

    Job Seeker
        ❌ Cannot create a job

    Recruiter
        ❌ Cannot apply for a job

The role checks are implemented using DRF permissions and additional view-level validation.

---

# 3. JWT Authentication

The project uses JSON Web Tokens (JWT) for API authentication.

The authentication flow is:

    Login / Obtain Token
          ↓
    Access Token + Refresh Token
          ↓
    Client stores token
          ↓
    Send Access Token
          ↓
    Authorization: Bearer <access_token>
          ↓
    Protected API

The project uses:

- Access Token
- Refresh Token
- Token Refresh
- Token Blacklisting

The access token is configured with a limited lifetime, while the refresh token can be used to obtain a new access token.

---

# 4. User Registration

Users can register through the registration API.

The registration request contains information such as:

- First name
- Last name
- Email
- Username
- Password
- Role
- Profile photo

Passwords are not stored as plain text.

The project uses Django's `create_user()` method so that passwords are properly hashed before being stored in the database.

---

# 5. User Profile Management

Authenticated users can access their profile.

The profile API supports:

- View profile
- Update profile
- Partially update profile
- Delete account

The profile response can also include resume information when available.

---

# 6. Resume Upload

Resume management is implemented as a separate model linked to the user.

The relationship is:

    User
      │
      │ One-to-One
      ▼
    Resume

A resume can contain:

- Resume file
- Skills
- Experience
- Last updated time

Only users with the `jobseeker` role are allowed to upload resumes.

The API accepts multipart form data for file uploads.

This was implemented to understand how file uploads work in a REST API instead of handling only JSON requests.

---

# 7. Job Management

Recruiters can create job postings.

Each job contains information such as:

- Job title
- Job description
- Company / recruiter
- Location
- Salary
- Created date

The relationship is:

    Recruiter
        │
        └────── creates ──────► Job

The recruiter is automatically associated with the job from the authenticated user rather than allowing the client to manually assign the company.

This helps maintain ownership of job postings.

---

# 8. Job CRUD Operations

Recruiters can manage their job postings through REST APIs.

### Create

A recruiter can create a new job.

### Read

Authenticated users can retrieve the available job listings.

### Update

A recruiter can update a job that belongs to them.

Both:

    PUT
    PATCH

are supported.

### Delete

A recruiter can delete their job posting.

The important part is that a recruiter should only be able to modify their own jobs.

For example:

    Recruiter A
        │
        ├── Job 1
        └── Job 2

    Recruiter B
        │
        └── Job 3

Recruiter A should not be able to update or delete Job 3.

The project uses a custom `IsRecruiter` permission and ownership checks for this purpose.

---

# 9. Job Application System

The application system connects a Job Seeker with a Job.

The relationship is:

    Job Seeker
         │
         │ applies
         ▼
        Job
         │
         ▼
    Job Application

A JobApplication record stores:

- Applicant
- Job
- Application status
- Applied date

The application status follows a simple workflow:

    Applied
       ↓
    Reviewed
       ↓
    Shortlisted

or

    Applied
       ↓
    Reviewed
       ↓
    Rejected

This represents a basic recruitment lifecycle.

---

# 10. Preventing Duplicate Applications

A Job Seeker should not be able to apply for the same job multiple times.

The application model enforces uniqueness for:

    applicant + job

For example:

    User A → Job 1 → Application 1

If User A tries to apply again:

    User A → Job 1 → ❌ Duplicate application

The API also checks for an existing application before creating a new one.

This provides protection at both the application logic and database-model level.

---

# 11. Application Status Management

Recruiters can review applications submitted to their own jobs.

A recruiter can update the application status.

For example:

    Applied
       ↓
    Reviewed
       ↓
    Shortlisted

or:

    Applied
       ↓
    Reviewed
       ↓
    Rejected

Before updating the status, the API checks whether the authenticated recruiter owns the job associated with the application.

This prevents one recruiter from modifying applications belonging to another recruiter.

---

# 12. Viewing Applications

The API provides separate views depending on the user's role.

## Job Seeker

A Job Seeker can view their own applications.

Example:

    My Applications

    Python Developer
    Status: Shortlisted

    Backend Developer
    Status: Reviewed

## Recruiter

A Recruiter can view applications received for their own job postings.

Example:

    Job: Python Developer

    Applicant: candidate_1
    Status: Applied

    Applicant: candidate_2
    Status: Shortlisted

The data is filtered using the authenticated user instead of exposing all applications.

---

# API Endpoints

## Authentication & User APIs

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/register/` | Register a new user |
| POST | `/login/` | Validate user credentials |
| POST | `/logout/` | Logout / blacklist refresh token |
| GET | `/profile/` | View authenticated user's profile |
| PUT | `/profile/` | Update profile |
| PATCH | `/profile/` | Partially update profile |
| DELETE | `/profile/` | Delete account |
| POST | `/uploadresume/` | Upload / update resume |

---

# JWT Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| POST | `/api/token/` | Obtain access and refresh tokens |
| POST | `/api/token/refresh/` | Refresh an access token |

Example authentication header:

    Authorization: Bearer <access_token>

---

# Job APIs

| Method | Endpoint | Purpose | Access |
|--------|----------|---------|--------|
| GET | `/job/job_list/` | List available jobs | Authenticated / Read |
| POST | `/job/job_list/` | Create a job | Recruiter |
| PUT | `/job/job_list/<id>/update/` | Replace a job | Job owner |
| PATCH | `/job/job_list/<id>/update/` | Partially update a job | Job owner |
| DELETE | `/job/job_list/<id>/delete/` | Delete a job | Job owner |

---

# Application APIs

| Method | Endpoint | Purpose | Access |
|--------|----------|---------|--------|
| POST | `/app/jobapply/` | Apply for a job | Job Seeker |
| GET | `/app/jobseekerview/` | View own applications | Job Seeker |
| GET | `/app/recruiterview/` | View applications for own jobs | Recruiter |
| PATCH | `/app/updatestatus/<id>/` | Update application status | Job owner |

---

# Example API Workflow

A typical Job Seeker workflow looks like this:

    1. Register
          ↓
    2. Obtain JWT token
          ↓
    3. Upload resume
          ↓
    4. View available jobs
          ↓
    5. Select a job
          ↓
    6. Submit application
          ↓
    7. View application status
          ↓
    8. Recruiter reviews application
          ↓
    9. Status changes
          ↓
    10. Job Seeker sees updated status

A Recruiter workflow looks like:

    1. Register as Recruiter
          ↓
    2. Obtain JWT token
          ↓
    3. Create job posting
          ↓
    4. View applications
          ↓
    5. Review applicants
          ↓
    6. Update application status

---

# Database Design

The main database relationships are:

    User
      │
      ├──────────────► Resume
      │
      ├──────────────► Job
      │                   │
      │                   │
      │                   ▼
      └──────────────► JobApplication
                              │
                              ▼
                             Job

More specifically:

    User
      │
      ├── 1 : 1 ── Resume
      │
      ├── 1 : Many ── Jobs (Recruiter)
      │
      └── 1 : Many ── JobApplications (Job Seeker)

    Job
      │
      └── 1 : Many ── JobApplications

This structure keeps user, job, resume and application data separated while maintaining their relationships through Django ORM.

---

# Project Structure

    Job-Portal-API/
    │
    ├── JobPortal/
    │   │
    │   ├── accounts/
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   ├── urls.py
    │   │   └── migrations/
    │   │
    │   ├── job/
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   ├── permissions.py
    │   │   ├── urls.py
    │   │   └── migrations/
    │   │
    │   ├── applications/
    │   │   ├── models.py
    │   │   ├── serializers.py
    │   │   ├── views.py
    │   │   ├── urls.py
    │   │   └── migrations/
    │   │
    │   ├── JobPortal/
    │   │   ├── settings.py
    │   │   ├── urls.py
    │   │   ├── asgi.py
    │   │   └── wsgi.py
    │   │
    │   ├── Dockerfile
    │   ├── docker-compose.yaml
    │   ├── requirements.txt
    │   └── manage.py
    │
    └── README.md

---

# Technology Stack

## Backend

- Python
- Django
- Django REST Framework

## Authentication

- JSON Web Token (JWT)
- Simple JWT
- Refresh Token
- Token Blacklisting

## Database

- PostgreSQL

## File Handling

- Django FileField
- Multipart form-data

## API Testing

- Postman

## Containerization

- Docker
- Docker Compose

---

# Docker Setup

The project uses Docker Compose to run the Django application and PostgreSQL database as separate services.

The architecture is:

    ┌───────────────────────────┐
    │       Docker Compose      │
    ├───────────────────────────┤
    │                           │
    │  Django REST API          │
    │                           │
    │          │                │
    │          ▼                │
    │  PostgreSQL Database      │
    │                           │
    └───────────────────────────┘

PostgreSQL data is persisted using a Docker volume.

---

# Running the Project Locally

## 1. Clone the repository

    git clone https://github.com/Saravanakumar1303/Job-Portal-API.git

    cd Job-Portal-API

## 2. Move into the Django project directory

    cd JobPortal

## 3. Build and start Docker containers

    docker compose up --build

## 4. Run migrations

If required:

    docker compose exec web python manage.py migrate

## 5. Create a superuser

    docker compose exec web python manage.py createsuperuser

## 6. Access the API

The Django application runs on the configured Docker port.

The PostgreSQL database runs inside its own Docker container.

---

# Testing with Postman

The APIs can be tested using Postman.

Recommended testing order:

### Step 1

Register a Job Seeker.

### Step 2

Obtain JWT tokens.

### Step 3

Add the access token to the Authorization header.

    Authorization: Bearer <access_token>

### Step 4

Upload a resume.

### Step 5

Register another user as a Recruiter.

### Step 6

Create a job using the Recruiter account.

### Step 7

Login as Job Seeker and apply for the job.

### Step 8

Login as Recruiter and view the received applications.

### Step 9

Update the application status.

### Step 10

Login again as Job Seeker and verify the updated status.

---

# Important Backend Concepts Used

This project helped me work with several concepts that are important in backend development.

### Custom User Model

Used Django's `AbstractUser` to create a user model specific to the application.

### Role-Based Access Control

Different operations are allowed depending on whether the authenticated user is a Job Seeker or Recruiter.

### JWT Authentication

Used access and refresh tokens for stateless API authentication.

### Object Ownership

Recruiters can modify only the jobs they created.

### File Upload

Resume files are uploaded using multipart form data and stored separately from user information.

### Relational Database Design

Users, jobs, resumes and applications are connected through foreign-key and one-to-one relationships.

### REST API Design

The project follows HTTP methods such as:

    GET
    POST
    PUT
    PATCH
    DELETE

according to the operation being performed.

---

# Challenges During Development

One of the main challenges was implementing different permissions for different types of users.

For example, the same API may be accessible for reading job listings, while creating or modifying a job should only be possible for recruiters.

Another challenge was handling file uploads because the API needs to accept multipart form data instead of only JSON.

The application workflow also required maintaining relationships between:

    User → Job → Application

and making sure users could only access data relevant to them.

JWT authentication and refresh-token handling were another important part of the project.

---

# What I Learned

Building this project helped me understand how a backend application works beyond simple CRUD APIs.

I gained practical experience with:

- Django REST Framework
- Custom user models
- JWT authentication
- Role-based permissions
- Object-level ownership checks
- File uploads
- Serializers
- Django ORM relationships
- PostgreSQL
- Docker
- REST API design
- API testing with Postman

The most important learning from this project was understanding how authentication and authorization are different.

Authentication answers:

    "Who is the user?"

Authorization answers:

    "What is this user allowed to do?"

For example, a recruiter may be authenticated successfully, but that does not mean the recruiter can modify another recruiter's job posting.

---

# Current Scope

The current version focuses on the core recruitment workflow:

    Authentication
         ↓
    User Roles
         ↓
    Job Management
         ↓
    Resume Upload
         ↓
    Job Application
         ↓
    Application Review
         ↓
    Status Tracking

The project is intended as a backend-focused implementation rather than a complete frontend job portal.

---

# Future Improvements

Some areas that can be added in future versions include:

- Job search and filtering
- Pagination
- Advanced recruiter dashboards
- Job categories
- Skills-based job matching
- Email notifications
- Application withdrawal
- Resume validation
- Resume file-type and size restrictions
- Password reset
- Email verification
- API documentation using Swagger / OpenAPI
- Automated unit and API tests
- Rate limiting
- Improved exception handling
- Production environment configuration
- CI/CD pipeline

---

# Project Status

The core Job Portal API workflow is implemented, including:

- Custom user authentication
- Job Seeker and Recruiter roles
- JWT authentication
- Resume upload
- Job CRUD
- Role-based permissions
- Job applications
- Application status tracking
- PostgreSQL integration
- Docker-based development

The project can be extended further with stronger validation, automated testing, API documentation, pagination, filtering and production-level security improvements.

---

# Author

**Saravanakumar V**

Python / Django Developer

GitHub:
https://github.com/Saravanakumar1303

LinkedIn:
https://www.linkedin.com/in/saravanakumar-varadarajan/
