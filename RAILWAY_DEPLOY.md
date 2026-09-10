# Deploy to Railway.app - Step by Step Guide

## 🚀 Complete Deployment Steps

### Step 1: Create Railway Account
1. Go to **https://railway.app**
2. Click **"Start Project"** 
3. Sign up with GitHub (recommended)
4. Authorize Railway to access your GitHub account

### Step 2: Create New Project
1. Click **"New Project"** button
2. Select **"Deploy from GitHub"** option
3. Search for: **roseice2000-design/my-first-project**
4. Select the repository

### Step 3: Select Branch
1. When asked to select branch, choose:
   ```
   claude/property-booking-website-vjgko5
   ```
2. Click **"Deploy"**

### Step 4: Configure (Auto-detected)
Railway will automatically:
- ✅ Detect Node.js runtime
- ✅ Install dependencies (`npm install`)
- ✅ Run start command (`npm start`)
- ✅ Assign a public URL

### Step 5: Wait for Deployment
- Green checkmark = Deployment complete ✅
- Takes about 2-3 minutes
- You'll see deployment logs in real-time

### Step 6: Get Your Live URL
1. Click on the deployed project
2. Look for **"Public URL"** or **"Domains"** section
3. Your URL will look like: `https://your-app.railway.app`

---

## 📱 Test Your Site

Once deployed, visit:
- **Main Site**: `https://your-app.railway.app/`
- **Import Tool**: `https://your-app.railway.app/import.html`
- **Admin Panel**: `https://your-app.railway.app/admin.html`

### Test Booking Flow:
1. Click on property card
2. Select check-in and check-out dates
3. Enter guest details
4. Get confirmation code
5. Search booking using code

---

## 🔧 If Deployment Fails

### Check Build Logs:
1. Go to your Railway project
2. Click **"Deployments"** tab
3. Click latest deployment
4. View **"Build Logs"** for errors

### Common Issues & Fixes:

**Error: "npm install failed"**
- Solution: Check internet connection, retry deployment

**Error: "Port already in use"**
- Solution: Railway handles this automatically

**Error: "Cannot find module"**
- Solution: Ensure `package.json` is correct
  ```bash
  npm install
  git push origin claude/property-booking-website-vjgko5
  ```

**Site shows 404**
- Solution: Wait 1-2 minutes for full deployment
- Check URL is correct (with public domain)

---

## 📧 Share Your Booking Link

Once live, share this with guests:
```
Book your stay: https://your-app.railway.app/
```

They can:
- View your Drouin property
- Check availability
- Make bookings directly
- Get confirmation code

---

## 🔄 Future Updates

To update your site after deployment:

```bash
# Make changes locally
git add .
git commit -m "your message"
git push origin claude/property-booking-website-vjgko5

# Railway auto-redeploys from GitHub
# Your site updates automatically! ✨
```

---

## 💡 Pro Tips

- Railway includes **1GB free storage** per month
- **Auto-redeploy** when you push to GitHub
- **Free SSL certificate** (HTTPS included)
- **Environment variables** available in Railway dashboard
- Set custom domain if you own one

---

## 🎯 Next Steps After Deployment

1. ✅ Test the booking form
2. ✅ Create test booking and check confirmation
3. ✅ Use admin panel to view bookings
4. ✅ Try import tool to add more properties
5. ✅ Share booking link with potential guests

---

## 📞 Troubleshooting Support

If you get stuck:
1. Check Railway deployment logs
2. Verify GitHub branch is correct
3. Ensure `package.json` exists
4. Check that `server.js` is in root directory

**All files are ready.** Just deploy! 🚀

---

## ✅ Verification Checklist

After deployment, verify:

- [ ] Site loads at your Railway URL
- [ ] Homepage displays property
- [ ] Can click "View Details" on property
- [ ] Booking modal opens
- [ ] Price calculation works
- [ ] Can submit booking form
- [ ] Confirmation code appears
- [ ] Admin panel accessible
- [ ] Can view bookings in admin
- [ ] Import tool works

---

**You're ready! Deploy now and share your booking link!** 🌍

Questions? Check the logs or reach out!
