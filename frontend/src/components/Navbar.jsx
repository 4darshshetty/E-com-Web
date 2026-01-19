import { useNavigate } from "react-router-dom";

export default function Navbar() {
  const navigate = useNavigate();
  const token = localStorage.getItem("token");
  
  let userRole = "user";
  try {
    if (token) {
      const payload = JSON.parse(atob(token.split('.')[1]));
      userRole = payload.role || "user";
    }
  } catch {}

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
  };

  if (!token) return null;

  return (
    <nav style={styles.navbar}>
      <div style={styles.container}>
        <h2 style={styles.logo} onClick={() => navigate("/products")}>E-Commerce</h2>
        <div style={styles.links}>
          <button style={styles.link} onClick={() => navigate("/products")}>Products</button>
          <button style={styles.link} onClick={() => navigate("/cart")}>Cart</button>
          <button style={styles.link} onClick={() => navigate("/track")}>Track Orders</button>
          {userRole === "admin" && (
            <button style={styles.link} onClick={() => navigate("/admin")}>Admin</button>
          )}
          <button style={styles.link} onClick={logout}>Logout</button>
        </div>
      </div>
    </nav>
  );
}

const styles = {
  navbar: {
    backgroundColor: "#2c3e50",
    color: "white",
    padding: "1rem 0",
    boxShadow: "0 2px 4px rgba(0,0,0,0.1)",
  },
  container: {
    maxWidth: "1200px",
    margin: "0 auto",
    display: "flex",
    justifyContent: "space-between",
    alignItems: "center",
    padding: "0 2rem",
  },
  logo: {
    margin: 0,
    cursor: "pointer",
    fontSize: "1.5rem",
  },
  links: {
    display: "flex",
    gap: "1rem",
  },
  link: {
    backgroundColor: "transparent",
    border: "1px solid white",
    color: "white",
    padding: "0.5rem 1rem",
    borderRadius: "4px",
    cursor: "pointer",
    fontSize: "0.9rem",
  },
};

