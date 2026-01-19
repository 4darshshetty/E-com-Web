import { useEffect, useState } from "react";
import api from "../src/api";

export default function Admin() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [showForm, setShowForm] = useState(false);
  const [formData, setFormData] = useState({
    name: "",
    price: "",
    category: "",
    stock: "",
  });

  useEffect(() => {
    loadProducts();
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

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      await api.post("/products", {
        name: formData.name,
        price: parseFloat(formData.price),
        category: formData.category,
        stock: parseInt(formData.stock),
      });
      alert("Product added successfully!");
      setFormData({ name: "", price: "", category: "", stock: "" });
      setShowForm(false);
      loadProducts();
    } catch (err) {
      alert(err.response?.data?.detail || "Failed to add product");
    }
  };

  if (loading) {
    return <div style={styles.loading}>Loading...</div>;
  }

  return (
    <div style={styles.container}>
      <div style={styles.header}>
        <h2 style={styles.title}>Admin Dashboard</h2>
        <button
          style={styles.addButton}
          onClick={() => setShowForm(!showForm)}
        >
          {showForm ? "Cancel" : "Add Product"}
        </button>
      </div>

      {showForm && (
        <form style={styles.form} onSubmit={handleSubmit}>
          <h3 style={styles.formTitle}>Add New Product</h3>
          <input
            style={styles.input}
            placeholder="Product Name"
            value={formData.name}
            onChange={(e) =>
              setFormData({ ...formData, name: e.target.value })
            }
            required
          />
          <input
            style={styles.input}
            placeholder="Price"
            type="number"
            step="0.01"
            min="0"
            value={formData.price}
            onChange={(e) =>
              setFormData({ ...formData, price: e.target.value })
            }
            required
          />
          <input
            style={styles.input}
            placeholder="Category"
            value={formData.category}
            onChange={(e) =>
              setFormData({ ...formData, category: e.target.value })
            }
            required
          />
          <input
            style={styles.input}
            placeholder="Stock"
            type="number"
            min="0"
            value={formData.stock}
            onChange={(e) =>
              setFormData({ ...formData, stock: e.target.value })
            }
            required
          />
          <button type="submit" style={styles.submitButton}>
            Add Product
          </button>
        </form>
      )}

      <div style={styles.productsGrid}>
        {products.length === 0 ? (
          <p style={styles.empty}>No products</p>
        ) : (
          products.map((p) => (
            <div key={p._id} style={styles.productCard}>
              <h3 style={styles.productName}>{p.name}</h3>
              <p style={styles.category}>{p.category}</p>
              <p style={styles.price}>₹{p.price.toFixed(2)}</p>
              <p style={styles.stock}>Stock: {p.stock}</p>
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
  addButton: {
    backgroundColor: "#27ae60",
    color: "white",
    border: "none",
    padding: "0.75rem 1.5rem",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
  },
  form: {
    backgroundColor: "white",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "2rem",
    marginBottom: "2rem",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  formTitle: {
    marginTop: 0,
    marginBottom: "1.5rem",
    color: "#2c3e50",
  },
  input: {
    width: "100%",
    padding: "0.75rem",
    marginBottom: "1rem",
    border: "1px solid #ddd",
    borderRadius: "4px",
    fontSize: "1rem",
    boxSizing: "border-box",
  },
  submitButton: {
    width: "100%",
    padding: "0.75rem",
    backgroundColor: "#3498db",
    color: "white",
    border: "none",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "1rem",
  },
  productsGrid: {
    display: "grid",
    gridTemplateColumns: "repeat(auto-fill, minmax(250px, 1fr))",
    gap: "1.5rem",
  },
  productCard: {
    backgroundColor: "white",
    border: "1px solid #e0e0e0",
    borderRadius: "8px",
    padding: "1.5rem",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  productName: {
    margin: "0 0 0.5rem 0",
    color: "#2c3e50",
  },
  category: {
    color: "#7f8c8d",
    fontSize: "0.9rem",
    margin: "0 0 0.5rem 0",
  },
  price: {
    fontSize: "1.2rem",
    fontWeight: "bold",
    color: "#27ae60",
    margin: "0.5rem 0",
  },
  stock: {
    fontSize: "0.9rem",
    color: "#7f8c8d",
    margin: 0,
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
