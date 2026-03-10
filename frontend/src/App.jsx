import { BrowserRouter, Routes, Route, Navigate } from "react-router-dom";
import Login from "./pages/Login";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";
import StatsPage from "./pages/StatsPage";
import HealthPage from "./pages/HealthPage";
import Layout from "./components/Layout";

function App() {
  const token = localStorage.getItem("token");

  return (
    <BrowserRouter>
      {!token ? (
        <Login onLogin={() => window.location.reload()} />
      ) : (
        <Layout>
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/upload" element={<Upload />} />
            <Route path="/stats" element={<StatsPage />} />
            <Route path="/health" element={<HealthPage />} />
            <Route path="*" element={<Navigate to="/" />} />
          </Routes>
        </Layout>
      )}
    </BrowserRouter>
  );
}

export default App;