## **💰 Smart Expense Tracker**

A full-stack web application built with **Django** that helps users monitor and understand their daily, weekly, and monthly expenses.

---

## 📋 Project Description

Smart Expense Tracker is a college-level Django project that allows users to securely record, categorize, and analyze their expenses. It features automatic category prediction from keywords, interactive Chart.js analytics, and report export in CSV and PDF formats.

---

## ✨ Features

| Feature | Description |
|---------|-------------|
| 🔐 Authentication | Signup, login, logout using Django's built-in auth |
| 💳 Add Expenses | Record expenses with description, amount, date, notes |
| 🤖 Smart Category | Auto-predicts category from keywords (e.g., "pizza" → Food) |
| 📋 Expense List | View all expenses with date filtering (Today/Week/Month/All) |
| ✏️ Edit Expenses | Update any expense with pre-filled form |
| 🗑️ Delete Expenses | Delete with confirmation page |
| 📊 Dashboard | Summary cards + Chart.js pie and bar charts |
| 📁 CSV Export | Download all expenses as a spreadsheet |
| 📄 PDF Export | Download a professionally formatted PDF report |
| 🔒 Data Isolation | Each user sees only their own data |
| 📱 Responsive | Works on desktop, tablet, and mobile |
| 🛡️ Admin Panel | Django admin to manage all records |

---

## 🔑 Quick Login Credentials

For testing and demonstration:

| Role | Username | Password |
|:---|:---|:---|
| **Admin Superuser** | `admin` | `admin123` |
| **Demo User** | `user` | `user123` |

You can also create your own custom account via the **Sign Up** page.

---

## 🛠️ Technologies Used

| Layer | Technology |
|-------|-----------|
| Backend | Python 3.x, Django 6.x |
| Frontend | HTML5, CSS3, Bootstrap 5, Vanilla JS |
| Database | SQLite (Django default) |
| Authentication | Django built-in auth system |
| Charts | Chart.js 4.x (CDN) |
| PDF Export | ReportLab |
| Icons | Bootstrap Icons |

---

## 📁 Folder Structure

```
expense/
│
├── manage.py
├── requirements.txt
├── README.md
├── db.sqlite3 (auto-created)
│
├── smart_expense_tracker/     ← Django project config
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py
│   └── asgi.py
│
├── expenses/                  ← Main app
│   ├── models.py              ← Expense model
│   ├── views.py               ← All views
│   ├── forms.py               ← Signup + Expense forms
│   ├── urls.py                ← App URL patterns
│   ├── admin.py               ← Admin configuration
│   ├── category_predictor.py  ← Keyword-based category prediction
│   ├── reports.py             ← CSV and PDF generation
│   ├── tests.py               ← Test suite
│   └── migrations/
│
├── templates/
│   ├── base.html              ← Base layout with navbar
│   ├── registration/
│   │   ├── login.html
│   │   └── signup.html
│   └── expenses/
│       ├── dashboard.html
│       ├── expense_list.html
│       ├── expense_form.html
│       ├── expense_confirm_delete.html
│       └── report.html
│
└── static/
    ├── css/style.css
    └── js/
        ├── main.js
        └── charts.js
```

---

## ⚙️ Installation & Setup

### 1. Check Prerequisites

Make sure Python 3.8+ is installed:

```bash
python --version
```

### 2. Create and Activate Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Windows)
venv\Scripts\activate

# Activate (Mac/Linux)
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Apply Database Migrations

```bash
python manage.py makemigrations
python manage.py migrate
```

### 5. Create a Superuser (Admin)

```bash
python manage.py createsuperuser
```

Follow the prompts to set a username, email, and password.

### 6. Run the Development Server

```bash
python manage.py runserver
```

---

## 🌐 How to Use

| URL | Description |
|-----|-------------|
| `http://127.0.0.1:8000/` | Redirects to dashboard |
| `http://127.0.0.1:8000/accounts/signup/` | Create new account |
| `http://127.0.0.1:8000/accounts/login/` | Login page |
| `http://127.0.0.1:8000/dashboard/` | Main dashboard |
| `http://127.0.0.1:8000/expenses/` | All expenses |
| `http://127.0.0.1:8000/expenses/add/` | Add expense |
| `http://127.0.0.1:8000/reports/` | Reports page |
| `http://127.0.0.1:8000/admin/` | Django admin panel |

---

## 🤖 Category Prediction Examples

| Description | Predicted Category |
|-------------|-------------------|
| "Uber ride to college" | Travel |
| "Pizza with friends" | Food |
| "Bought Python book" | Education |
| "Netflix subscription" | Entertainment |
| "Electricity bill" | Bills |
| "Medicine from pharmacy" | Health |
| "Ordered from Amazon" | Shopping |

---

## 🧪 Running Tests

```bash
python manage.py test expenses
```

Tests cover:
- Category prediction
- User authentication
- Expense CRUD operations
- Data isolation (security)
- CSV and PDF export

---

## 📸 Screenshots

> Add screenshots here after running the project.

- Dashboard
- Expense List
- Add Expense Form
- Analytics Charts
- Reports Page

---

## 🚀 Future Enhancements

- Budget limit setting with alerts
- Monthly spending goal tracker
- Income vs Expense comparison
- Multi-currency support
- Email report delivery
- Dark/Light mode toggle
- Recurring expense management

---

## 🎓 College Project Information

- **Project**: Smart Expense Tracker
- **Technology**: Python Django Full-Stack Web Application
- **Semester**: B.E. CSE
- **Database**: SQLite
- **Authentication**: Django Built-in Auth

---

> Built with ❤️ using Django, Bootstrap 5, and Chart.js# Expense-tracker
