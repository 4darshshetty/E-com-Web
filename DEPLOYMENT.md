# Deployment Guide - Advanced E-Commerce Application

## 🚀 Deployment Steps

### Prerequisites
- GitHub account
- Node.js installed
- Python 3.8+ installed
- MongoDB Atlas account (for production) or local MongoDB

### Step 1: Prepare for Deployment

#### Backend Deployment (Python/FastAPI)

1. **Create `Procfile` for Heroku/Railway:**
```
web: uvicorn main:app --host 0.0.0.0 --port $PORT
```

2. **Create `runtime.txt`:**
```
python-3.11.0
```

3. **Update `requirements.txt`** (already done)

4. **Create `.env` file template:**
```env
MONGO_URL=mongodb+srv://username:password@cluster.mongodb.net/ecommerce_db
STRIPE_SECRET_KEY=sk_live_your_stripe_key
STRIPE_PUBLISHABLE_KEY=pk_live_your_stripe_key
SECRET_KEY=your_secret_key_here
```

#### Frontend Deployment (React)

1. **Update `package.json` scripts:**
```json
"scripts": {
  "start": "react-scripts start",
  "build": "react-scripts build",
  "predeploy": "npm run build",
  "deploy": "gh-pages -d build"
}
```

2. **Create `.env.production`:**
```
REACT_APP_API_URL=https://your-backend-url.herokuapp.com
REACT_APP_STRIPE_KEY=pk_live_your_stripe_key
```

### Step 2: Deploy Backend

#### Option A: Railway (Recommended)
1. Go to [railway.app](https://railway.app)
2. Click "New Project"
3. Select "Deploy from GitHub repo"
4. Connect your repository
5. Select the `backend` folder
6. Add environment variables
7. Deploy!

#### Option B: Heroku
```bash
cd backend
heroku create your-app-name
heroku addons:create mongolab:sandbox
heroku config:set MONGO_URL=your_mongodb_url
git push heroku main
```

#### Option C: Render
1. Go to [render.com](https://render.com)
2. Create new Web Service
3. Connect GitHub repository
4. Set root directory to `backend`
5. Build command: `pip install -r requirements.txt`
6. Start command: `uvicorn main:app --host 0.0.0.0 --port $PORT`

### Step 3: Deploy Frontend

#### Option A: Vercel (Recommended)
```bash
cd frontend
npm install -g vercel
vercel
# Follow prompts
```

#### Option B: Netlify
```bash
cd frontend
npm run build
# Drag and drop the 'build' folder to Netlify
```

#### Option C: GitHub Pages
```bash
cd frontend
npm install --save-dev gh-pages
# Add to package.json:
# "homepage": "https://yourusername.github.io/your-repo-name"
npm run build
npm run deploy
```

### Step 4: Configure CORS

Update backend `main.py`:
```python
allow_origins=[
    "http://localhost:3000",
    "https://your-frontend-domain.vercel.app",
    "https://your-frontend-domain.netlify.app"
]
```

### Step 5: Environment Variables

#### Backend (.env)
- `MONGO_URL`: MongoDB connection string
- `STRIPE_SECRET_KEY`: Stripe secret key
- `SECRET_KEY`: JWT secret key

#### Frontend (.env.production)
- `REACT_APP_API_URL`: Backend API URL
- `REACT_APP_STRIPE_KEY`: Stripe publishable key

### Step 6: MongoDB Atlas Setup

1. Create account at [mongodb.com/cloud/atlas](https://www.mongodb.com/cloud/atlas)
2. Create cluster
3. Create database user
4. Whitelist IP addresses (0.0.0.0/0 for all)
5. Get connection string
6. Update `MONGO_URL` in backend environment variables

### Step 7: Stripe Setup

1. Create account at [stripe.com](https://stripe.com)
2. Get API keys from dashboard
3. Add to environment variables
4. Update frontend with publishable key

### Step 8: Final Steps

1. **Test the deployment:**
   - Check backend health: `https://your-backend.railway.app/docs`
   - Test frontend: `https://your-frontend.vercel.app`

2. **Update API URLs:**
   - Update `frontend/src/api.js` with production URL
   - Rebuild and redeploy frontend

3. **Set up custom domain (optional):**
   - Add domain in Vercel/Netlify settings
   - Update CORS in backend

## 📋 Post-Deployment Checklist

- [ ] Backend API is accessible
- [ ] Frontend connects to backend
- [ ] MongoDB connection works
- [ ] Payment integration works (test mode)
- [ ] Admin dashboard accessible
- [ ] User registration/login works
- [ ] Product display works
- [ ] Cart functionality works
- [ ] Order placement works
- [ ] Shipping tracker works
- [ ] Map integration works

## 🔒 Security Checklist

- [ ] Environment variables are set (not in code)
- [ ] CORS is properly configured
- [ ] JWT secret is strong and secure
- [ ] MongoDB credentials are secure
- [ ] Stripe keys are production keys
- [ ] HTTPS is enabled
- [ ] Admin routes are protected

## 🐛 Troubleshooting

### Backend Issues
- Check logs: `heroku logs --tail` or Railway logs
- Verify MongoDB connection string
- Check CORS settings
- Verify environment variables

### Frontend Issues
- Check browser console for errors
- Verify API URL in `.env.production`
- Check network tab for API calls
- Verify build completed successfully

### Common Errors
- **CORS Error**: Update backend CORS origins
- **404 Error**: Check API routes
- **500 Error**: Check backend logs
- **MongoDB Error**: Verify connection string

## 📚 Additional Resources

- [FastAPI Deployment](https://fastapi.tiangolo.com/deployment/)
- [React Deployment](https://create-react-app.dev/docs/deployment/)
- [MongoDB Atlas](https://docs.atlas.mongodb.com/)
- [Stripe Docs](https://stripe.com/docs)

