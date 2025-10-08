# 🚀 Deployment Guide - Streamlit Cloud

## Quick Deploy to Streamlit Cloud

### Prerequisites
- GitHub account
- OpenAI API key
- Code pushed to GitHub repository

---

## Step-by-Step Deployment

### 1. **Push Code to GitHub**

```bash
# Make sure all changes are committed
git add -A
git commit -m "Ready for deployment"

# Push to GitHub (setup authentication first if needed)
git push origin main
```

### 2. **Deploy to Streamlit Cloud**

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Click **"New app"**
3. Select your repository: `Lakshmi-Sindhu-P/ai-email-generator`
4. **Main file path:** `scripts/app.py`
5. **Branch:** `main`
6. Click **"Deploy"**

### 3. **Configure Secrets**

Once deployed, you'll see a configuration error. Fix it:

1. Click **"Settings"** (⚙️ icon in the bottom right)
2. Click **"Secrets"** in the sidebar
3. Add your secrets in TOML format:

```toml
OPENAI_API_KEY = "sk-your-actual-api-key-here"

# Optional overrides
OPENAI_MODEL = "gpt-3.5-turbo"
OPENAI_MAX_TOKENS = "350"
OPENAI_TEMPERATURE = "0.7"
```

4. Click **"Save"**
5. App will automatically restart with secrets

### 4. **Verify Deployment**

- App should now be running at: `https://your-app-name.streamlit.app`
- Test all features:
  - ✅ Generate emails
  - ✅ View history
  - ✅ Check settings
  - ✅ Test templates

---

## 🔒 Security Best Practices

### **Never:**
❌ Commit `.env` file to GitHub
❌ Hard-code API keys in code
❌ Share your secrets publicly
❌ Use production API keys in development

### **Always:**
✅ Use Streamlit secrets for sensitive data
✅ Use `.gitignore` to exclude `.env` files
✅ Rotate API keys if exposed
✅ Monitor API usage for unexpected spikes

---

## 🐛 Troubleshooting Deployment

### **Issue: "OPENAI_API_KEY not found"**

**Solution:**
1. Go to app Settings > Secrets
2. Add `OPENAI_API_KEY = "your_key"` (with quotes!)
3. Save and wait for restart

### **Issue: "Module not found"**

**Solution:**
- Ensure `requirements.txt` is in repository root
- Check all imports are listed
- Redeploy from Streamlit Cloud dashboard

### **Issue: "Database errors"**

**Solution:**
- Database creates automatically on first run
- Check logs in Streamlit Cloud app
- May need to reboot app (Settings > Reboot app)

### **Issue: "Import errors in pages"**

**Solution:**
- File structure must match: `scripts/app.py` and `scripts/pages/*.py`
- All imports should be relative to scripts directory
- Check that path modifications work in cloud environment

---

## ⚙️ Environment Differences

### **Local Development:**
- Uses `.env` file
- Database stored locally
- Logs in `logs/` directory
- Full file system access

### **Streamlit Cloud:**
- Uses Streamlit secrets
- Database in temporary storage (resets on redeploy!)
- Limited file system
- Read-only for most files

---

## 💾 Database Persistence on Cloud

**Important:** Streamlit Cloud uses temporary storage that resets on redeploy!

**Solutions:**

### Option 1: External Database (Recommended for Production)
```python
# Use PostgreSQL, MySQL, or cloud database
# Update config.py to support different DB backends
```

### Option 2: Downloadable Backups
- Implement export/import functionality
- Download database before redeploys
- Re-upload after deployment

### Option 3: Cloud Storage
- Store database in AWS S3, Google Cloud Storage, etc.
- Load on startup

---

## 📊 Monitoring Your Deployed App

### **Streamlit Cloud Dashboard:**
- View logs
- Monitor resource usage
- Check app status
- Reboot app if needed
- View deployment history

### **API Usage:**
- Monitor OpenAI dashboard for API costs
- Set up billing alerts
- Track usage patterns
- Optimize based on metrics

---

## 🔄 Updating Your Deployed App

### **Method 1: Git Push (Automatic)**
```bash
# Make changes locally
git add -A
git commit -m "Update feature"
git push origin main

# Streamlit Cloud auto-deploys on push!
```

### **Method 2: Manual Redeploy**
1. Go to Streamlit Cloud dashboard
2. Click "Reboot app"
3. Or click "..." > "Redeploy"

---

## 🌐 Custom Domain (Optional)

1. In Streamlit Cloud, go to app Settings
2. Click "General"
3. Add custom domain
4. Follow DNS configuration instructions
5. Wait for DNS propagation

---

## 📈 Scaling Considerations

### **Free Tier Limits:**
- 1 app
- Limited resources
- Community support

### **Paid Plans:**
- Multiple apps
- More resources
- Priority support
- Custom domains
- Password protection

---

## 🎯 Pre-Deployment Checklist

Before deploying, ensure:

- ✅ Code is pushed to GitHub
- ✅ All dependencies in requirements.txt
- ✅ `.env` excluded via `.gitignore`
- ✅ Main file path is `scripts/app.py`
- ✅ API key ready for secrets
- ✅ Tested locally
- ✅ No hardcoded secrets
- ✅ Error handling in place

---

## 📞 Support

### **Streamlit Cloud Issues:**
- [Streamlit Cloud Docs](https://docs.streamlit.io/streamlit-community-cloud)
- [Community Forum](https://discuss.streamlit.io/)
- [Status Page](https://streamlitstatus.com/)

### **App Issues:**
- Check app logs in Streamlit Cloud
- Review `logs/app.log` locally
- See main README.md for troubleshooting

---

## 🎉 You're Ready to Deploy!

Your app is now configured to work seamlessly on both:
- **Local development** (using `.env`)
- **Streamlit Cloud** (using secrets)

**Next:** Push to GitHub and deploy at [share.streamlit.io](https://share.streamlit.io)! 🚀

