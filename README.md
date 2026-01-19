# 🛍️ Advanced E-Commerce Web Application

A **professional, full-featured e-commerce platform** built with **React**, **Python (FastAPI)**, **MongoDB**, and **C++** for high performance. This is a production-ready application with advanced features including payment processing, real-time shipping tracking, map integration, admin analytics, and 3D graphics.

## ✨ Key Features

### 🔐 Authentication & User Management
- User registration and login
- JWT token-based authentication
- Role-based access control (User/Admin)
- User profile management
- Secure password hashing

### 📦 Product Management
- Complete CRUD operations
- Category-based organization
- Advanced search and filtering
- Product images and specifications
- Stock management
- Featured products
- Ratings and reviews

### 🛒 Shopping Experience
- Advanced shopping cart
- Real-time cart updates
- Persistent cart storage
- Quantity management
- Cart total calculation

### 💳 Payment Processing
- **Stripe integration** (production-ready)
- Multiple payment methods
- Payment intent creation
- Payment confirmation
- Payment status tracking
- Mock payment for development

### 📍 Shipping & Tracking
- Real-time order tracking
- **Map integration** (Leaflet)
- GPS location tracking
- Shipping cost calculation
- Delivery estimation
- Tracking number generation
- Shipping history

### 🏠 Address Management
- Add/edit/delete addresses
- **Map picker** for location selection
- GPS coordinates
- Default address selection
- Address validation

### 🎫 Coupon System
- Coupon code creation (admin)
- Percentage and fixed discounts
- Usage limits
- Expiry dates
- Minimum purchase requirements
- Bank discount integration

### 📊 Admin Dashboard
- **Sales analytics** with charts
- Revenue statistics
- Payment statistics
- Order tracking
- Product management
- User management
- Revenue by category
- Top products analysis
- Recent orders

### 🎨 Advanced UI/UX
- Modern, responsive design
- Smooth animations (Framer Motion)
- Loading states
- Error handling
- Toast notifications
- Premium styling
- **3D product visualization** (Three.js)

### ⚡ Performance
- **C++ discount engine** for fast calculations
- **C++ 3D graphics engine** for product rendering
- MongoDB indexes for optimization
- Async operations
- Code splitting

## 🏗️ Technology Stack

### Backend
- **Python 3.8+** - Programming language
- **FastAPI** - Modern, fast web framework
- **MongoDB** - NoSQL database
- **Motor** - Async MongoDB driver
- **JWT** - Authentication tokens
- **Stripe** - Payment processing
- **Geopy** - Location services

### Frontend
- **React 19** - UI framework
- **React Router** - Client-side routing
- **Axios** - HTTP client
- **Leaflet** - Map integration
- **Stripe.js** - Payment UI
- **Recharts** - Analytics charts
- **Framer Motion** - Animations
- **Three.js** - 3D graphics
- **React Icons** - Icon library

### Performance Engines
- **C++** - Discount calculation engine
- **C++** - 3D graphics rendering engine

## 📁 Project Structure

```
E com Web/
├── backend/                 # Python FastAPI backend
│   ├── main.py             # Main API endpoints
│   ├── database.py         # MongoDB connection
│   ├── schemas.py          # Pydantic models
│   ├── auth.py             # Authentication
│   ├── payment.py          # Payment integration
│   ├── shipping.py         # Shipping logic
│   ├── coupon_service.py   # Coupon system
│   └── requirements.txt    # Dependencies
│
├── frontend/                # React frontend
│   ├── src/
│   │   ├── App.jsx         # Main app component
│   │   ├── api.js          # API client
│   │   ├── components/     # Reusable components
│   │   └── pages/          # Page components
│   └── package.json        # Dependencies
│
├── cpp-engine/              # C++ performance engines
│   ├── discount.cpp        # Discount engine
│   ├── graphics_engine.cpp # 3D graphics
│   └── build_advanced.bat  # Build script
│
├── README.md                # This file
├── DEPLOYMENT.md           # Deployment guide
└── PROJECT_STRUCTURE.md    # Detailed structure
```

## 🚀 Quick Start

### Prerequisites
- **Node.js** 16+ and npm
- **Python** 3.8+
- **MongoDB** (local or Atlas)
- **g++ compiler** (for C++ engines)

### Step 1: Clone Repository
```bash
git clone <your-repo-url>
cd "E com Web"
```

### Step 2: Backend Setup
```bash
cd backend
pip install -r requirements.txt
```

### Step 3: Frontend Setup
```bash
cd frontend
npm install
```

### Step 4: Build C++ Engines (Optional)
```bash
cd cpp-engine
build_advanced.bat  # Windows
# or
./build_advanced.sh  # Linux/Mac
```

### Step 5: Start MongoDB
Make sure MongoDB is running on `localhost:27017`

### Step 6: Start Backend
```bash
cd backend
uvicorn main:app --reload
```
Backend runs on: **http://127.0.0.1:8000**

### Step 7: Start Frontend
```bash
cd frontend
npm start
```
Frontend runs on: **http://localhost:3000**

## 🔧 Configuration

### Backend Environment Variables
Create `backend/.env`:
```env
MONGO_URL=mongodb://localhost:27017
STRIPE_SECRET_KEY=sk_test_your_key
SECRET_KEY=your_secret_key_here
```

### Frontend Environment Variables
Create `frontend/.env`:
```env
REACT_APP_API_URL=http://127.0.0.1:8000
REACT_APP_STRIPE_KEY=pk_test_your_key
```

## 📚 API Documentation

When the backend is running, visit:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

## 🎯 Usage Guide

### For Users
1. **Sign Up**: Create a new account
2. **Login**: Authenticate with credentials
3. **Browse Products**: View products by category
4. **Add to Cart**: Add products to shopping cart
5. **Checkout**: Enter address and payment details
6. **Track Order**: Monitor order status with map
7. **View History**: Check order history

### For Admins
1. **Admin Login**: Login with admin credentials
2. **Dashboard**: View sales and payment analytics
3. **Add Products**: Create new products
4. **Manage Orders**: Update order status
5. **Track Shipments**: Update shipping locations
6. **Create Coupons**: Generate discount codes
7. **View Statistics**: Analyze sales data

## 🔐 Admin Setup

To create an admin user:
1. Sign up normally
2. Update MongoDB:
```javascript
use ecommerce_db
db.users.updateOne(
  { email: "admin@example.com" },
  { $set: { role: "admin" } }
)
```

## 📊 Features Breakdown

### Payment System
- Stripe integration for secure payments
- Support for credit/debit cards, PayPal, UPI
- Payment intent creation
- Payment confirmation
- Transaction tracking
- Refund support

### Shipping Tracker
- Real-time GPS tracking
- Map visualization
- Location history
- Delivery estimation
- Status updates
- Tracking numbers

### Address Management
- Multiple addresses per user
- Map-based address picker
- GPS coordinates
- Default address
- Address validation

### Coupon System
- Percentage discounts
- Fixed amount discounts
- Usage limits
- Expiry dates
- Minimum purchase
- Bank discounts

### Admin Analytics
- Total revenue
- Sales by category
- Payment statistics
- Top products
- Recent orders
- Monthly trends

## 🎨 UI Components

- **Navbar**: Navigation with user menu
- **ProductCard**: Product display with images
- **Cart**: Shopping cart with totals
- **Checkout**: Payment and address form
- **MapView**: Interactive map component
- **TrackingMap**: Order tracking visualization
- **AdminDashboard**: Analytics and management
- **PaymentForm**: Stripe payment integration

## 🚀 Deployment

See `DEPLOYMENT.md` for detailed deployment instructions to:
- **Vercel/Netlify** (Frontend)
- **Railway/Heroku** (Backend)
- **MongoDB Atlas** (Database)
- **GitHub Pages** (Alternative)

## 🛠️ Development

### Backend Development
```bash
cd backend
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

### Frontend Development
```bash
cd frontend
npm start
```

### C++ Engine Development
```bash
cd cpp-engine
g++ -shared -o discount.dll discount.cpp -fPIC -O3
g++ -shared -o graphics_engine.dll graphics_engine.cpp -fPIC -O3
```

## 📝 API Endpoints

### Authentication
- `POST /signup` - Register new user
- `POST /login` - User login
- `POST /logout` - User logout

### Products
- `GET /products` - List products
- `GET /products/{id}` - Get product details
- `POST /products` - Create product (admin)
- `PUT /products/{id}` - Update product (admin)

### Cart
- `POST /cart/add` - Add to cart
- `GET /cart` - Get cart
- `DELETE /cart/{id}` - Remove item

### Orders
- `POST /orders` - Create order
- `GET /orders` - List orders
- `GET /orders/{id}` - Get order details

### Tracking
- `GET /track/{tracking_number}` - Track order

### Payments
- `POST /payments/intent` - Create payment intent
- `POST /payments/confirm` - Confirm payment

### Admin
- `GET /admin/analytics/sales` - Sales statistics
- `GET /admin/analytics/payments` - Payment statistics

See API docs at `/docs` for complete list.

## 🔒 Security

- JWT authentication
- Password hashing (bcrypt)
- CORS configuration
- Input validation
- Role-based access control
- Secure payment processing

## 📈 Performance

- C++ engines for fast calculations
- MongoDB indexes
- Async operations
- Code splitting
- Lazy loading
- Image optimization

## 🐛 Troubleshooting

### Backend Issues
- Check MongoDB connection
- Verify environment variables
- Check CORS settings
- Review logs: `uvicorn main:app --reload`

### Frontend Issues
- Check API URL in `.env`
- Verify backend is running
- Check browser console
- Clear cache and rebuild

### C++ Engine Issues
- Ensure g++ is installed
- Check build script permissions
- Verify DLL/SO files exist

## 📄 License

This project is open source and available for educational purposes.

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📞 Support

For issues and questions:
1. Check the documentation
2. Review API docs at `/docs`
3. Check GitHub issues
4. Create a new issue

## 🎉 Acknowledgments

- FastAPI for the excellent framework
- React team for the amazing library
- MongoDB for the database
- Stripe for payment processing
- All open-source contributors

---

**Built with ❤️ using React, Python, MongoDB, and C++**
