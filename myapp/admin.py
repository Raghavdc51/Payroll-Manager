from django.contrib import admin
from .models import Profile, Employee, SalaryStructure, Payroll

# 🎨 Admin branding
admin.site.site_header = "Payroll Manager Admin"
admin.site.site_title = "Payroll Admin Portal"
admin.site.index_title = "Welcome to Payroll Management Dashboard"

# 🧑‍💼 Profile admin
@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'role')
    list_filter = ('role',)
    search_fields = ('userusername', 'useremail')

# 👨‍💻 Employee admin
@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'position', 'salary', 'status']
    list_filter = ['status']
    ordering = ['full_name']
    search_fields = ['full_name', 'position', 'department']

# 💰 Salary structure admin
@admin.register(SalaryStructure)
class SalaryStructureAdmin(admin.ModelAdmin):
    list_display = ('employee', 'basic', 'hra', 'allowances', 'deductions')
    list_filter = ('employee',)
    search_fields = ('employee__full_name',)

# 🧾 Payroll admin
@admin.register(Payroll)
class PayrollAdmin(admin.ModelAdmin):
    list_display = ('structure', 'month', 'net_salary', 'is_paid')
    list_filter = ('is_paid', 'month')
    search_fields = ('structureemployeefull_name',)