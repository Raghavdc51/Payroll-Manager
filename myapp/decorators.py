# 📄 File: myapp/decorators.py
from django.http import HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from functools import wraps
from myapp.models import Profile


def role_required(allowed_roles):
    """
    Decorator to restrict views to users with specific roles.
    Example: @role_required(['admin', 'hr'])
    """
    def decorator(view_func):
        @wraps(view_func)
        @login_required
        def wrapper(request, *args, **kwargs):
            try:
                profile = request.user.profile
                if profile.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                return HttpResponseForbidden("🔒 You do not have permission to access this page.")
            except Profile.DoesNotExist:
                return HttpResponseForbidden("🔒 User profile not found. Please contact admin.")
        return wrapper
    return decorator