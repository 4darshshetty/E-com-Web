import api from "../api";

export default function Login() {
  const login = async () => {
    const res = await api.post("/login", {
      email: "user@gmail.com",
      password: "1234"
    });
    localStorage.setItem("token", res.data.token);
    window.location = "/products";
  };

  return <button onClick={login}>Login</button>;
}
