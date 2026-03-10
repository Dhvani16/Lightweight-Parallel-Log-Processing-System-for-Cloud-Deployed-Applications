import { useEffect, useState } from "react";
import api from "../api/client";

export default function PerformanceStats() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    const fetchStats = async () => {
      const res = await api.get("/stats/");
      setStats(res.data);
    };

    fetchStats();
    const interval = setInterval(fetchStats, 3000);
    return () => clearInterval(interval);
  }, []);

  if (!stats) return null;

  return (
    <div style={{ marginTop: 40 }}>
      <h2>Performance Comparison</h2>

      <div>
        <strong>Avg Sequential:</strong>{" "}
        {stats.sequential_avg_ms
          ? stats.sequential_avg_ms.toFixed(2)
          : "N/A"}{" "}
        ms
      </div>

      <div>
        <strong>Avg Parallel:</strong>{" "}
        {stats.parallel_avg_ms
          ? stats.parallel_avg_ms.toFixed(2)
          : "N/A"}{" "}
        ms
      </div>

      <div>
        <strong>Speedup:</strong>{" "}
        {stats.speedup
          ? stats.speedup.toFixed(2) + "x"
          : "Not enough data"}
      </div>
    </div>
  );
}