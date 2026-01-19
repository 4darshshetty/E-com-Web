import api from "../api";
import { useEffect, useState } from "react";

export default function Products() {
  const [items, setItems] = useState([]);

  useEffect(() => {
    api.get("/products").then(res => setItems(res.data));
  }, []);

  return (
    <div>
      {items.map(p => (
        <div key={p._id}>
          {p.name} - ₹{p.price}
        </div>
      ))}
    </div>
  );
}
