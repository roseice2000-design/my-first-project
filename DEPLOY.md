# Quick Deployment Guide

## Option 1: Deploy to Railway (Recommended - Easiest)

1. **Sign up at Railway**
   - Visit https://railway.app
   - Sign up with GitHub

2. **Connect Your Repository**
   - Click "New Project"
   - Select "Deploy from GitHub"
   - Choose this repository
   - Select branch: `claude/property-booking-website-vjgko5`

3. **Configure**
   - Railway will auto-detect Node.js
   - Set environment variables (if needed):
     - `PORT=3000`
     - `NODE_ENV=production`

4. **Deploy**
   - Railway will automatically build and deploy
   - Your live URL will appear in the dashboard

---

## Option 2: Deploy to Heroku

1. **Install Heroku CLI**
   ```bash
   npm install -g heroku
   heroku login
   ```

2. **Create Heroku App**
   ```bash
   heroku create your-app-name
   ```

3. **Deploy**
   ```bash
   git push heroku claude/property-booking-website-vjgko5:main
   ```

4. **View Logs**
   ```bash
   heroku logs --tail
   ```

---

## Option 3: Deploy to Vercel

1. **Push to GitHub**
   ```bash
   git push origin claude/property-booking-website-vjgko5
   ```

2. **Import to Vercel**
   - Visit https://vercel.com/new
   - Import from GitHub
   - Select this repo
   - Deploy

**Note:** Vercel's serverless functions have limitations for long-running Node.js servers. Railway is recommended.

---

## After Deployment

1. Access your live site
2. Use `/import.html` to add more properties
3. Use `/admin.html` to manage bookings
4. Share the main URL with guests

---

## Database Setup

Current setup uses in-memory storage (data lost on restart).

For production, add a database:
- MongoDB Atlas (free tier available)
- PostgreSQL (via Railway)
- Firebase Realtime Database

Update `server.js` to use your database connection string.

---

## Environment Variables

Create a `.env` file:
```
PORT=3000
NODE_ENV=production
DATABASE_URL=your-database-url
```

---

## Troubleshooting

**Port Already in Use:**
```bash
lsof -i :3000
kill -9 <PID>
```

**Dependencies Not Installing:**
```bash
rm -rf node_modules package-lock.json
npm install
```

**Properties Not Persisting:**
Database setup required. See "Database Setup" section above.

---

**Questions?** Check the README.md for more information.
