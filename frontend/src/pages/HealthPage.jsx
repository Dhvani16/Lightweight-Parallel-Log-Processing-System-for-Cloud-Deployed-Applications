import { useEffect, useState } from "react";
import api from "../api/client";

export default function HealthPage() {
  const [health, setHealth] = useState(null);

  useEffect(() => {
    api.get("/health").then((res) => setHealth(res.data));
  }, []);

  return (
    <div>
      <h2>Backend Health</h2>
      {health ? <pre>{JSON.stringify(health, null, 2)}</pre> : "Checking..."}
    </div>
  );
}