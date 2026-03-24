from django.contrib import admin
from django.urls import path
from django.shortcuts import redirect
from django.conf import settings
from django.conf.urls.static import static

from myapp import views as my_views

urlpatterns = [
    # 🔐 Admin Panel
    path('admin/', admin.site.urls),

    # 🏠 Landing Page
    path('', my_views.select_role, name='select_role'),

    # 🔑 Authentication Routes
    path('login/admin/', my_views.login_admin_view, name='login_admin'),
    path('login/hr/', my_views.login_hr_view, name='login_hr'),
    path('login/emp/', my_views.login_emp_view, name='login_emp'),

    # Generic login fallback
    path('login/', lambda request: redirect('select_role'), name='login'),

    # Logout
    path('logout/', my_views.custom_logout, name='logout'),

    # 🏠 Main Dashboard
    path('dashboard/', my_views.dashboard_view, name='dashboard'),

    # 💰 Salary & Payroll Actions
    path('salary/update/', my_views.update_salary_structure, name='update_salary_structure'),
    path('payroll/mark-paid/<int:payroll_id>/', my_views.mark_payroll_paid, name='mark_payroll_paid'),

    # 📄 Payslip Routes
    # path('payslip/<int:payroll_id>/', my_views.generate_payslip_pdf, name='view_payslip'),
    path('preview-payslip/<int:payroll_id>/', my_views.preview_payslip, name='preview_payslip'),

    # 👤 Registration Routes
    path('register/', my_views.register_emp_view, name='register'),
    path('register/hr/', my_views.register_hr_view, name='register_hr'),

    # 👥 Employee Management (Admin & HR only)
    path('employees/', my_views.manage_employees, name='manage_employees'),
    path('employee/add/', my_views.add_employee, name='add_employee'),
    path('employee/<int:emp_id>/edit/', my_views.edit_employee, name='edit_employee'),
    path('employee/<int:emp_id>/delete/', my_views.delete_employee, name='delete_employee'),
    path('my-salary/', my_views.employee_salary_view, name='employee_salary'),
]

# Serve static and media files during development
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)