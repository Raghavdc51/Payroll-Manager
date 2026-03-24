# Payroll Management System

A Django-based payroll management system with role-based authentication for Admin, HR, and Employee users.

---

## ✨ Features

### 👑 Admin
- Dashboard with summary statistics
- Visual doughnut chart (Paid vs Unpaid payrolls)
- Full employee and payroll management

### 💼 HR
- Employee CRUD operations (Add, Edit, Delete)
- View and manage pending payrolls
- Mark payrolls as paid
- Search and filter by name or department
- Update salary structures

### 👨‍💼 Employee
- View salary breakdown
- View payroll history
- Preview payslips

---

## 🛠 Tech Stack

| Category | Technology |
|----------|------------|
| Backend | Django 6.0.2 |
| Database | SQLite (dev) / MySQL (prod) |
| Frontend | Bootstrap 5.3, Chart.js|
| Python | 3.x |

---

## 📁 Project Structure

```
payroll/
├── settings.py          # Django settings
├── urls.py               # URL routing
├── wsgi.py               # WSGI entry
├── asgi.py               # ASGI entry

myapp/
├── models.py             # Profile, Employee, SalaryStructure, Payroll
├── views.py              # All view functions
├── forms.py              # Django forms
├── decorators.py         # @role_required decorator
├── admin.py              # Admin config
├── signals.py            # Django signals

templates/
├── base.html             # Base template with Bootstrap
├── dashboard.html        # Role-specific dashboards
├── select_role.html      # Landing page
├── registration/         # Login/Register templates
└── partials/             # Reusable template parts

static/myapp/
├── style.css             # Custom styles
└── logo.png              # App logo
```

---

## 🚀 Quick Start

```bash
# 1. Navigate to project
cd payroll-1

# 2. Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows

# 3. Install dependencies
pip install -r requirements.txt

# 4. Run migrations
python manage.py migrate

# 5. Create superuser (optional)
python manage.py createsuperuser

# 6. Seed fake data 
python manage.py seed_fake

# 7. Run server
python manage.py runserver
```

Open http://127.0.0.1:8000/

---

## 🗄 Database Models

### Profile
Links User to a role (admin/hr/emp).

```python
class Profile(models.Model):
    ROLE_CHOICES = [('admin','Admin'), ('hr','HR'), ('emp','Employee')]
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='emp')
```

### Employee
```python
class Employee(models.Model):
    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="General")
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('active','Active'),('inactive','Inactive')])
```

### SalaryStructure
```python
class SalaryStructure(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE)
    basic = models.DecimalField(max_digits=12, decimal_places=2)
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    
    @property
    def net_salary(self):
        return (self.basic + self.hra + self.allowances) - self.deductions
```

### Payroll
```python
class Payroll(models.Model):
    structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE)
    month = models.CharField(max_length=7, default=now().strftime("%Y-%m"))
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
```

---

## 🔀 Database Configuration

### Development (SQLite) - Default
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Production (MySQL) - Uncomment in settings.py
```python
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.mysql',
#         'NAME': 'payroll_db',
#         'USER': 'root',
#         'PASSWORD': 'tiger',
#         'HOST': 'localhost',
#         'PORT': '3306',
#     }
# }
```

---

## 🌐 URL Routes

| URL | View | Description |
|-----|------|-------------|
| `/` | select_role | Landing page |
| `/login/admin/` | login_admin_view | Admin login |
| `/login/hr/` | login_hr_view | HR login |
| `/login/emp/` | login_emp_view | Employee login |
| `/logout/` | custom_logout | Logout |
| `/dashboard/` | dashboard_view | Main dashboard |
| `/register/` | register_emp_view | Employee registration |
| `/register/hr/` | register_hr_view | HR registration |
| `/employees/` | manage_employees | Manage employees |
| `/employee/add/` | add_employee | Add employee |
| `/employee/<id>/edit/` | edit_employee | Edit employee |
| `/employee/<id>/delete/` | delete_employee | Delete employee |
| `/my-salary/` | employee_salary_view | View own salary |
| `/salary/update/` | update_salary_structure | Update salary |
| `/payroll/mark-paid/<id>/` | mark_payroll_paid | Mark as paid |
| `/preview-payslip/<id>/` | preview_payslip | Preview payslip |

---

## 🔐 Authentication

**Reserved Usernames:** admin, administrator, hr, superuser

**Role Access:**
- Admin: Full access
- HR: Manage employees and payrolls
- Employee: View own salary and payroll history

---

## 🎨 JavaScript Features

| Feature | File | Description |
|---------|------|-------------|
| Chart.js | dashboard.html | Doughnut chart (Paid/Unpaid) |
| Table Sorting | dashboard.html | Sortable columns |
| Search & Filter | dashboard.html | Real-time filtering |
| Toast Notifications | base.html | Auto-dismiss alerts |
| Modal Popups | partials/*.html | Dynamic form pre-filling |
| Live Search | employee_list.html | Instant search |

**External Libraries:**
- Bootstrap 5.3.3
- Chart.js 4.4.0
- Bootstrap Icons

---

## 📜 License

This project is for educational purposes.

---

## 👤 Author

Developed with Django and Bootstrap

