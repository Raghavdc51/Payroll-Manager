from django.core.management.base import BaseCommand
from django.contrib.auth.models import User
from myapp.models import Profile, Employee, SalaryStructure, Payroll
import random
from faker import Faker

fake = Faker()

class Command(BaseCommand):
    help = 'Seeds 50 fake users with roles, employees, salary structures, and multiple months of payroll'

    def handle(self, *args, **kwargs):
        self.stdout.write("🧹 Clearing old non-admin fake data...")

        # Clean up safely (keep admins/superusers)
        Payroll.objects.all().delete()
        SalaryStructure.objects.all().delete()
        Employee.objects.all().delete()
        Profile.objects.exclude(role='admin').delete()
        User.objects.exclude(is_superuser=True).delete()

        self.stdout.write("🌱 Creating 50 fake users...")

        job_data = [
            ('Developer', 'Engineering'),
            ('Backend Engineer', 'Engineering'),
            ('QA Engineer', 'Engineering'),
            ('UI/UX Designer', 'Design'),
            ('HR Coordinator', 'Human Resources'),
            ('HR Manager', 'Human Resources'),
            ('Marketing Specialist', 'Marketing'),
            ('Financial Analyst', 'Finance'),
            ('Support Executive', 'Customer Success'),
            ('Data Analyst', 'Analytics'),
        ]

        payroll_months = ['2026-01', '2026-02', '2026-03']
        statuses = ['active', 'inactive']
        hr_count = 0
        max_hr = 15

        grade_salaries = {
            'Engineering': (60000, 120000),
            'Design': (50000, 90000),
            'Human Resources': (45000, 80000),
            'Marketing': (45000, 85000),
            'Finance': (55000, 110000),
            'Analytics': (55000, 100000),
            'Customer Success': (40000, 75000),
        }

        for i in range(1, 51):
            # Create user
            first = fake.first_name()
            last = fake.last_name()
            username = f"user_{i:03d}"
            email = f"{first.lower()}.{last.lower()}@payroll-demo.com"

            user = User.objects.create_user(
                username=username,
                password='test1234',
                first_name=first,
                last_name=last,
                email=email,
            )

            # Profile is auto-created by signal – no need to create here
            # We can update role manually if needed (e.g. for HR)
            profile = user.profile
            if hr_count < max_hr and random.random() < 0.25:
                profile.role = 'hr'
                profile.save()
                hr_count += 1

            # Employee
            position, department = random.choice(job_data)
            min_sal, max_sal = grade_salaries.get(department, (40000, 80000))
            salary = random.randint(min_sal, max_sal)

            emp = Employee.objects.create(
                full_name=f"{first} {last}",
                position=position,
                department=department,
                salary=salary,
                status=random.choice(statuses),
            )

            # Salary structure
            basic = round(salary * 0.50, 2)
            hra = round(salary * 0.20, 2)
            allowances = round(salary * 0.15, 2)
            deductions = round(salary * 0.10, 2)

            struct = SalaryStructure.objects.create(
                employee=emp,
                basic=basic,
                hra=hra,
                allowances=allowances,
                deductions=deductions,
            )

            # Payroll for 3 months
            for month in payroll_months:
                Payroll.objects.create(
                    structure=struct,
                    month=month,
                    net_salary=struct.net_salary,
                    is_paid=random.choice([True, False, False]),  # ~33% paid
                )

        self.stdout.write(self.style.SUCCESS('✅ Seeded 50 fake users with roles, employees, salaries, and payrolls!'))