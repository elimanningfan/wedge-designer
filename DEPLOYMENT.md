# 🚀 Deployment Guide: Share Your Wedge Designer

Deploy the interactive wedge designer to share with others worldwide!

---

## ⚡ Quick Deploy: Streamlit Community Cloud (Recommended)

**Best for:** Quick, free deployment with minimal setup

### Prerequisites
- GitHub account
- Repository pushed to GitHub ✅ (already done!)

### Steps

#### 1. Sign Up for Streamlit Cloud
- Go to **[share.streamlit.io](https://share.streamlit.io)**
- Click **"Sign up with GitHub"**
- Authorize Streamlit to access your repositories

#### 2. Deploy Your App
- Click **"New app"**
- Select:
  - **Repository:** `elimanningfan/wedge-designer`
  - **Branch:** `main`
  - **Main file path:** `app.py`
- Click **"Deploy!"**

#### 3. Wait for Deployment
- First deployment takes 5-10 minutes
- Streamlit installs all dependencies from `requirements.txt`
- Watch the logs for any errors

#### 4. Share Your Link!
Your app will be live at:
```
https://wedge-designer-[your-app-id].streamlit.app
```

**That's it!** Anyone can now access your wedge designer.

---

## ⚠️ Important: CadQuery Deployment Challenges

**Challenge:** CadQuery has large binary dependencies (165MB+ for `cadquery-ocp`)

### Potential Issues on Streamlit Cloud:
1. **Memory limits:** Free tier has 1GB RAM limit
2. **Build timeouts:** Large dependencies may timeout during install
3. **Binary compatibility:** `cadquery-ocp` requires specific system libraries

### Solutions:

#### Option A: Try It First (Recommended)
Just try deploying! Streamlit Cloud has improved and may handle CadQuery now.

**If it fails**, you'll see errors like:
- "Memory limit exceeded"
- "Build timeout"
- "Module not found"

#### Option B: Use Alternative Platform

If Streamlit Cloud doesn't work, try these alternatives:

---

## 🔷 Alternative: Railway (Easy, Generous Free Tier)

**Best for:** Apps with heavy dependencies

### Steps:

#### 1. Create Dockerfile
Already included in repo (see below)

#### 2. Sign Up for Railway
- Go to **[railway.app](https://railway.app)**
- Sign in with GitHub

#### 3. Deploy
- Click **"New Project"**
- Select **"Deploy from GitHub repo"**
- Choose `elimanningfan/wedge-designer`
- Railway auto-detects the app and deploys

#### 4. Configure Port
- Go to your app settings
- Add environment variable: `PORT=8501`
- Railway will assign a public URL

**Live in 3-5 minutes!**

---

## 🐳 Docker Deployment (Any Platform)

Create a `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app

# Install system dependencies for CadQuery
RUN apt-get update && apt-get install -y \\
    libgl1-mesa-glx \\
    libglib2.0-0 \\
    libsm6 \\
    libxext6 \\
    libxrender-dev \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Expose port
EXPOSE 8501

# Health check
HEALTHCHECK CMD curl --fail http://localhost:8501/_stcore/health

# Run Streamlit
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Deploy Docker Image To:
- **DigitalOcean App Platform:** $5/month
- **Google Cloud Run:** Pay per use (often free)
- **AWS ECS/Fargate:** Pay per use
- **Azure Container Apps:** Pay per use

---

## 🌊 Alternative: Render

**Best for:** Free hobby projects (sleeps after inactivity)

### Steps:

1. Go to **[render.com](https://render.com)**
2. Sign up with GitHub
3. Click **"New Web Service"**
4. Connect to `elimanningfan/wedge-designer`
5. Configure:
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `streamlit run app.py --server.port=$PORT`
   - **Environment:** Python 3.9
6. Deploy (free tier available)

---

## 📊 Deployment Comparison

| Platform | Free Tier | RAM | Build Time | Difficulty | Best For |
|----------|-----------|-----|------------|------------|----------|
| **Streamlit Cloud** | ✅ Yes | 1GB | Medium | ⭐ Easy | Quick demos |
| **Railway** | ✅ Limited | 8GB | Fast | ⭐⭐ Easy | Heavy apps |
| **Render** | ✅ Yes* | 512MB | Slow | ⭐⭐ Easy | Hobby projects |
| **Docker + Cloud** | ⚠️ Varies | Custom | Fast | ⭐⭐⭐ Medium | Production |

*Render free tier sleeps after 15min inactivity

---

## 🎯 Recommended Deployment Strategy

### 1. Try Streamlit Cloud First (5 minutes)
- Easiest option
- May work despite heavy dependencies
- Free forever
- **If successful, you're done!**

### 2. If That Fails, Use Railway (10 minutes)
- More generous resources
- Handles CadQuery better
- Still very easy to deploy
- Free tier: 500 hours/month

### 3. If You Need Production, Use Docker + Cloud Run
- Most reliable
- Scales automatically
- Pay only for usage
- Requires Docker knowledge

---

## 🔧 Configuration Files (Already Included)

✅ **`.streamlit/config.toml`** - Streamlit settings
✅ **`requirements.txt`** - Python dependencies
✅ **`packages.txt`** - System dependencies
✅ **`app.py`** - Main application

All ready for deployment!

---

## 🚦 Post-Deployment Checklist

After deploying:

- [ ] Test the live URL in your browser
- [ ] Adjust sliders - confirm UI responds
- [ ] Generate a wedge - confirm STEP file generation works
- [ ] Download a STEP file - confirm download works
- [ ] Test on mobile - confirm responsive design
- [ ] Share the URL with friends!

---

## 📝 Custom Domain (Optional)

### Streamlit Cloud:
- Free custom domains not supported
- Use provided `*.streamlit.app` URL

### Railway/Render:
- Add custom domain in settings
- Point DNS to their servers
- Free SSL certificate included

---

## 🐛 Troubleshooting Deployments

### "Module not found: cadquery"
**Solution:** Streamlit Cloud couldn't install CadQuery
- Try Railway or Docker deployment instead
- CadQuery needs binary dependencies not available on all platforms

### "Memory limit exceeded"
**Solution:** App uses too much RAM
- Use Railway (8GB limit) or paid tier
- Or optimize by lazy-loading CadQuery

### "Build timeout"
**Solution:** Dependencies take too long to install
- Use Railway (faster builds)
- Or pre-build Docker image

### "App keeps sleeping"
**Solution:** Free tier limitation (Render)
- Upgrade to paid tier ($7/month)
- Or accept 15min sleep delay
- Or use Streamlit Cloud (never sleeps)

---

## 💡 Pro Tips

### Optimize for Deployment:
1. **Add .gitignore for output files**
   ```
   output/step_files/*.step
   ```

2. **Add loading message** in app.py:
   ```python
   with st.spinner("Loading CadQuery (first time may take a moment)..."):
       import cadquery as cq
   ```

3. **Monitor usage** on your platform dashboard

4. **Set up alerts** for errors or downtime

---

## 🔗 Example Deployed Apps

After deployment, your app will be accessible like:

- **Streamlit Cloud:** `https://wedge-designer-xyz.streamlit.app`
- **Railway:** `https://wedge-designer-production-abc.up.railway.app`
- **Render:** `https://wedge-designer.onrender.com`

**Anyone with the link can design wedges!**

---

## 🎉 Next Steps After Deployment

1. **Share on social media** (Twitter, LinkedIn, Reddit)
2. **Add to your portfolio** (showcase on your website)
3. **Submit to Streamlit gallery** (free promotion)
4. **Get feedback** from golf enthusiasts
5. **Iterate** based on user feedback

---

## 📞 Need Help?

- **Streamlit Cloud Docs:** [docs.streamlit.io/streamlit-community-cloud](https://docs.streamlit.io/streamlit-community-cloud)
- **Railway Docs:** [docs.railway.app](https://docs.railway.app)
- **Render Docs:** [render.com/docs](https://render.com/docs)
- **GitHub Issues:** Report problems at your repo

---

## 🏌️ Share Your Wedge Designer!

Once deployed, anyone in the world can:
- Design custom wedges
- Adjust parameters in real-time
- Download STEP files for manufacturing
- Learn about wedge design

**No installation required. Just share the link!**

---

**Ready to deploy?** Start with Streamlit Cloud (easiest) and fall back to Railway if needed!
