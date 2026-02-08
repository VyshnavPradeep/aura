# 🚀 Aura Deployment Guide - 100% Free Hosting

Deploy your Aura security analysis application for **FREE** using Render (backend) and Vercel (frontend).

## 📋 Prerequisites

- ✅ GitHub account (free)
- ✅ Code pushed to GitHub repository
- ✅ Gemini API key ([Get it here](https://aistudio.google.com/app/apikey))

**No credit card required for either platform!**

---

## 🔧 Part 1: Deploy Backend on Render

### Step 1: Sign Up for Render

1. Go to [render.com](https://render.com)
2. Click "Get Started for Free"
3. Sign up with GitHub (recommended) or email
4. No credit card required!

### Step 2: Create Web Service

1. Click "New +" → "Web Service"
2. Connect your GitHub account if not already connected
3. Select your repository: `VyshnavPradeep/aura`
4. Click "Connect"

### Step 3: Configure Service

Fill in the following settings:

| Setting | Value |
|---------|-------|
| **Name** | `aura-backend` (or any name you prefer) |
| **Region** | Choose closest to you |
| **Root Directory** | `aura-main` |
| **Environment** | `Python 3` |
| **Build Command** | `pip install -r requirements.txt` |
| **Start Command** | `uvicorn main:app --host 0.0.0.0 --port $PORT` |
| **Instance Type** | `Free` |

### Step 4: Add Environment Variables

Click "Advanced" → "Add Environment Variable":

```
GEMINI_API_KEY=your_actual_api_key_here
ENVIRONMENT=production
ALLOWED_ORIGINS=*
```

> **Important**: Replace `your_actual_api_key_here` with your real Gemini API key

### Step 5: Deploy!

1. Click "Create Web Service"
2. Wait 5-10 minutes for deployment
3. Your backend will be live at: `https://aura-backend-xxxx.onrender.com`

### Step 6: Test Backend

Visit: `https://your-backend-url.onrender.com/docs`

You should see the FastAPI Swagger documentation!

---

## 🎨 Part 2: Deploy Frontend on Vercel

### Step 1: Sign Up for Vercel

1. Go to [vercel.com](https://vercel.com)
2. Click "Start Deploying"
3. Sign up with GitHub (recommended)
4. No credit card required!

### Step 2: Import Project

1. Click "Add New..." → "Project"
2. Import your GitHub repository: `VyshnavPradeep/aura`
3. Click "Import"

### Step 3: Configure Project

| Setting | Value |
|---------|-------|
| **Framework Preset** | Next.js (auto-detected) |
| **Root Directory** | `aura-main/frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |
| **Install Command** | `npm install` (default) |

### Step 4: Add Environment Variable

Click "Environment Variables" and add:

```
NEXT_PUBLIC_API_URL=https://your-backend-url.onrender.com
```

> **Important**: Replace with your actual Render backend URL from Part 1

### Step 5: Deploy!

1. Click "Deploy"
2. Wait 2-3 minutes for build
3. Your frontend will be live at: `https://your-project.vercel.app`

---

## ✅ Verification

### Test Your Deployment

1. **Visit your frontend URL**: `https://your-project.vercel.app`
2. **Check the dashboard** loads with the creative design
3. **Test file upload**:
   - Upload a sample ZIP file with code
   - Wait for analysis to complete
   - Verify results display correctly

### Check Backend API

Visit: `https://your-backend-url.onrender.com/docs`

Test endpoints:
- ✅ GET `/upload/projects` - Should return empty array initially
- ✅ POST `/upload/` - Upload a test file
- ✅ POST `/analyze/{project_id}` - Run analysis

---

## 🔄 Update CORS Settings (If Needed)

If you get CORS errors, update the backend:

1. Go to your Render dashboard
2. Click on your service
3. Go to "Environment"
4. Update `ALLOWED_ORIGINS` to your Vercel URL:
   ```
   ALLOWED_ORIGINS=https://your-project.vercel.app
   ```
5. Service will auto-redeploy

---

## 📊 Free Tier Limits

### Render Free Tier
- ✅ 750 hours/month (24/7 uptime)
- ✅ 512 MB RAM
- ⚠️ Sleeps after 15 min inactivity (wakes on first request in ~30 sec)
- ✅ Automatic HTTPS
- ✅ No credit card required

### Vercel Free Tier
- ✅ Unlimited deployments
- ✅ 100 GB bandwidth/month
- ✅ Automatic HTTPS
- ✅ Global CDN
- ✅ No credit card required

---

## 🐛 Troubleshooting

### Backend Issues

**Problem**: Build fails on Render
- **Solution**: Check build logs, ensure `requirements.txt` is correct
- Try updating Python version in `runtime.txt` to `python-3.11.0`

**Problem**: Backend sleeps after 15 minutes
- **Solution**: This is normal for free tier. First request wakes it up (~30 sec)
- Consider using [UptimeRobot](https://uptimerobot.com) (free) to ping every 5 min

**Problem**: Import errors
- **Solution**: Some packages might not install on free tier (limited RAM)
- Comment out heavy packages like `semgrep` if needed

### Frontend Issues

**Problem**: API calls fail with CORS error
- **Solution**: Update `ALLOWED_ORIGINS` in Render environment variables

**Problem**: Environment variable not working
- **Solution**: Ensure it starts with `NEXT_PUBLIC_` for client-side access
- Redeploy after adding environment variables

**Problem**: Build fails
- **Solution**: Check Vercel build logs
- Ensure `package.json` has all dependencies

---

## 🎯 Next Steps

### After Successful Deployment

1. **Update README** with live demo links
2. **Share your app** with the world!
3. **Monitor usage** in Render and Vercel dashboards
4. **Set up custom domain** (optional, free with Vercel)

### Optional Enhancements

1. **Add monitoring**: Use Render's built-in monitoring
2. **Set up alerts**: Get notified of downtime
3. **Custom domain**: Add your own domain in Vercel settings
4. **Analytics**: Add Vercel Analytics (free tier available)

---

## 🆘 Need Help?

- **Render Docs**: https://render.com/docs
- **Vercel Docs**: https://vercel.com/docs
- **Check logs**: Both platforms provide detailed deployment logs

---

## 🎉 Success!

Your Aura application is now live and accessible worldwide for **FREE**!

- 🌐 **Frontend**: `https://your-project.vercel.app`
- 🔧 **Backend**: `https://your-backend.onrender.com`
- 📚 **API Docs**: `https://your-backend.onrender.com/docs`

Share it with your friends and start analyzing code for security vulnerabilities! 🚀
