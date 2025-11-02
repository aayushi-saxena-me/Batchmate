# Deployment Guide - Inventory Management System

This guide covers multiple deployment options for your Django inventory management application, from the easiest GitHub-based deployments to more advanced containerized solutions.

## 📋 Table of Contents

1. [Quick Comparison](#quick-comparison)
2. [Easiest Options (Recommended)](#easiest-options-recommended)
   - [Railway.app](#railwayapp---recommended-easiest)
   - [Render.com](#rendercom)
   - [Fly.io](#flyio)
3. [Docker-Based Deployment](#docker-based-deployment)
4. [AWS Deployment Options](#aws-deployment-options)
   - [AWS Elastic Beanstalk](#aws-elastic-beanstalk)
   - [AWS ECS (Fargate)](#aws-ecs-fargate)
   - [AWS Lightsail](#aws-lightsail)
5. [Pre-Deployment Checklist](#pre-deployment-checklist)
6. [Post-Deployment Steps](#post-deployment-steps)

---

## Quick Comparison

| Platform | Ease | GitHub Deploy | Cost (Free Tier) | Best For |
|----------|------|---------------|-------------------|----------|
| **Railway** | ⭐⭐⭐⭐⭐ | ✅ Direct | $5/month credit | Quickest deployment |
| **Render** | ⭐⭐⭐⭐ | ✅ Direct | Free tier available | Budget-friendly |
| **Fly.io** | ⭐⭐⭐⭐ | ✅ Direct | Free tier | Global edge deployment |
| **Docker + AWS** | ⭐⭐ | Requires setup | Pay-as-you-go | Enterprise scale |

---

## Easiest Options (Recommended)

### Railway.app - ⭐ RECOMMENDED (Easiest)

**Why Railway?**
- ✅ Deploy directly from GitHub in 5 minutes
- ✅ Automatic PostgreSQL database setup
- ✅ Free $5/month credit (enough for small apps)
- ✅ Automatic SSL certificates
- ✅ No Docker knowledge required (though Dockerfile is included)

#### Step-by-Step Deployment:

1. **Push to GitHub**
   ```bash
   git add .
   git commit -m "Prepare for deployment"
   git push origin main
   ```

2. **Sign up at Railway**
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

3. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose your repository

4. **Configure Environment Variables**
   In Railway dashboard, go to Variables tab and add:
   ```
   DEBUG=False
   SECRET_KEY=<generate-a-random-secret-key>
   ALLOWED_HOSTS=your-app-name.railway.app
   DATABASE_URL=<auto-provided-by-railway>
   ```

5. **Add PostgreSQL Database**
   - Click "New" → "Database" → "PostgreSQL"
   - Railway automatically sets `DATABASE_URL`

6. **Deploy**
   - Railway automatically detects `Dockerfile` or `railway.json`
   - Deployment starts automatically
   - Your app will be live at `https://your-app-name.railway.app`

7. **Run Migrations**
   - In Railway dashboard, go to your service
   - Click "Deployments" → "View Logs"
   - Or use Railway CLI:
     ```bash
     railway run python manage.py migrate
     railway run python manage.py createsuperuser
     ```

**Cost:** $5/month free credit (usually enough for small apps)

---

### Render.com

**Why Render?**
- ✅ Free tier available (with limitations)
- ✅ Direct GitHub deployment
- ✅ PostgreSQL included

#### Step-by-Step Deployment:

1. **Sign up at Render**
   - Go to [render.com](https://render.com)
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository
   - Render will detect `render.yaml` configuration

3. **Configure Service**
   - Name: `inventory-management`
   - Environment: `Python 3`
   - Build Command: (auto-detected from render.yaml)
   - Start Command: `gunicorn inventory_management.wsgi:application --bind 0.0.0.0:8000`

4. **Add PostgreSQL Database**
   - Click "New +" → "PostgreSQL"
   - Note the connection string

5. **Set Environment Variables**
   ```
   DEBUG=False
   SECRET_KEY=<generate-random-key>
   ALLOWED_HOSTS=inventory-management.onrender.com
   DATABASE_URL=<from-postgres-service>
   ```

6. **Deploy**
   - Render automatically deploys on git push
   - First deployment may take 5-10 minutes

**Free Tier Limitations:**
- App spins down after 15 minutes of inactivity
- Slower startup times
- Limited to 512MB RAM

**Paid:** Starting at $7/month

---

### Fly.io

**Why Fly.io?**
- ✅ Global edge deployment (fast worldwide)
- ✅ Generous free tier
- ✅ Great for containerized apps

#### Step-by-Step:

1. **Install Fly CLI**
   ```bash
   # Windows (PowerShell)
   iwr https://fly.io/install.ps1 -useb | iex
   
   # Or download from fly.io
   ```

2. **Login and Initialize**
   ```bash
   fly auth login
   fly launch
   ```

3. **Fly will detect Dockerfile and create fly.toml**
   - Follow prompts
   - Choose a region close to you

4. **Deploy**
   ```bash
   fly deploy
   ```

5. **Set Secrets**
   ```bash
   fly secrets set SECRET_KEY=your-secret-key
   fly secrets set DEBUG=False
   fly secrets set ALLOWED_HOSTS=your-app.fly.dev
   ```

6. **Add PostgreSQL**
   ```bash
   fly postgres create --name inventory-db
   fly postgres attach inventory-db
   ```

7. **Run Migrations**
   ```bash
   fly ssh console -C "python manage.py migrate"
   fly ssh console -C "python manage.py createsuperuser"
   ```

**Cost:** Free tier includes 3 shared VMs, 3GB persistent volumes

---

## Docker-Based Deployment

### Using Docker Locally (Testing)

```bash
# Build and run with docker-compose
docker-compose up --build

# Access at http://localhost:8000
```

### Using Docker on Any Platform

Any platform that supports Docker can use the included `Dockerfile`:

1. **Build the image**
   ```bash
   docker build -t inventory-management .
   ```

2. **Run the container**
   ```bash
   docker run -p 8000:8000 \
     -e SECRET_KEY=your-secret \
     -e DEBUG=False \
     -e ALLOWED_HOSTS=yourdomain.com \
     -e DATABASE_URL=postgresql://... \
     inventory-management
   ```

---

## AWS Deployment Options

### AWS Elastic Beanstalk

**Easiest AWS option - no Docker required**

1. **Install EB CLI**
   ```bash
   pip install awsebcli
   ```

2. **Initialize EB**
   ```bash
   eb init -p python-3.12 inventory-management
   ```

3. **Create Environment**
   ```bash
   eb create inventory-env
   ```

4. **Set Environment Variables**
   ```bash
   eb setenv SECRET_KEY=your-key DEBUG=False
   ```

5. **Deploy**
   ```bash
   eb deploy
   ```

**Cost:** ~$30-50/month (EC2 instance + RDS)

---

### AWS ECS (Fargate)

**Container-based, serverless**

1. **Build and Push to ECR**
   ```bash
   aws ecr create-repository --repository-name inventory-management
   docker build -t inventory-management .
   docker tag inventory-management:latest <account>.dkr.ecr.<region>.amazonaws.com/inventory-management:latest
   docker push <account>.dkr.ecr.<region>.amazonaws.com/inventory-management:latest
   ```

2. **Create ECS Task Definition**
   - Use AWS Console or Terraform
   - Configure environment variables
   - Set up RDS PostgreSQL database

3. **Deploy**
   - Create ECS service from task definition
   - Configure Application Load Balancer

**Cost:** ~$40-80/month (Fargate + RDS + ALB)

---

### AWS Lightsail

**Simplest AWS option - like a VPS**

1. **Create Lightsail Instance**
   - Choose "Django" blueprint or "OS Only" (Ubuntu)
   - Connect via SSH

2. **Install Dependencies**
   ```bash
   sudo apt update
   sudo apt install python3-pip postgresql nginx
   pip3 install -r requirements.txt
   ```

3. **Set up PostgreSQL**
   ```bash
   sudo -u postgres createdb inventory_db
   sudo -u postgres createuser inventory_user
   ```

4. **Configure Nginx + Gunicorn**
   - Use systemd service for Gunicorn
   - Configure Nginx reverse proxy

5. **Set up SSL**
   ```bash
   sudo apt install certbot python3-certbot-nginx
   sudo certbot --nginx
   ```

**Cost:** ~$10-20/month (instance) + ~$15/month (RDS if separate)

---

## Pre-Deployment Checklist

Before deploying to production, ensure:

### Security
- [ ] Change `SECRET_KEY` to a secure random value
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS` with your domain
- [ ] Set up SSL/HTTPS (most platforms do this automatically)
- [ ] Review Django security checklist: `python manage.py check --deploy`

### Database
- [ ] Migrate from SQLite to PostgreSQL (production-ready)
- [ ] Backup existing data if migrating
- [ ] Test migrations on production database

### Static Files
- [ ] Run `python manage.py collectstatic`
- [ ] Configure static file serving (WhiteNoise or CDN)
- [ ] Test static files load correctly

### Media Files
- [ ] For production, consider cloud storage (AWS S3, Cloudinary)
- [ ] Configure `MEDIA_ROOT` and `MEDIA_URL`

### Environment Variables
- [ ] Set `SECRET_KEY` (never commit to git!)
- [ ] Set `DEBUG=False`
- [ ] Set `ALLOWED_HOSTS`
- [ ] Configure `DATABASE_URL`
- [ ] Set email credentials (optional)

### Testing
- [ ] Test all CRUD operations
- [ ] Test user authentication
- [ ] Test file uploads (if applicable)
- [ ] Check error pages (404, 500)

---

## Post-Deployment Steps

### 1. Run Database Migrations

```bash
# Railway
railway run python manage.py migrate

# Render (via shell)
render:shell
python manage.py migrate

# Fly.io
fly ssh console -C "python manage.py migrate"

# AWS (SSH or EB CLI)
eb ssh
python manage.py migrate
```

### 2. Create Superuser

```bash
# Same as above, but run:
python manage.py createsuperuser
```

### 3. Verify Deployment

- [ ] Visit your app URL
- [ ] Test login/registration
- [ ] Check static files load
- [ ] Test creating a product
- [ ] Verify admin panel works

### 4. Set Up Monitoring (Optional)

- **Sentry** for error tracking
- **Uptime Robot** for uptime monitoring
- Platform-native monitoring (Railway, Render have built-in)

### 5. Configure Domain (Optional)

Most platforms allow custom domains:
- Railway: Settings → Domains
- Render: Settings → Custom Domains
- Fly.io: `fly domains add yourdomain.com`

---

## Generating a Secure SECRET_KEY

```python
from django.core.management.utils import get_random_secret_key
print(get_random_secret_key())
```

Or use online tools (trusted sources only):
- Django's secret key generator
- Random.org

**Never commit SECRET_KEY to git!**

---

## Troubleshooting

### Static Files Not Loading
- Ensure `collectstatic` ran: `python manage.py collectstatic --noinput`
- Check `STATIC_ROOT` configuration
- Verify WhiteNoise middleware is active (if using)

### Database Connection Issues
- Verify `DATABASE_URL` format: `postgresql://user:pass@host:port/dbname`
- Check database credentials
- Ensure database exists

### 500 Errors in Production
- Check platform logs
- Enable Django error emails (configure email settings)
- Use Sentry for error tracking

### Migration Errors
- Run `python manage.py makemigrations` locally first
- Test migrations locally with production database settings
- Use `--fake-initial` if needed (careful!)

---

## Recommendation Summary

**For Quickest Deployment:**
1. **Railway.app** - Best balance of ease and features
2. **Render.com** - If you need a free tier
3. **Fly.io** - If you want global edge deployment

**For Enterprise/Production:**
1. **AWS Elastic Beanstalk** - Managed, familiar
2. **AWS ECS Fargate** - Container-based, scalable
3. **AWS Lightsail** - Simple VPS-like setup

**For Learning:**
- Start with Railway or Render to get familiar
- Then try Docker + AWS for more control

---

## Need Help?

- Check platform-specific documentation
- Django deployment docs: https://docs.djangoproject.com/en/stable/howto/deployment/
- Platform communities and forums

---

**Good luck with your deployment! 🚀**

