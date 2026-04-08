# 🚀 JobPortal API

## 📌 Project Overview

JobPortal API is a backend system built using Django REST Framework that connects **job seekers** and **recruiters**. It allows recruiters to post jobs and job seekers to apply for them with resume uploads.

---

## 👥 User Roles

### 🔹 Job Seeker

* Register & create profile
* Upload resume (separate model)
* Apply for jobs
* Track application status

### 🔹 Recruiter

* Register & create profile
* Create, update, delete job postings
* View applications
* Update application status

---

## ⚙️ Features

* ✅ Custom User Model (Abstract User)
* ✅ Role-based system (Job Seeker / Recruiter)
* ✅ Resume upload functionality
* ✅ Job CRUD operations (Recruiter only)
* ✅ Job application system
* ✅ Application status tracking
* ✅ JWT Authentication
* ✅ RESTful APIs

---

## 🛠️ Tech Stack

* **Backend Framework**: Django REST Framework (DRF)
* **Authentication**: JWT (JSON Web Token)
* **Database**: PostgreSQL
* **Testing Tool**: Postman
* **Deployment**: Docker

---

## 📂 Project Structure

```
JobPortal/
│── accounts/
│── job/
│── application/
│── manage.py
│── requirements.txt
│── README.md
```

---

## 🔐 Authentication

This project uses JWT authentication.

* Login → Get Access & Refresh Token
* Use Access Token in headers:

```
Authorization: Bearer <access_token>
```

## 🧪 API Testing

Use Postman to test all APIs:

* User Registration
* Login (JWT)
* Job APIs
* Application APIs

---

## 📌 Notes

* Recruiters can manage jobs
* Job seekers can only apply for jobs
* Resume upload is handled separately
* Role-based permissions implemented

---
