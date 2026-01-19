# Quick Start Guide

## Prerequisites Check
- [ ] Node.js installed (`node --version`)
- [ ] Python 3.8+ installed (`python --version`)
- [ ] MongoDB running on `localhost:27017`
- [ ] g++ compiler installed (for C++ engine, optional)

## Step-by-Step Setup

### 1. Build C++ Engine (Optional)
```bash
cd cpp-engine
# Windows:
build.bat
# Linux/Mac:
chmod +x build.sh && ./build.sh
```

### 2. Start Backend
```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```
Backend runs on: http://127.0.0.1:8000

### 3. Start Frontend
```bash
cd frontend
npm install
npm start
```
Frontend runs on: http://localhost:3000

## First Steps

1. Open http://localhost:3000
2. Click "Sign up" to create an account
3. Login with your credentials
4. Browse products and add to cart
5. Place an order with optional coupon code

## Creating Admin User

To create an admin user, sign up normally, then update MongoDB:

```javascript
use ecommerce_db
db.users.updateOne(
  { email: "your-email@example.com" },
  { $set: { role: "admin" } }
)
```

Then login again to access the admin dashboard.

## Testing the Application

1. **Sign Up**: Create a new user account
2. **Login**: Authenticate with your credentials
3. **Browse**: View products on the Products page
4. **Cart**: Add items and place orders
5. **Track**: View your order history
6. **Admin**: (If admin) Add new products

## Troubleshooting

- **Backend won't start**: Check MongoDB is running
- **Frontend won't start**: Run `npm install` first
- **C++ engine errors**: Backend will use Python fallback automatically
- **401 errors**: Make sure you're logged in
- **CORS errors**: Backend CORS is configured for localhost:3000

