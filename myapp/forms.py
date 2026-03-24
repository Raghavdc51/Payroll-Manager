# 📍 File: myapp/forms.py
from django import forms
from .models import Employee

DEPARTMENT_CHOICES = [
    ('Engineering', 'Engineering'),
    ('Design', 'Design'),
    ('Human Resources', 'Human Resources'),
    ('Marketing', 'Marketing'),
    ('Finance', 'Finance'),
    ('Analytics', 'Analytics'),
    ('Customer Success', 'Customer Success'),
]

POSITION_CHOICES = [
    ('Developer', 'Developer'),
    ('Backend Engineer', 'Backend Engineer'),
    ('QA Engineer', 'QA Engineer'),
    ('UI/UX Designer', 'UI/UX Designer'),
    ('HR Coordinator', 'HR Coordinator'),
    ('HR Manager', 'HR Manager'),
    ('Marketing Specialist', 'Marketing Specialist'),
    ('Financial Analyst', 'Financial Analyst'),
    ('Support Executive', 'Support Executive'),
    ('Data Analyst', 'Data Analyst'),
]


class EmployeeForm(forms.ModelForm):
    class Meta:
        model = Employee
        fields = ['full_name', 'position', 'department', 'salary', 'status']
        widgets = {
            'full_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter full name'
            }),
            'position': forms.Select(choices=POSITION_CHOICES, attrs={
                'class': 'form-select'
            }),
            'department': forms.Select(choices=DEPARTMENT_CHOICES, attrs={
                'class': 'form-select'
            }),
            'salary': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Monthly Salary (₹)',
                'min': '0',
                'step': '100'
            }),
            'status': forms.Select(attrs={
                'class': 'form-select'
            }),
        }

    def clean_salary(self):
        salary = self.cleaned_data.get('salary')
        if salary is not None and salary < 0:
            raise forms.ValidationError("Salary cannot be negative.")
        return salary