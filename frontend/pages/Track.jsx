import { useEffect, useState } from "react";
import api from "../api";

export default function Track() {
  const [orders, setOrders] = useState([]);

  useEffect(() => {
    api.get("/orders/user@gmail.com").then(res => setOrders(res.data));
  }, []);

  return (
    <div>
      <h2>Order Tracking</h2>
      {orders.map(o => (
        <div key={o._id}>
          <p>Status: {o.status}</p>
          <p>Location: {o.location || "Not updated"}</p>
        </div>
      ))}
    </div>
  );
}
