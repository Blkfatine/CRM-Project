🚀 CRM Project – WebRasma & Digital Ranking

A modern Customer Relationship Management (CRM) system built with Django to manage leads, appointments, and internal communications efficiently. This project showcases practical experience in full-stack web development and database management.

📌 Key Features
User-Facing

Dashboard: Quick stats, recent leads, upcoming appointments, notifications.

Lead Management: Add, edit, delete leads, import via CSV, assign to users, track interactions.

Appointments: Schedule, track status (planned, confirmed, completed, cancelled).

Messaging: Internal chat system for users and groups.

Announcements: Team updates and important notifications.

Admin Panel

Global Dashboard: Stats, lead sources, user performance graphs.

User Management: Add, edit, delete users, assign roles.

Announcement Management: Create, edit, delete announcements for all users.

🛠 Technologies

Backend: Django 5.0.7, SQLite, Django ORM

Frontend: HTML5, CSS3, JavaScript, Ion Icons, Chart.js

Security: CSRF protection, role-based access, server-side form validation

⚡ Quick Setup
git clone https://github.com/Blkfatine/CRM-Project.git
cd CRM-Project
python -m venv venv
# Activate venv:
# Windows: venv\Scripts\activate
# macOS/Linux: source venv/bin/activate
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver


Access the app at http://127.0.0.1:8000
 and the admin at /admin.

🎯 Purpose

This project is a real demonstration of the skills listed on my CV: Django, full-stack web development, database handling, and building functional web apps. Perfect for recruiters to see that these projects are fully implemented.
