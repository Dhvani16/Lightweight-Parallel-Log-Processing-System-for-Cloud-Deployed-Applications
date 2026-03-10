import { useEffect, useState } from "react";
import api from "../api/client";

export default function StatsPage() {
  const [stats, setStats] = useState(null);

  useEffect(() => {
    api.get("/stats/").then((res) => setStats(res.data));
  }, []);

  if (!stats) return <div>Loading stats...</div>;

  return (
    <div>
      <h2>System Stats</h2>
      <pre>{JSON.stringify(stats, null, 2)}</pre>
    </div>
  );
}