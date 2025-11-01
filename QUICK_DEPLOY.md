# Quick Deployment Guide - Choose Your Path

## 🚀 Fastest Option: Railway.app (Recommended)

**Deploy from GitHub in 5 minutes!**

### Steps:
1. Push your code to GitHub
2. Go to [railway.app](https://railway.app) and sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Railway will auto-detect your app and deploy
6. Add environment variables:
   - `SECRET_KEY` - Run `python generate_secret_key.py` to generate
   - `DEBUG=False`
   - `ALLOWED_HOSTS=your-app-name.railway.app`
7. Add PostgreSQL database (Railway → New → Database → PostgreSQL)
8. Run migrations: Railway dashboard → Deployments → Run Command → `python manage.py migrate`
9. Create superuser: Railway dashboard → Run Command → `python manage.py createsuperuser`

**Done! Your app is live.** ✨

---

## 💰 Budget Option: Render.com (Free Tier Available)

1. Go to [render.com](https://render.com) and sign up
2. New + → Web Service
3. Connect GitHub repo
4. Settings:
   - Build Command: `pip install -r requirements.txt && python manage.py collectstatic --noinput`
   - Start Command: `gunicorn inventory_management.wsgi:application --bind 0.0.0.0:$PORT`
5. Add PostgreSQL database (New + → PostgreSQL)
6. Set environment variables (same as Railway)
7. Deploy!

**Note:** Free tier spins down after 15 min inactivity (first request will be slow)

---

## 🌍 Global Option: Fly.io

1. Install Fly CLI: `iwr https://fly.io/install.ps1 -useb | iex`
2. `fly auth login`
3. `fly launch` (follow prompts)
4. `fly secrets set SECRET_KEY=<your-key> DEBUG=False`
5. `fly postgres create --name inventory-db`
6. `fly postgres attach inventory-db`
7. `fly deploy`
8. `fly ssh console -C "python manage.py migrate && python manage.py createsuperuser"`

**Done!**

---

## 🐳 Docker Option (For AWS, DigitalOcean, etc.)

If you want to use Docker on any platform:

1. **Build locally:**
   ```bash
   docker build -t inventory-management .
   ```

2. **Run locally (test):**
   ```bash
   docker-compose up
   ```

3. **Push to registry (Docker Hub, AWS ECR, etc.)**
   ```bash
   docker tag inventory-management:latest yourusername/inventory-management:latest
   docker push yourusername/inventory-management:latest
   ```

4. **Deploy to your platform:**
   - AWS ECS, DigitalOcean App Platform, Google Cloud Run, Azure Container Instances, etc.
   - All support Docker images!

---

## ⚙️ Environment Variables You Need

Set these on your platform:

```
SECRET_KEY=<run python generate_secret_key.py to get one>
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
DATABASE_URL=<provided by platform or PostgreSQL connection string>
```

---

## 📝 After Deployment

1. Run migrations:
   ```bash
   python manage.py migrate
   ```

2. Create superuser:
   ```bash
   python manage.py createsuperuser
   ```

3. Visit your app URL and test!

---

## 🆚 Which Should You Choose?

- **Railway** → Easiest, great for beginners, $5/month free credit
- **Render** → Free tier available, good for testing
- **Fly.io** → Fast global deployment, generous free tier
- **Docker + AWS** → Most control, scalable, more setup required

**Recommendation:** Start with Railway, then move to Docker/AWS if you need more control.

---

See `DEPLOYMENT_GUIDE.md` for detailed instructions for each platform.

