import { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import api from "../src/api";

export default function Cart() {
  const [cart, setCart] = useState([]);
  const [coupon, setCoupon] = useState("");
  const [userEmail, setUserEmail] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  useEffect(() => {
    loadCart();
    loadUserEmail();
  }, []);

  const loadCart = () => {
    const savedCart = JSON.parse(localStorage.getItem("cart") || "[]");
    setCart(savedCart);
  };

  const loadUserEmail = () => {
    try {
      const token = localStorage.getItem("token");
      if (token) {
        const payload = JSON.parse(atob(token.split('.')[1]));
        setUserEmail(payload.email || "");
      }
    } catch (err) {
      console.error("Failed to load user email", err);
    }
  };

  const removeFromCart = (index) => {
    const newCart = cart.filter((_, i) => i !== index);
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
  };

  const placeOrder = async () => {
    if (cart.length === 0) {
      alert("Cart is empty");
      return;
    }

    if (!userEmail) {
      alert("User email not found. Please login again.");
      return;
    }

    setLoading(true);
    try {
      const total = cart.reduce((s, p) => s + p.price, 0);
      const couponPercent = coupon ? parseInt(coupon) : 0;

      const response = await api.post("/order", {
        user_email: userEmail,
        products: cart.map((p) => p.name),
        total,
      }, {
        params: { coupon: couponPercent }
      });

      alert("Order placed successfully!");
      localStorage.removeItem("cart");
      navigate("/track");
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to place order");
    } finally {
      setLoading(false);
    }
  };

  const total = cart.reduce((s, p) => s + p.price, 0);

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Shopping Cart</h2>

      {cart.length === 0 ? (
        <div style={styles.empty}>
          <p>Your cart is empty</p>
          <button style={styles.button} onClick={() => navigate("/products")}>
            Continue Shopping
          </button>
        </div>
      ) : (
        <>
          <div style={styles.cartItems}>
            {cart.map((item, index) => (
              <div key={index} style={styles.cartItem}>
                <div style={styles.itemInfo}>
                  <h3 style={styles.itemName}>{item.name}</h3>
                  <p style={styles.itemCategory}>{item.category}</p>
                  <p style={styles.itemPrice}>₹{item.price.toFixed(2)}</p>
                </div>
                <button
                  style={styles.removeButton}
                  onClick={() => removeFromCart(index)}
                >
                  Remove
                </button>
              </div>
            ))}
          </div>

          <div style={styles.summary}>
            <div style={styles.couponSection}>
              <input
                style={styles.couponInput}
                placeholder="Coupon code (0-70)"
                type="number"
                min="0"
                max="70"
                value={coupon}
                onChange={(e) => setCoupon(e.target.value)}
              />
            </div>
            <div style={styles.totalSection}>
              <p style={styles.totalLabel}>Total: ₹{total.toFixed(2)}</p>
              {coupon && !isNaN(coupon) && (
                <p style={styles.discount}>
                  Discount ({coupon}%): ₹
                  {(total - total * (parseInt(coupon) / 100)).toFixed(2)}
                </p>
              )}
            </div>
            <button
              style={styles.orderButton}
              onClick={placeOrder}
              disabled={loading}
            >
              {loading ? "Placing Order..." : "Place Order"}
            </button>
          </div>
        </>
      )}
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "800px",
    margin: "0 auto",
    padding: "2rem",
  },
  title: {
    color: "#2c3e50",
    marginBottom: "2rem",
  },
  empty: {
    textAlign: "center",
    padding: "3rem",
  },
  cartItems: {
    marginBottom: "2rem",
  },
  cartItem: {
    backgroundColor: "white",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "1.5rem",
    marginBottom: "1rem",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  itemInfo: {
    flex: 1,
  },
  itemName: {
    margin: "0 0 0.5rem 0",
    color: "#2c3e50",
  },
  itemCategory: {
    color: "#7f8c8d",
    fontSize: "0.9rem",
    margin: "0 0 0.5rem 0",
  },
  itemPrice: {
    fontSize: "1.2rem",
    fontWeight: "bold",
    color: "#27ae60",
    margin: 0,
  },
  removeButton: {
    backgroundColor: "#e74c3c",
    color: "white",
    border: "none",
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    cursor: "pointer",
  },
  summary: {
    backgroundColor: "white",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "1.5rem",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  couponSection: {
    marginBottom: "1rem",
  },
  couponInput: {
    width: "100%",
    padding: "0.75rem",
    border: "1px solid #ddd",
    borderRadius: "4px",
    fontSize: "1rem",
    boxSizing: "border-box",
  },
  totalSection: {
    marginBottom: "1rem",
    paddingTop: "1rem",
    borderTop: "1px solid #e0e0e0",
  },
  totalLabel: {
    fontSize: "1.5rem",
    fontWeight: "bold",
    color: "#2c3e50",
    margin: "0 0 0.5rem 0",
  },
  discount: {
    color: "#27ae60",
    fontSize: "1.1rem",
    margin: 0,
  },
  orderButton: {
    width: "100%",
    padding: "1rem",
    backgroundColor: "#27ae60",
    color: "white",
    border: "none",
    borderRadius: "4px",
    fontSize: "1.1rem",
    cursor: "pointer",
    fontWeight: "bold",
  },
  button: {
    padding: "0.75rem 1.5rem",
    backgroundColor: "#3498db",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
  },
};
