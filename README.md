# UniShare

A Flask-based web application for university students to share tutoring availability (gigs), create blog posts, and access centralized course resources. Features role-based access control with student, teacher, and admin roles.

## Features

- **Tutoring Gigs**: Students can post their tutoring availability and search for tutors by subject or major
- **Blog Posts**: All users can write and share blog posts
- **Course Resources**: Teachers can add course resources and links for students
- **Profile Management**: Users can customize their profiles with bio, major, and profile pictures
- **Admin Dashboard**: Admins can manage users and content with comprehensive statistics

## Tech Stack

- **Backend**: Flask 3.0
- **Database**: SQLite (development), PostgreSQL (production)
- **Authentication**: Flask-Login with password hashing
- **Forms**: Flask-WTF with validation
- **ORM**: Flask-SQLAlchemy
- **Image Processing**: Pillow
- **Production Server**: Gunicorn

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- pip
- virtualenv (recommended)

### Installation

1. **Clone or navigate to the project directory**:
   ```bash
   cd unishare
   ```

2. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and set your secret key:
   ```
   SECRET_KEY=your-secret-key-here
   FLASK_ENV=development
   ```

5. **Initialize the database**:
   ```bash
   flask db init
   flask db migrate -m "Initial migration"
   flask db upgrade
   ```

6. **Create an admin account**:
   ```bash
   python create_admin.py
   ```

7. **Run the development server**:
   ```bash
   python run.py
   ```

   The application will be available at `http://localhost:5000`

## Deployment to Render

For detailed deployment instructions, see [DEPLOYMENT.md](DEPLOYMENT.md).

### Quick Start

1. **Create a PostgreSQL database on Render**
2. **Create a Web Service** with:
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn run:app`
3. **Set Environment Variables**:
   - `FLASK_ENV=production`
   - `SECRET_KEY` (generate with: `python -c "import secrets; print(secrets.token_hex(32))"`)
   - `DATABASE_URL` (from your PostgreSQL database)
   - `ADMIN_USERNAME` (your admin username)
   - `ADMIN_EMAIL` (your admin email)
   - `ADMIN_PASSWORD` (your admin password)
4. **Deploy** - the build script will automatically:
   - Install dependencies
   - Run database migrations
   - Create your admin account


## User Roles

### Student
- Post tutoring gigs
- Create blog posts
- View all content
- Manage their own profile

### Teacher
- Create blog posts
- Add course resources
- View all content
- Manage their own profile

### Admin
- Full access to all features
- User management (create, delete users)
- Content moderation (delete any gig, post, course)
- Access to admin dashboard with statistics

## File Upload

- **Profile Pictures**: Supported formats are JPG, JPEG, PNG, GIF
- **Max File Size**: 16MB
- Images are automatically resized to 300x300 pixels

## Database Schema

### User
- `id`: Primary key
- `username`: Unique username
- `email`: Unique email
- `password_hash`: Hashed password
- `role`: student/teacher/admin
- `bio`: User bio (optional)
- `profile_picture`: Profile picture filename (optional)
- `major`: Student major (optional)
- `created_at`: Account creation timestamp

### Gig
- `id`: Primary key
- `user_id`: Foreign key to User
- `major`: Academic major
- `available_hours`: Availability description
- `subject`: Subject offered
- `created_at`: Creation timestamp

### Post
- `id`: Primary key
- `user_id`: Foreign key to User
- `title`: Post title
- `content`: Post content
- `created_at`: Creation timestamp
- `updated_at`: Last update timestamp

### Course
- `id`: Primary key
- `teacher_id`: Foreign key to User
- `title`: Course title
- `description`: Course description (optional)
- `link`: Course resource URL
- `created_at`: Creation timestamp

## Security Features

- Password hashing with Werkzeug
- CSRF protection on all forms
- Role-based access control
- Input validation and sanitization
- Secure file uploads

## Development Commands

```bash
# Run development server
python run.py

# Database migrations
flask db init          # Initialize migrations (first time only)
flask db migrate -m "message"  # Create migration
flask db upgrade       # Apply migrations

# Flask shell (for database operations)
flask shell

# Create admin account
python create_admin.py
```

## Project Structure

```
unishare/
├── app/
│   ├── __init__.py          # App factory
│   ├── models.py            # Database models
│   ├── forms.py             # WTForms
│   ├── decorators.py        # Custom decorators
│   ├── routes/              # Blueprint routes
│   │   ├── auth.py
│   │   ├── gigs.py
│   │   ├── posts.py
│   │   ├── courses.py
│   │   ├── profile.py
│   │   └── admin.py
│   ├── templates/           # Jinja2 templates
│   └── static/              # CSS, JS, uploads
├── config.py                # Configuration
├── requirements.txt         # Dependencies
├── run.py                   # Application entry point
├── create_admin.py          # Admin creation script
├── Procfile                 # Render deployment
└── README.md                # This file
```

## License

This project is open source and available under the MIT License.

## Support

For issues or questions, please create an issue in the repository.
