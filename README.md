📄 DocSys – Document Management System

DocSys is a role-based Django web application designed to manage and organize documents efficiently across different user levels — Admin (HOD), Staff, Staff-Member, and Members.
Each user type has unique permissions, and the system ensures secure access and document handling through authentication and authorization.

🚀 Features
🔐 Authentication & Security

Custom login and role-based redirects (Admin, Staff, Member)

Global middleware to enforce login for all restricted pages

Access control for dashboards and features per role

Secure file upload and management

👨‍💼 Admin (HOD)

Add, edit, delete staff, staff-members, members, houses, and voices

Upload, edit, and delete documents

View and manage all uploaded documents

Dashboard with statistical summaries using Chart.js

👩‍🏫 Staff

Upload documents for review

View and manage personal documents

Update profile information

👩‍🏫 Staff-Member

Created by the Admin from the Members list

This is a member with staff and member privileges

Upload documents for review

View and manage personal documents

Update profile information

👨‍🎓 Member

View documents shared by admin or staff

Limited access based on role

Personal dashboard

📊 Dashboard & Analytics

Dynamic charts showing:

Total members, staff, houses, and voices

Voice distribution per house (using Chart.js)

Interactive hover tooltips for more detailed info

🧱 Tech Stack
Layer	Technologies Used

Frontend:	HTML5, CSS3, Bootstrap, AdminLTE, Chart.js, JavaScript

Backend:	Django (Python 3.x)

Database:	PostgreSQL, can support SQLite3/MySQL

Authentication:	Django’s built-in User model with custom roles

Other Tools:	jQuery, Font Awesome, Ionicons

🛡️ Security Enhancements

Middleware restricts direct URL access (must login)

Decorators @login_required and custom @role_required

File uploads sanitized and stored securely

Uses Django CSRF protection by default

📁 Project Structure
docSys/
│
├── docSys/                          # Main project folder
│   ├── settings.py                  # Project settings and configuration
│   ├── urls.py                      # Root URL routing
│   ├── middleware.py                # Custom authentication middleware
│   └── wsgi.py                      # WSGI configuration for deployment
│
├── docSys_app/                      # Main application
│   ├── models.py                    # Database models (User, Document, etc.)
│   ├── views.py                     # Base views and utilities
│   ├── HodViews.py                  # Admin/HOD specific views
│   ├── StaffViews.py                # Staff-specific views
│   ├── MemberViews.py               # Member-specific views
│   ├── decorators.py                # Role-based access decorators
│   ├── urls.py                      # App-specific URL routing
│   └── utils.py                     # Utility functions and helpers
│
├── templates/                       # Django templates
│   ├── base.html                    # Base template structure
│   ├── registration/                # Auth templates (login, logout)
│   ├── hod_template/                # Admin templates
│   │   ├── admin_dashboard.html     # Admin main dashboard
│   │   ├── manage_users.html        # User management
│   │   └── analytics.html           # Charts and reports
│   ├── staff_template/              # Staff templates
│   └── member_template/             # Member templates
│
├── static/                          # Static assets
│   ├── css/
│   │   ├── custom.css               # Custom styling overrides
│   │   └── dashboard.css            # Dashboard-specific styles
│   ├── js/
│   │   ├── charts.js                # Chart.js configurations
│   │   └── custom.js                # Custom JavaScript
│   ├── dist/                        # AdminLTE compiled assets
│   ├── plugins/                     # jQuery, Bootstrap, Chart.js
│   └── images/                      # Logos and icons
│
├── media/                           # User-uploaded files
│   ├── documents/                   # Uploaded documents
│   └── profiles/                    # User profile pictures
│
├── screenshots/                     # README screenshots (add your images here)
│   ├── login-page.png
│   ├── admin-dashboard.png
│   ├── staff-dashboard.png
│   └── mobile-views.png
│
├── requirements.txt                 # Python dependencies
├── manage.py
└── README.md

⚙️ Installation & Setup
1️⃣ Prerequisites
Python 3.10 or higher

PostgreSQL (for production) or SQLite (for development)

Git

2️⃣ Clone & Setup
# Clone the repository
git clone https://github.com/Gilks97/docsys.git
cd docsys

# Create virtual environment
python -m venv venv
source env/bin/activate  # Linux/Mac
# OR
env\Scripts\activate     # Windows

# Install dependencies
pip install -r requirements.txt

3️⃣ Database Configuration
# Apply migrations
python manage.py makemigrations
python manage.py migrate

# Create superuser (Admin)
python manage.py createsuperuser

4️⃣ Run Server
python manage.py runserver

Visit http://127.0.0.1:8000/ to access the application.


Dashboards
Login page:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/12258f4c-af3c-4c76-b205-8afa1f6d9238" />

Admin Dashboard:
Home:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/f1b2315c-6244-461a-b4f1-9406ff6317ee" />

Add members:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/8a4a86c4-1f7a-4a27-bd9f-6b12cfc84ed6" />

Manage members:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/3e33cf09-ad23-4c36-bf69-caf21de1df5e" />

Add Staff:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/c7b074d6-11a9-432e-aaad-3d2828c944e1" />

Manage Staff:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/1008c367-d2f9-43b9-a973-0097d540a65b" />

Staff Dashboard:
Home:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/f50ce254-14c5-424a-bfc2-62b42689159a" />

Upload Document:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/4ca1c7b5-fc6b-468a-a403-9fe2ac3d5ab9" />

Manage Documents:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/727e5793-0d0d-4eaa-be49-fec18289b317" />

Member Dashboard:
Home:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/ba548cc5-a561-404a-ba50-2c57311ee822" />

Members' Documents view:
<img width="1366" height="701" alt="image" src="https://github.com/user-attachments/assets/91fcfdd4-a65b-4cf6-9d74-502c61470e23" />

