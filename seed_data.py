"""
Seed demo data for Mini LMS.
Run with: python manage.py shell < seed_data.py
Or:       python seed_data.py (if Django settings are configured)
"""
import os
import django
from datetime import datetime, timedelta

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from accounts.models import User
from courses.models import Course, Lesson, Assignment

print("🌱 Seeding demo data...")

# ── Users ────────────────────────────────────────────────────────────────────
instructor, _ = User.objects.get_or_create(
    username='instructor1',
    defaults={'email': 'instructor@example.com', 'role': 'instructor'}
)
instructor.set_password('password123')
instructor.save()

student1, _ = User.objects.get_or_create(
    username='student1',
    defaults={'email': 'student1@example.com', 'role': 'student'}
)
student1.set_password('password123')
student1.save()

student2, _ = User.objects.get_or_create(
    username='student2',
    defaults={'email': 'student2@example.com', 'role': 'student'}
)
student2.set_password('password123')
student2.save()

print("✅ Users created")

# ── Courses ──────────────────────────────────────────────────────────────────
courses_data = [
    {
        'title': 'Introduction to Python',
        'description': 'Learn the fundamentals of Python programming from scratch. Covers variables, loops, functions, and object-oriented programming.',
    },
    {
        'title': 'Web Development with Django',
        'description': 'Build powerful web applications using the Django framework. Learn MVC patterns, ORM, authentication, and REST APIs.',
    },
    {
        'title': 'Data Science Fundamentals',
        'description': 'Explore data analysis, visualization, and machine learning with Python libraries like pandas, matplotlib, and scikit-learn.',
    },
]

created_courses = []
for cd in courses_data:
    course, _ = Course.objects.get_or_create(
        title=cd['title'],
        defaults={'description': cd['description'], 'instructor': instructor}
    )
    course.students.add(student1)
    created_courses.append(course)

print(f"✅ {len(created_courses)} courses created")

# ── Lessons ───────────────────────────────────────────────────────────────────
py_course = created_courses[0]
lessons_data = [
    ('Getting Started', 'Install Python, set up your environment, and write your first script.', 1),
    ('Variables & Data Types', 'Learn about integers, strings, lists, tuples, and dictionaries.', 2),
    ('Control Flow', 'Master if-else statements, for loops, while loops, and break/continue.', 3),
    ('Functions', 'Define reusable functions, understand scope, and use lambda expressions.', 4),
]
for title, content, order in lessons_data:
    Lesson.objects.get_or_create(
        course=py_course, title=title,
        defaults={'content': content, 'order': order}
    )

print("✅ Lessons created")

# ── Assignments ───────────────────────────────────────────────────────────────
assignments_data = [
    ('Week 1: Hello World', 'Write a Python script that prints "Hello, World!" and your name.', 7),
    ('Week 2: FizzBuzz', 'Write a program that prints numbers 1-100, replacing multiples of 3 with Fizz, multiples of 5 with Buzz.', 14),
    ('Week 3: Calculator', 'Build a simple calculator that performs add, subtract, multiply, and divide operations.', 21),
]
for title, desc, days in assignments_data:
    Assignment.objects.get_or_create(
        course=py_course, title=title,
        defaults={
            'description': desc,
            'due_date': datetime.now() + timedelta(days=days),
            'max_score': 100,
        }
    )

print("✅ Assignments created")

print("""
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
🎓 Demo Accounts:

  Instructor:
    username: instructor1
    password: password123

  Student 1:
    username: student1
    password: password123

  Student 2:
    username: student2
    password: password123

Open: http://127.0.0.1:8000
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
""")
