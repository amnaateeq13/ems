from django.core.exceptions import PermissionDenied

def role_required(required_role):
    def decorator(view_func):
        def _wrapped_view(request, *args, **kwargs):
            if not request.user.is_authenticated:
                raise PermissionDenied("You must be logged in.")
            if request.user.role != required_role:
                raise PermissionDenied("Access denied: wrong role.")
            return view_func(request, *args, **kwargs)
        return _wrapped_view
    return decorator
from django.core.exceptions import PermissionDenied
from django.contrib.auth.decorators import login_required

def role_required(*allowed_roles):
    def decorator(view_func):
        @login_required
        def _wrapped_view(request, *args, **kwargs):
            # Assumes 'role' field is on the User model directly
            if hasattr(request.user, 'role'):
                if request.user.role in allowed_roles:
                    return view_func(request, *args, **kwargs)
                else:
                    raise PermissionDenied("Access denied: wrong role.")
            else:
                raise PermissionDenied("User role not found.")
        return _wrapped_view
    return decorator
