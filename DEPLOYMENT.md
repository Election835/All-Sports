# Deployment Guide – All Sports on Render

This guide walks through deploying the All Sports application to Render.com.

## Prerequisites

- Render.com account (free tier available)
- GitHub repository with code pushed publicly
- NewsData.io API key (get free key at https://newsdata.io)

## Step 1: Connect GitHub to Render

1. Go to [render.com](https://render.com) and sign in
2. Click **New +** → **Web Service**
3. Click **Connect account** to link your GitHub
4. Authorize Render to access your GitHub repositories
5. Select the `all-sports` repository
6. Click **Connect**

## Step 2: Configure Deployment Settings

### Basic Configuration
- **Name:** `all-sports` (or your preferred name)
- **Environment:** `Python 3`
- **Region:** Choose closest to your users (e.g., `US West` for US)
- **Branch:** `main`

### Build & Start Commands
- **Build Command:** 
  ```
  pip install -r requirements.txt
  ```
- **Start Command:** 
  ```
  gunicorn -w 4 -b 0.0.0.0:5000 app:app
  ```

### Environment Variables
Click **Add Environment Variable** and add:
- **Key:** `GNEWS_API_KEY`
- **Value:** Your NewsData.io API key (from https://newsdata.io/api)

### Advanced Settings (Optional)
- **Auto-Deploy:** Enabled (recommended)
- **Health Check Path:** `/` (default)

## Step 3: Deploy

1. Click **Create Web Service**
2. Render will:
   - Clone your repository
   - Install Python dependencies from `requirements.txt`
   - Start the Gunicorn server
   - Provide a public URL (e.g., `https://all-sports-abc123.onrender.com`)

Deployment typically takes 2-3 minutes. Check the deploy logs for any errors.

## Step 4: Verify Deployment

1. Once deployed, click the URL provided by Render
2. Verify the homepage loads correctly
3. Test each sport category (NFL, NBA, etc.)
4. Test searching for a team (e.g., "Lakers")
5. Test saving/loading favorites

## Monitoring & Debugging

### View Logs
- Click **Logs** in Render dashboard to see real-time output
- Look for error messages during API calls or database operations

### Common Issues

**Issue: "GNEWS_API_KEY not found"**
- Solution: Verify the environment variable is set in Render Settings
- Wait 30 seconds after adding the variable for it to take effect

**Issue: "Database is locked"**
- Solution: SQLite works on Render, but avoid concurrent writes
- For production scale, consider migrating to PostgreSQL

**Issue: "503 Bad Gateway"**
- Solution: Check logs for errors; restart the service from Render dashboard
- May indicate API timeout—check NewsData.io status

**Issue: Deployment keeps failing**
- Verify `requirements.txt` has all dependencies
- Check `gunicorn` is in `requirements.txt`
- Ensure no syntax errors in `app.py`

## Production Checklist

- [ ] `.env` file NOT committed to GitHub (check `.gitignore`)
- [ ] Environment variable set in Render
- [ ] All sport categories tested (NFL, NBA, MLB, NHL, Soccer)
- [ ] Team search tested (Lakers, Falcons, Yankees)
- [ ] Save/remove favorites working
- [ ] Empty state displays when no favorites
- [ ] Error messages display on API failure
- [ ] Mobile responsive layout working

## Advanced: Custom Domain

1. In Render dashboard, click **Settings** for your service
2. Scroll to **Custom Domains**
3. Add your domain (requires DNS configuration)
4. Follow Render's DNS instructions

## Auto-Deploy on GitHub Push

By default, Render auto-deploys when you push to the `main` branch:

```bash
# Make changes locally
git add .
git commit -m "Fix: improve article filtering"
git push origin main

# Render automatically detects the push and redeploys
# Check Render dashboard for deployment status
```

To disable auto-deploy or choose specific branches:
- Go to Render **Settings** → **Auto-Deploy**
- Select **Manual Deploy** or configure branch filter

## Scaling Considerations

Current setup uses:
- **Plan:** Free or Starter tier
- **Instances:** Single instance with auto-restart on failure
- **Database:** SQLite (suitable for small/medium traffic)

For production scale (1000+ daily users):
- Migrate SQLite to PostgreSQL (Render offers managed Postgres)
- Increase Gunicorn workers: `-w 8` or higher
- Add caching layer (Redis) for API responses
- Implement request rate limiting

## Rollback

To revert to a previous deployment:
1. Go to Render dashboard for your service
2. Click **Deploys** tab
3. Find the previous successful deployment
4. Click **Redeploy** on that deployment

This will revert code to that point in time.

## Support

- Render docs: https://render.com/docs
- Flask deployment: https://flask.palletsprojects.com/deployment/
- Gunicorn docs: https://gunicorn.org/

