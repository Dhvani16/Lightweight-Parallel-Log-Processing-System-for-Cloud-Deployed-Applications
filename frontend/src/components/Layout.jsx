import { Link, useNavigate } from "react-router-dom";

export default function Layout({ children }) {
  const navigate = useNavigate();

  const logout = () => {
    localStorage.removeItem("token");
    navigate("/");
    window.location.reload();
  };

  return (
    <div style={{ display: "flex", minHeight: "100vh", fontFamily: "sans-serif" }}>
      <aside
        style={{
          width: 220,
          background: "#1e293b",
          color: "white",
          padding: 20,
        }}
      >
        <h2>Log Analyzer</h2>
        <nav style={{ display: "flex", flexDirection: "column", gap: 10 }}>
          <Link to="/" style={linkStyle}>Dashboard</Link>
          <Link to="/upload" style={linkStyle}>Upload Job</Link>
          <Link to="/stats" style={linkStyle}>Stats</Link>
          <Link to="/health" style={linkStyle}>Health</Link>
          <button onClick={logout} style={logoutStyle}>Logout</button>
        </nav>
      </aside>

      <main style={{ flex: 1, padding: 30, background: "#f1f5f9" }}>
        {children}
      </main>
    </div>
  );
}

const linkStyle = {
  color: "white",
  textDecoration: "none",
  padding: "8px 0",
};

const logoutStyle = {
  marginTop: 20,
  padding: 8,
  background: "#ef4444",
  border: "none",
  color: "white",
  cursor: "pointer",
};