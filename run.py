import os
from app import create_app, db
from app.models import User, Gig, Post, Course

app = create_app(os.environ.get('FLASK_ENV', 'development'))


@app.shell_context_processor
def make_shell_context():
    """Make database models available in Flask shell."""
    return {
        'db': db,
        'User': User,
        'Gig': Gig,
        'Post': Post,
        'Course': Course
    }


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
