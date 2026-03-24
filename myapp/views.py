from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.utils import timezone

from .models import Profile, Employee, SalaryStructure, Payroll
from .forms import EmployeeForm
from .decorators import role_required

# Reserved usernames
RESERVED_USERNAMES = ['admin', 'administrator', 'hr', 'superuser']


# Role Selector (landing page)
def select_role(request):
    return render(request, 'select_role.html')


# Logout
def custom_logout(request):
    logout(request)
    messages.success(request, "👋 Logged out successfully.")
    return redirect('select_role')


# Employee Registration
def register_emp_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role = 'emp'

        if username.lower() in RESERVED_USERNAMES or User.objects.filter(username__iexact=username).exists():
            messages.error(request, "⚠️ Username is not allowed or already taken.")
            return redirect('register')

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.update_or_create(user=user, defaults={'role': role})

        parts = username.split()
        user.first_name = parts[0]
        user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.save()

        full_name = user.get_full_name().strip()
        Employee.objects.get_or_create(
            full_name__iexact=full_name,
            defaults={'full_name': full_name, 'position': 'Support', 'salary': 25000, 'status': 'active'}
        )

        messages.success(request, f"✅ Employee '{full_name}' registered successfully!")
        return redirect('login_emp')

    return render(request, 'registration/register_emp.html')


# HR Registration
def register_hr_view(request):
    if request.method == 'POST':
        username = request.POST.get('username', '').strip()
        password = request.POST.get('password', '').strip()
        role = 'hr'

        if username.lower() in RESERVED_USERNAMES or User.objects.filter(username__iexact=username).exists():
            messages.error(request, "⚠️ Username is not allowed or already taken.")
            return redirect('register_hr')

        user = User.objects.create_user(username=username, password=password)
        Profile.objects.update_or_create(user=user, defaults={'role': role})

        parts = username.split()
        user.first_name = parts[0]
        user.last_name = " ".join(parts[1:]) if len(parts) > 1 else ""
        user.save()

        messages.success(request, f"✅ HR account for '{user.get_full_name()}' created successfully!")
        return redirect('login_hr')

    return render(request, 'registration/register_hr.html')


# Generic Login Handler
def login_view(request, expected_role, template, redirect_url, error_redirect):
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.get_user()
            if getattr(user.profile, 'role', '') != expected_role:
                messages.error(request, f"⚠️ Not a {expected_role.capitalize()} account.")
                return redirect(error_redirect)
            login(request, user)
            messages.success(request, f"✅ Logged in as {expected_role.capitalize()}!")
            return redirect(redirect_url)
        messages.error(request, "❌ Invalid credentials.")
    return render(request, template, {'form': form})


def login_admin_view(request):
    return login_view(request, 'admin', 'registration/login_admin.html', 'dashboard', 'login_admin')


def login_hr_view(request):
    return login_view(request, 'hr', 'registration/login_hr.html', 'dashboard', 'login_hr')


def login_emp_view(request):
    return login_view(request, 'emp', 'registration/login_emp.html', 'dashboard', 'login_emp')

@login_required
def employee_salary_view(request):
    if request.user.profile.role != 'emp':
        messages.error(request, "Only employees can access this page.")
        return redirect('dashboard')

    full_name = request.user.get_full_name().strip()
    employee = get_object_or_404(Employee, full_name__iexact=full_name)
    
    # Get the latest salary structure
    salary_structure = SalaryStructure.objects.filter(employee=employee).order_by('-id').first()
    
    if not salary_structure:
        messages.info(request, "No salary structure found for your profile.")
        salary_structure = None  # or handle as you wish

    context = {
        'salary_structure': salary_structure,
        'employee': employee,
    }
    return render(request, 'employee_salary.html', context)


# Dashboard View – FIXED department_list
@login_required
def dashboard_view(request):
    role = request.user.profile.role.lower()
    context = {'role': role}

    if role in ['admin', 'hr']:
        # FIXED: Unique departments from employees with unpaid payrolls
        department_list = Payroll.objects.filter(is_paid=False) \
            .values_list('structure__employee__department', flat=True) \
            .distinct() \
            .order_by()

        employee_count = Employee.objects.count()
        payroll_count = Payroll.objects.count()
        paid_count = Payroll.objects.filter(is_paid=True).count()
        unpaid_count = Payroll.objects.filter(is_paid=False).count()

        payrolls = Payroll.objects.select_related('structure__employee') \
                                .order_by('-created_at')

        search_query = request.GET.get('search', '').strip()
        if search_query:
            payrolls = payrolls.filter(
                structure__employee__full_name__icontains=search_query
            )

        context.update({
            'employees': Employee.objects.all(),
            'employee_count': employee_count,
            'payrolls': payrolls,
            'payroll_count': payroll_count,
            'paid_count': paid_count,
            'unpaid_count': unpaid_count,
            'pending_payrolls': Payroll.objects.filter(is_paid=False),
            'salary_structures': SalaryStructure.objects.all(),
            'department_list': department_list,
        })

        dashboard_cards = [
            {"label": "Total Employees", "count": employee_count, "color": "success"},
            {"label": "Total Payrolls", "count": payroll_count, "color": "primary"},
            {"label": "Paid Payrolls", "count": paid_count, "color": "info"},
        ]
        context["dashboard_cards"] = dashboard_cards

    elif role == 'emp':
        full_name = request.user.get_full_name().strip()
        emp, _ = Employee.objects.get_or_create(
            full_name__iexact=full_name,
            defaults={'full_name': full_name, 'position': 'Support', 'salary': 25000, 'status': 'active'}
        )

        context.update({
            'salary': SalaryStructure.objects.filter(employee=emp).last(),
            'salary_structures': SalaryStructure.objects.filter(employee=emp),
            'payrolls': Payroll.objects.filter(structure__employee=emp).order_by('-month')
        })

    else:
        messages.error(request, "❌ Unknown role.")
        return redirect('select_role')

    return render(request, 'dashboard.html', context)


# Preview Payslip (browser view)
@login_required
def preview_payslip(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    role = request.user.profile.role

    if role in ['admin', 'hr'] or payroll.structure.employee.full_name == request.user.get_full_name():
        return render(request, 'payslip.html', {
            'payroll': payroll,
            'now': timezone.now(),
            'request': request,
        })
    return HttpResponseForbidden("🚫 Access denied.")


# Update Salary Structure
@require_POST
@login_required
def update_salary_structure(request):
    struct = get_object_or_404(SalaryStructure, id=request.POST.get('structure_id'))
    struct.basic = float(request.POST.get('basic', 0))
    struct.hra = float(request.POST.get('hra', 0))
    struct.allowances = float(request.POST.get('allowances', 0))
    struct.deductions = float(request.POST.get('deductions', 0))
    struct.save()

    Payroll.objects.filter(structure=struct).update(net_salary=struct.net_salary)

    messages.success(request, f"💰 {struct.employee.full_name}'s salary updated.")
    return redirect('dashboard')


# Mark Payroll as Paid
@role_required(['hr'])
def mark_payroll_paid(request, payroll_id):
    payroll = get_object_or_404(Payroll, id=payroll_id)
    employee_name = payroll.structure.employee.full_name

    if payroll.is_paid:
        messages.info(request, f"ℹ️ Payroll for {employee_name} is already paid.")
    else:
        payroll.is_paid = True
        payroll.save()
        messages.success(request, f"✅ Payroll marked paid for {employee_name}.")
    return redirect('dashboard')


# Manage Employees
@role_required(['admin', 'hr'])
def manage_employees(request):
    return render(request, 'manage_employees.html', {
        'employees': Employee.objects.all(),
        'role': request.user.profile.role
    })


@user_passes_test(lambda u: u.is_superuser or u.profile.role in ['admin', 'hr'])
def add_employee(request):
    form = EmployeeForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        emp = form.save()
        messages.success(request, f"✅ {emp.full_name} added!")
        return redirect('dashboard')
    return render(request, 'employees/add_employee.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser or u.profile.role in ['admin', 'hr'])
def edit_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    form = EmployeeForm(request.POST or None, instance=emp)
    if form.is_valid():
        form.save()
        messages.success(request, f"✏️ {emp.full_name}'s details updated!")
        return redirect('dashboard')
    return render(request, 'employees/edit_employee.html', {'form': form})


@user_passes_test(lambda u: u.is_superuser or u.profile.role in ['admin', 'hr'])
def delete_employee(request, emp_id):
    emp = get_object_or_404(Employee, id=emp_id)
    if request.method == 'POST':
        emp.delete()
        messages.success(request, f"❌ {emp.full_name}'s record deleted.")
        return redirect('dashboard')
    return render(request, 'employees/delete_employee.html', {'employee': emp})