import { useEffect, useState } from "react";
import api from "../api";

export default function Admin() {
  const [products, setProducts] = useState([]);

  useEffect(() => {
    api.get("/products").then(res => setProducts(res.data));
  }, []);

  return (
    <div>
      <h2>Admin Dashboard</h2>
      {products.map(p => (
        <p key={p._id}>{p.name} - ₹{p.price}</p>
      ))}
    </div>
  );
}
