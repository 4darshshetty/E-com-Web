import { useEffect, useState } from "react";
import api from "../src/api";

export default function Track() {
  const [orders, setOrders] = useState([]);
  const [loading, setLoading] = useState(true);
  const [userEmail, setUserEmail] = useState("");

  useEffect(() => {
    loadUserEmail();
  }, []);

  useEffect(() => {
    if (userEmail) {
      loadOrders();
    }
  }, [userEmail]);

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

  const loadOrders = async () => {
    try {
      const res = await api.get(`/track/${userEmail}`);
      setOrders(res.data);
    } catch (err) {
      console.error("Failed to load orders", err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading orders...</div>;
  }

  return (
    <div style={styles.container}>
      <h2 style={styles.title}>Order Tracking</h2>

      {orders.length === 0 ? (
        <div style={styles.empty}>
          <p>No orders found</p>
        </div>
      ) : (
        <div style={styles.ordersList}>
          {orders.map((order) => (
            <div key={order._id} style={styles.orderCard}>
              <div style={styles.orderHeader}>
                <h3 style={styles.orderId}>Order #{order._id.slice(-8)}</h3>
                <span
                  style={{
                    ...styles.status,
                    ...styles[`status${order.status}`],
                  }}
                >
                  {order.status}
                </span>
              </div>
              <div style={styles.orderDetails}>
                <p style={styles.products}>
                  <strong>Products:</strong> {order.products.join(", ")}
                </p>
                <p style={styles.total}>
                  <strong>Total:</strong> ₹{order.total.toFixed(2)}
                </p>
                <p style={styles.location}>
                  <strong>Location:</strong>{" "}
                  {order.location || "Not updated"}
                </p>
              </div>
            </div>
          ))}
        </div>
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
  loading: {
    textAlign: "center",
    padding: "2rem",
    fontSize: "1.2rem",
    color: "#7f8c8d",
  },
  empty: {
    textAlign: "center",
    padding: "3rem",
    color: "#7f8c8d",
  },
  ordersList: {
    display: "flex",
    flexDirection: "column",
    gap: "1rem",
  },
  orderCard: {
    backgroundColor: "white",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "1.5rem",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  orderHeader: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "1rem",
    paddingBottom: "1rem",
    borderBottom: "1px solid #e0e0e0",
  },
  orderId: {
    margin: 0,
    color: "#2c3e50",
  },
  status: {
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    fontSize: "0.9rem",
    fontWeight: "bold",
  },
  statusProcessing: {
    backgroundColor: "#f39c12",
    color: "white",
  },
  statusShipped: {
    backgroundColor: "#3498db",
    color: "white",
  },
  statusDelivered: {
    backgroundColor: "#27ae60",
    color: "white",
  },
  statusCancelled: {
    backgroundColor: "#e74c3c",
    color: "white",
  },
  orderDetails: {
    display: "flex",
    flexDirection: "column",
    gap: "0.5rem",
  },
  products: {
    margin: 0,
    color: "#2c3e50",
  },
  total: {
    margin: 0,
    color: "#27ae60",
    fontSize: "1.1rem",
    fontWeight: "bold",
  },
  location: {
    margin: 0,
    color: "#7f8c8d",
  },
};
