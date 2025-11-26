# Deployment Instructions for Render

## Prerequisites
- A Render account (free tier works fine)
- Your code pushed to GitHub

## Step-by-Step Deployment

### 1. Create a PostgreSQL Database
1. Go to [Render Dashboard](https://dashboard.render.com/)
2. Click "New +" → "PostgreSQL"
3. Fill in:
   - Name: `unishare-db` (or any name you prefer)
   - Database: `unishare`
   - User: `unishare` (auto-generated)
   - Region: Choose closest to you
   - Plan: **Free**
4. Click "Create Database"
5. **Important:** Copy the "Internal Database URL" - you'll need this

### 2. Create the Web Service
1. In Render Dashboard, click "New +" → "Web Service"
2. Connect your GitHub repository
3. Fill in the settings:
   - **Name**: `unishare` (or any name)
   - **Environment**: `Python 3`
   - **Region**: Same as your database
   - **Branch**: `main` (or your default branch)
   - **Build Command**: `chmod +x build.sh && ./build.sh`
   - **Start Command**: `gunicorn run:app`
   - **Plan**: **Free**

### 3. Configure Environment Variables
In your web service settings, go to "Environment" tab and add these variables:

| Key | Value |
|-----|-------|
| `FLASK_ENV` | `production` |
| `SECRET_KEY` | Generate a random string (use: `python -c "import secrets; print(secrets.token_hex(32))"`) |
| `DATABASE_URL` | Paste the Internal Database URL from Step 1 |
| `ADMIN_USERNAME` | Your desired admin username (e.g., `admin`) |
| `ADMIN_EMAIL` | Your admin email (e.g., `admin@unishare.com`) |
| `ADMIN_PASSWORD` | Your admin password (min 6 chars) |

### 4. Deploy
1. Click "Create Web Service"
2. Render will automatically:
   - Install dependencies
   - Run database migrations
   - Create your admin account
   - Start the application

### 5. Verify Deployment
1. Wait for the deployment to complete (check the logs)
2. Click the URL provided by Render (e.g., `https://unishare.onrender.com`)
3. Try logging in with your admin credentials

## Troubleshooting

### Common Issues

#### 1. Internal Server Error
- **Check Logs**: Go to your service → Logs tab
- **Common causes**:
  - Database not connected (check `DATABASE_URL`)
  - Migrations didn't run (check build logs)
  - Missing environment variables

#### 2. Database Connection Error
- Verify `DATABASE_URL` is set correctly
- Make sure the database is in the same region as your web service
- Check that the database is running (green status in Render dashboard)

#### 3. Admin Login Not Working
- Make sure `ADMIN_USERNAME`, `ADMIN_EMAIL`, and `ADMIN_PASSWORD` are set in environment variables
- Check build logs to see if admin was created successfully
- Try running the shell command to verify: `flask shell` then `User.query.filter_by(role='admin').first()`

#### 4. Static Files Not Loading
- Render free tier might have slower cold starts
- Check that `UPLOAD_FOLDER` directory exists
- Verify static file paths in templates

### Viewing Logs
```bash
# In Render Dashboard, go to:
Your Service → Logs
```

Look for errors related to:
- Database connection
- Missing environment variables
- Failed migrations
- Application startup errors

### Manual Database Commands (if needed)
You can run commands via Render Shell:

1. Go to your web service → Shell tab
2. Run migrations manually:
```bash
flask db upgrade
```

3. Create admin manually:
```bash
python create_admin.py
```

## Important Notes for Free Tier

1. **Cold Starts**: Your app will spin down after 15 minutes of inactivity and take 30-60 seconds to wake up
2. **Database Limitations**: Free PostgreSQL has a 90-day expiration
3. **No Persistent Storage**: Uploaded files will be lost on redeploy (use cloud storage for production)
4. **Limited Resources**: 512 MB RAM, shared CPU

## Updating Your Deployment

To update your app:
1. Push changes to GitHub
2. Render will automatically detect and redeploy
3. Or manually trigger: Service → Manual Deploy → Deploy latest commit

---

**Need Help?** Check the logs first - they usually show exactly what's wrong!
