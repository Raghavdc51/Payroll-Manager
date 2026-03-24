from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now


class Profile(models.Model):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('hr', 'HR'),
        ('emp', 'Employee'),
    )

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='emp')

    def __str__(self):
        return f"{self.user.username} ({self.role})"

    @property
    def is_admin(self):
        return self.role == 'admin'

    @property
    def is_hr(self):
        return self.role == 'hr'

    @property
    def is_employee(self):
        return self.role == 'emp'

    class Meta:
        verbose_name_plural = "Profiles"


class Employee(models.Model):
    STATUS_CHOICES = (
        ('active', 'Active'),
        ('inactive', 'Inactive'),
    )

    full_name = models.CharField(max_length=100)
    position = models.CharField(max_length=100)
    department = models.CharField(max_length=100, default="General")
    salary = models.DecimalField(max_digits=12, decimal_places=2)  # increased precision
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='active')

    class Meta:
        ordering = ['full_name']
        verbose_name_plural = "Employees"

    def __str__(self):
        return self.full_name


class SalaryStructure(models.Model):
    employee = models.ForeignKey(Employee, on_delete=models.CASCADE, related_name='salary_structures')
    basic = models.DecimalField(max_digits=12, decimal_places=2)
    hra = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    allowances = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    deductions = models.DecimalField(max_digits=12, decimal_places=2, default=0)

    class Meta:
        verbose_name_plural = "Salary Structures"

    def __str__(self):
        return f"{self.employee} – Net ₹{self.net_salary():.2f}"

    @property
    def gross_salary(self):
        return self.basic + self.hra + self.allowances

    @property
    def net_salary(self):
        return self.gross_salary - self.deductions


class Payroll(models.Model):
    structure = models.ForeignKey(SalaryStructure, on_delete=models.CASCADE, related_name='payrolls')
    month = models.CharField(max_length=7, default=now().strftime("%Y-%m"))
    net_salary = models.DecimalField(max_digits=12, decimal_places=2)
    is_paid = models.BooleanField(default=False)
    payslip_pdf = models.FileField(upload_to='payslips/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = "Payrolls"

    def __str__(self):
        status = "Paid" if self.is_paid else "Unpaid"
        return f"{self.structure.employee} – {self.month} ({status})"