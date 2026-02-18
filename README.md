# 🎓 Mini LMS — Learning Management System

A full-stack Learning Management System built with **Django + Django REST Framework** and a vanilla JS frontend. Supports instructors, students, JWT auth, course management, assignments, and submissions.

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Run Migrations

```bash
python manage.py makemigrations accounts
python manage.py makemigrations courses
python manage.py migrate
```

### 3. (Optional) Load Demo Data

```bash
python seed_data.py
```

Creates demo users:
| Username | Password | Role |
|---|---|---|
| `instructor1` | `password123` | Instructor |
| `student1` | `password123` | Student |
| `student2` | `password123` | Student |

### 4. Create Admin User

```bash
python manage.py createsuperuser
```

### 5. Start the Server

```bash
python manage.py runserver
```

Visit: **http://127.0.0.1:8000**  
Admin: **http://127.0.0.1:8000/admin/**

---

## 🗂 Project Structure

```
mini_lms/
├── manage.py
├── requirements.txt
├── seed_data.py
├── setup.sh
│
├── backend/                  # Django project settings
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── accounts/                 # Auth & user roles
│   ├── models.py             # Custom User with role field
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   └── admin.py
│
├── courses/                  # Core LMS functionality
│   ├── models.py             # Course, Lesson, Assignment, Submission
│   ├── serializers.py
│   ├── views.py
│   ├── urls.py
│   ├── permissions.py
│   └── admin.py
│
└── frontend/                 # HTML/CSS UI
    ├── templates/
    │   ├── index.html        # Login / Register
    │   ├── courses.html      # Course catalog
    │   └── assignments.html  # Assignments & Submissions
    └── static/
        └── css/
            └── style.css
```

---

## 🔌 API Endpoints

### Authentication
| Method | Endpoint | Description |
|---|---|---|
| POST | `/api/accounts/register/` | Register new user |
| POST | `/api/token/` | Login → JWT tokens |
| POST | `/api/token/refresh/` | Refresh access token |
| GET | `/api/accounts/profile/` | Get current user profile |

### Courses
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/courses/` | List all published courses |
| POST | `/api/courses/` | Create course *(instructor)* |
| GET | `/api/courses/<id>/` | Course detail |
| PUT | `/api/courses/<id>/` | Update course *(instructor)* |
| DELETE | `/api/courses/<id>/` | Delete course *(instructor)* |
| POST | `/api/courses/<id>/enroll/` | Enroll/unenroll *(student)* |
| GET | `/api/courses/my/` | My courses (enrolled or teaching) |

### Lessons
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/courses/<course_id>/lessons/` | List lessons |
| POST | `/api/courses/<course_id>/lessons/` | Add lesson *(instructor)* |

### Assignments
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/courses/assignments/` | List assignments |
| POST | `/api/courses/assignments/` | Create assignment *(instructor)* |
| DELETE | `/api/courses/assignments/<id>/` | Delete assignment |

### Submissions
| Method | Endpoint | Description |
|---|---|---|
| GET | `/api/courses/submissions/` | List submissions |
| POST | `/api/courses/submissions/` | Submit assignment *(student)* |
| GET | `/api/courses/submissions/<id>/` | Submission detail |
| PATCH | `/api/courses/submissions/<id>/` | Grade submission *(instructor)* |

---

## 👥 User Roles

| Role | Capabilities |
|---|---|
| **Admin** | Full access via `/admin/` dashboard |
| **Instructor** | Create/manage courses, lessons, assignments; grade submissions |
| **Student** | Browse & enroll in courses; submit assignments; view grades |

---

## 🖥 Frontend Pages

| Page | URL | Description |
|---|---|---|
| Login/Register | `/` | JWT authentication |
| Courses | `/courses/` | Browse & enroll in courses |
| Assignments | `/assignments/` | Submit work & view grades |

---

## 🔐 Authentication Flow

1. User registers at `/api/accounts/register/`
2. Logs in at `/api/token/` → receives `access` + `refresh` tokens
3. Frontend stores tokens in `localStorage`
4. All API requests include `Authorization: Bearer <access_token>`
5. Token refreshed automatically via `/api/token/refresh/`

---

## 🔮 Future Improvements

- [ ] File upload for assignments (PDFs, images)
- [ ] Grading rubrics and detailed analytics
- [ ] Real-time notifications (Django Channels / WebSockets)
- [ ] Email notifications for due dates & grades
- [ ] Student progress dashboard with charts
- [ ] Payment integration for premium courses
- [ ] Lesson video embedding support
- [ ] Cloud deployment (Render / Railway / AWS)
- [ ] REST API documentation with Swagger/OpenAPI
