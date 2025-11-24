from functools import wraps
from flask import abort
from flask_login import current_user


def login_required_with_role(*roles):
    """Decorator to require login and specific role(s)."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            if not current_user.is_authenticated:
                abort(401)
            if current_user.role not in roles:
                abort(403)
            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Decorator to require admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated or not current_user.is_admin():
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


def teacher_or_admin_required(f):
    """Decorator to require teacher or admin role."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        if not (current_user.is_teacher() or current_user.is_admin()):
            abort(403)
        return f(*args, **kwargs)
    return decorated_function
