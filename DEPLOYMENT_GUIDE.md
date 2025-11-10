# 🌐 DEPLOYMENT GUIDE

## Deploy Your Emotion Detection App

---

## ⭐ Recommended: Render.com (FREE)

### Step 1: Create Render Account
1. Go to https://render.com
2. Sign up (free account)
3. Verify email

### Step 2: Connect GitHub
1. Click "New +" → "Web Service"
2. Click "Connect account" for GitHub
3. Authorize Render
4. Select your repository

### Step 3: Configure Service
1. **Name**: emotion-detection-app
2. **Environment**: Python 3
3. **Build Command**: `pip install -r requirements.txt`
4. **Start Command**: `gunicorn app:app`
5. **Plan**: Free
6. Click "Create Web Service"

### Step 4: Wait for Deployment
- Build takes 2-3 minutes
- Deploy takes 1-2 minutes
- You'll see "Live" when done

### Step 5: Get Your URL
- Copy the service URL from dashboard
- Format: `https://your-app-name.onrender.com`

### Step 6: Update link_to_my_web_app.txt
Replace content with:
```
Render - https://your-app-name.onrender.com
```

### Step 7: Push Changes
```bash
git add link_to_my_web_app.txt
git commit -m "Update deployed URL"
git push origin main
```

---

## 🚂 Alternative: Railway.app (FREE)

### Step 1: Create Account
1. Go to https://railway.app
2. Sign up with GitHub
3. Create new project

### Step 2: Deploy from GitHub
1. Click "GitHub Repo"
2. Select your repository
3. Authorize and connect

### Step 3: Configure
1. No configuration needed (auto-detected)
2. Deployment starts automatically
3. Wait for "Active" status

### Step 4: Get URL
- Click "Settings" → "Domains"
- Generate domain
- Copy the URL

### Step 5: Update Link File
```
Railway - https://your-app-name.up.railway.app
```

---

## 🟣 Alternative: Heroku (Requires Credit Card)

### Step 1: Create Heroku Account
1. Go to https://heroku.com
2. Sign up (requires credit card for free tier)

### Step 2: Create App
1. Click "New" → "Create new app"
2. Enter app name
3. Select region (US)

### Step 3: Connect GitHub
1. Go to "Deploy" tab
2. Select "GitHub"
3. Connect GitHub account
4. Search and select repository

### Step 4: Deploy
1. Click "Deploy Branch"
2. Wait for deployment (3-5 min)
3. Click "View" to see live app

### Step 5: Update Link File
```
Heroku - https://your-app-name.herokuapp.com
```

---

## 🔒 Security Setup

### Before Deploying
1. Create `.env` file (local only):
   ```
   DEBUG=False
   PORT=10000
   ```

2. Update `.gitignore`:
   ```
   .env
   __pycache__/
   *.db
   uploads/
   .venv/
   ```

3. Don't commit `.env` to GitHub

### On Cloud Server
Environment variables are set in platform settings:
- **Render**: Environment tab
- **Railway**: Variables tab
- **Heroku**: Config Vars

---

## ✅ Post-Deployment Checklist

### Test Deployed App
```bash
# Test all endpoints
curl https://your-app.com/health
curl https://your-app.com/
curl https://your-app.com/api/emotion
```

### Verify Features
- [ ] Homepage loads
- [ ] Webcam section visible
- [ ] Upload section works
- [ ] History section appears
- [ ] Styles load correctly
- [ ] No console errors

### Database
- [ ] Database auto-created
- [ ] Can upload images
- [ ] Can capture from webcam
- [ ] Data persists

---

## 🐛 Troubleshooting

### App Won't Start
**Error**: Build failed
**Solution**: 
- Check requirements.txt syntax
- Ensure gunicorn is installed
- Check Python version compatibility

### Webcam Not Working
**Expected**: Webcam won't work on cloud servers
**Solution**: Use image upload feature instead

### Database Connection Error
**Error**: Cannot connect to database
**Solution**: Database auto-creates in app directory

### 404 Errors
**Error**: Cannot find static files
**Solution**: Check Flask static folder configuration

---

## 📊 Monitoring

### Render Logs
1. Dashboard → Your app
2. Click "Logs" tab
3. See real-time logs

### Railway Logs
1. Project → Your app
2. Click "Logs"
3. View deployment logs

### Heroku Logs
```bash
heroku logs --tail -a your-app-name
```

---

## 🔄 Update Deployed App

### When You Push to GitHub
1. Changes auto-detected
2. Rebuild starts automatically
3. New version deployed
4. Takes 3-5 minutes

### Manual Redeploy (Render)
1. Go to dashboard
2. Click "Deploys"
3. Click "Deploy latest"

---

## 💾 Database Backup

### Download Database
**Render**:
```bash
# Via SSH into container
cd /opt/render/project/src
sqlite3 emotion_detection_results.db ".dump" > backup.sql
```

**Railway**:
```bash
# Similar process via Railway shell
```

### Backup to GitHub (Optional)
```bash
# Create backup directory
mkdir backups

# Copy database
cp emotion_detection_results.db backups/backup_$(date +%Y%m%d).db

# Commit
git add backups/
git commit -m "Database backup"
git push
```

---

## 🚀 Performance Tips

### Optimize for Cloud
1. Use image resize in upload
2. Implement rate limiting
3. Cache model in memory
4. Use CDN for static files

### Monitor Usage
- Track database size
- Monitor uploads folder
- Check daily active users
- Analyze error logs

---

## 🛡️ Production Checklist

```
Deployment
□ Application deployed
□ URL obtained
□ Domain configured
□ HTTPS enabled

Testing
□ All endpoints working
□ Database persisting
□ Uploads storing
□ History retrieving
□ Statistics calculating

Monitoring
□ Logs accessible
□ Error alerts set
□ Performance acceptable
□ No 404 errors

Security
□ Debug mode off
□ Environment variables set
□ HTTPS enforced
□ Input validation working
□ File size limits enforced
```

---

## 📞 Platform Support

### Render Support
- Docs: https://render.com/docs
- Status: https://render-status.com
- Email: support@render.com

### Railway Support
- Docs: https://docs.railway.app
- Discord: https://railway.app/discord
- Status: https://status.railway.app

### Heroku Support
- Docs: https://devcenter.heroku.com
- Forum: https://help.heroku.com
- Support: https://help.heroku.com/contact-us

---

## 💡 Cost Overview

| Platform | Free Tier | Cost After |
|----------|-----------|-----------|
| **Render** | ✅ Limited | $7/month |
| **Railway** | ✅ $5/month | $5+ /month |
| **Heroku** | ❌ Discontinued | Paid only |
| **Local Dev** | ✅ Free | Free |

---

## 🎯 Next Steps

1. **Choose Platform**: Render recommended
2. **Deploy**: Follow steps above
3. **Test**: Verify all features
4. **Document**: Update link file
5. **Submit**: Provide URL to graders

---

## 📝 Update Instructions

### After Deployment
```bash
# Update link file
echo "Render - https://your-app.onrender.com" > link_to_my_web_app.txt

# Commit changes
git add link_to_my_web_app.txt
git commit -m "Add deployed app URL"

# Push
git push origin main
```

### For Graders
Provide them:
1. GitHub repository URL
2. Deployed app URL
3. Any credentials (if needed)

---

## ✨ Final Notes

- **No credit card needed** for Render or Railway free tiers
- **Deployment takes 5-10 minutes** total
- **Auto-rebuilds on git push** (most platforms)
- **Database persists** on cloud storage
- **Free tier is production-ready** for projects

---

**Ready to deploy? Pick Render and follow the steps above!** 🚀

---

*Last Updated: November 10, 2025*
