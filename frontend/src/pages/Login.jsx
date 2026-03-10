import { useState } from "react";
import api from "../api/client";

export default function Login({ onLogin }) {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");

  const inputStyle = {
    padding: 10,
    borderRadius: 4,
    border: "none",
  };

  const buttonStyle = {
    padding: 10,
    background: "#3b82f6",
    color: "white",
    border: "none",
    cursor: "pointer",
  };

  const submit = async (e) => {
    e.preventDefault();

    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const res = await api.post("/auth/login", formData, {
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
    });

    localStorage.setItem("token", res.data.access_token);
    onLogin();
  };

  return (
    <div style={{
      display: "flex",
      justifyContent: "center",
      alignItems: "center",
      height: "100vh",
      background: "#0f172a",
      color: "white"
    }}>
      <form
        onSubmit={submit}
        style={{
          background: "#1e293b",
          padding: 40,
          borderRadius: 8,
          display: "flex",
          flexDirection: "column",
          gap: 15,
          width: 300,
        }}
      >
        <h2 style={{ textAlign: "center" }}>Login</h2>

        <input
          placeholder="Username"
          onChange={(e) => setUsername(e.target.value)}
          style={inputStyle}
        />

        <input
          type="password"
          placeholder="Password"
          onChange={(e) => setPassword(e.target.value)}
          style={inputStyle}
        />

        <button type="submit" style={buttonStyle}>Login</button>
      </form>
    </div>
  );
}