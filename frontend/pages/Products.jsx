import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import api from "../src/api";

export default function Products() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    loadProducts();
    loadCart();
  }, []);

  const loadProducts = async () => {
    try {
      const res = await api.get("/products");
      setProducts(res.data);
    } catch (err) {
      console.error("Failed to load products", err);
    } finally {
      setLoading(false);
    }
  };

  const loadCart = () => {
    const savedCart = JSON.parse(localStorage.getItem("cart") || "[]");
    setCart(savedCart);
  };

  const addToCart = (p) => {
    if (p.stock <= 0) {
      alert("Product out of stock");
      return;
    }
    const newCart = [...cart, p];
    setCart(newCart);
    localStorage.setItem("cart", JSON.stringify(newCart));
    alert(`${p.name} added to cart!`);
  };

  const getCartCount = () => cart.length;

  if (loading) {
    return <div style={styles.loading}>Loading products...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Products</h2>
        <button style={styles.cartButton} onClick={() => navigate("/cart")}>
          Cart ({getCartCount()})
        </button>
      </div>

      <div style={styles.grid}>
        {products.length === 0 ? (
          <p style={styles.empty}>No products available</p>
        ) : (
          products.map((p) => (
            <div key={p._id} style={styles.card}>
              <h3 style={styles.productName}>{p.name}</h3>
              <p style={styles.category}>{p.category}</p>
              <p style={styles.price}>₹{p.price.toFixed(2)}</p>
              <p style={styles.stock}>
                {p.stock > 0 ? `In Stock: ${p.stock}` : "Out of Stock"}
              </p>
              <button
                style={{
                  ...styles.addButton,
                  ...(p.stock <= 0 ? styles.disabledButton : {}),
                }}
                onClick={() => addToCart(p)}
                disabled={p.stock <= 0}
              >
                {p.stock > 0 ? "Add to Cart" : "Out of Stock"}
              </button>
            </div>
          ))
        )}
      </div>
    </div>
  );
}

const styles = {
  container: {
    maxWidth: "1200px",
    margin: "0 auto",
    padding: "2rem",
  },
  header: {
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    marginBottom: "2rem",
  },
  title: {
    color: "#2c3e50",
    margin: 0,
  },
  cartButton: {
    backgroundColor: "#3498db",
    color: "white",
    border: "none",
    padding: "0.75rem 1.5rem",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
  },
  grid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
    gap: "1.5rem",
  },
  card: {
    backgroundColor: "white",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "1.5rem",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
    transition: "transform 0.2s",
  },
  productName: {
    margin: "0 0 0.5rem 0",
    color: "#2c3e50",
    fontSize: "1.25rem",
  },
  category: {
    color: "#7f8c8d",
    fontSize: "0.9rem",
    margin: "0 0 0.5rem 0",
  },
  price: {
    fontSize: "1.5rem",
    fontWeight: "bold",
    color: "#27ae60",
    margin: "0.5rem 0",
  },
  stock: {
    fontSize: "0.9rem",
    color: "#7f8c8d",
    margin: "0.5rem 0",
  },
  addButton: {
    width: "100%",
    padding: "0.75rem",
    backgroundColor: "#3498db",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
    marginTop: "1rem",
  },
  disabledButton: {
    backgroundColor: "#bdc3c7",
    cursor: "not-allowed",
  },
  empty: {
    textAlign: "center",
    color: "#7f8c8d",
    fontSize: "1.2rem",
    gridColumn: "1 / -1",
  },
  loading: {
    textAlign: "center",
    padding: "2rem",
    fontSize: "1.2rem",
    color: "#7f8c8d",
  },
};
