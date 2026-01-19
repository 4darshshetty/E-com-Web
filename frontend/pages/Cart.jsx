import api from "../api";

export default function Cart() {
  const cart = JSON.parse(localStorage.getItem("cart") || "[]");

  const placeOrder = async () => {
    const total = cart.reduce((s, p) => s + p.price, 0);

    await api.post("/order", {
      user_email: "user@gmail.com",
      products: cart.map(p => p.name),
      total
    });

    alert("Order placed");
    localStorage.removeItem("cart");
    window.location = "/track";
  };

  return (
    <div>
      <h2>Cart</h2>
      {cart.map((p, i) => (
        <p key={i}>{p.name} - ₹{p.price}</p>
      ))}
      <button onClick={placeOrder}>Place Order</button>
    </div>
  );
}
