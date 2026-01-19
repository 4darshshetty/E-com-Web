# E-Commerce Web Application

A full-stack e-commerce application with React frontend, FastAPI backend, MongoDB database, and C++ discount engine.

## Features

- **User Authentication**: Sign up and login with JWT tokens
- **Product Management**: Browse products, add to cart, and place orders
- **Admin Dashboard**: Add new products (admin only)
- **Order Tracking**: Track your orders with status and location
- **Discount System**: C++-powered discount calculation engine
- **Responsive UI**: Modern, clean interface

## Tech Stack

### Frontend
- React 19
- React Router DOM
- Axios
- Modern CSS styling

### Backend
- FastAPI
- MongoDB (Motor async driver)
- JWT authentication
- CORS enabled

### C++ Engine
- Discount calculation engine compiled as shared library

## Setup Instructions

### Prerequisites
- Node.js and npm
- Python 3.8+
- MongoDB (running on localhost:27017)
- g++ compiler (for C++ engine)

### Backend Setup

1. Navigate to the backend directory:
```bash
cd backend
```

2. Install Python dependencies:
```bash
pip install -r requirements.txt
```

3. Make sure MongoDB is running on `localhost:27017`

4. Start the FastAPI server:
```bash
uvicorn main:app --reload
```

The backend will run on `http://127.0.0.1:8000`

### C++ Engine Setup

#### Windows:
```bash
cd cpp-engine
build.bat
```

#### Linux/Mac:
```bash
cd cpp-engine
chmod +x build.sh
./build.sh
```

This will create `discount.dll` (Windows) or `discount.so` (Linux/Mac) in the `cpp-engine` directory.

**Note**: If the C++ engine fails to compile, the backend will automatically use a Python fallback implementation.

### Frontend Setup

1. Navigate to the frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm start
```

The frontend will run on `http://localhost:3000`

## Usage

1. **Sign Up**: Create a new account at `/signup`
2. **Login**: Login with your credentials at `/`
3. **Browse Products**: View available products at `/products`
4. **Add to Cart**: Click "Add to Cart" on any product
5. **Place Order**: Go to `/cart`, optionally enter a coupon code (0-70%), and place your order
6. **Track Orders**: View your order history at `/track`
7. **Admin**: Login with an admin account to access `/admin` and add new products

## Admin Access

To create an admin user, you can manually insert one into MongoDB:

```javascript
db.users.insertOne({
  email: "admin@example.com",
  password: "<hashed_password>",
  role: "admin"
})
```

Or sign up normally and update the role in MongoDB.

## API Endpoints

- `POST /signup` - Create new user account
- `POST /login` - Login and get JWT token
- `GET /products` - Get all products (requires auth)
- `POST /products` - Add new product (admin only)
- `POST /order?coupon=<percent>` - Place order with optional discount
- `GET /track/{email}` - Get orders for a user

## Project Structure

```
E com Web/
├── backend/
│   ├── main.py          # FastAPI application
│   ├── database.py      # MongoDB connection
│   ├── schemas.py       # Pydantic models
│   ├── auth.py          # Authentication utilities
│   └── requirements.txt # Python dependencies
├── frontend/
│   ├── src/
│   │   ├── App.jsx      # Main app component with routing
│   │   ├── api.js       # Axios API client
│   │   └── components/  # Reusable components
│   ├── pages/           # Page components
│   └── package.json     # Node dependencies
├── cpp-engine/
│   ├── discount.cpp     # C++ discount calculation
│   ├── engine.h         # Header file
│   └── build scripts    # Compilation scripts
└── README.md
```

## Notes

- The C++ discount engine supports discounts from 0-70%
- All routes except `/signup` and `/login` require authentication
- Admin routes require admin role
- Users can only track their own orders (unless admin)
- Cart is stored in localStorage
- JWT tokens expire after 2 hours

## Troubleshooting

- **C++ engine not loading**: The backend will automatically use a Python fallback
- **CORS errors**: Make sure the backend is running and CORS is configured
- **MongoDB connection errors**: Ensure MongoDB is running on `localhost:27017`
- **401 errors**: Make sure you're logged in and the token hasn't expired

