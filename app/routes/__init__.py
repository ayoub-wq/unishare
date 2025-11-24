# Blueprint imports will be added here
from app.routes.auth import bp as auth_bp
from app.routes.gigs import bp as gigs_bp
from app.routes.posts import bp as posts_bp
from app.routes.courses import bp as courses_bp
from app.routes.profile import bp as profile_bp
from app.routes.admin import bp as admin_bp
from app.routes.setup import bp as setup_bp

__all__ = ['auth_bp', 'gigs_bp', 'posts_bp', 'courses_bp', 'profile_bp', 'admin_bp']
