import { useEffect, useState } from "react";
import api from "../api/client";

export default function Dashboard({ jobId }) {
  const [job, setJob] = useState(null);

  useEffect(() => {
    const interval = setInterval(async () => {
      const res = await api.get(`/jobs/${jobId}`);
      setJob(res.data);

      if (res.data.status === "completed") {
        clearInterval(interval);
      }
    }, 1000);

    return () => clearInterval(interval);
  }, [jobId]);

  if (!job) return null;

  return (
    <div>
      <h2>Job Status</h2>
      <p>Status: {job.status}</p>
      {job.duration_ms && <p>Duration: {job.duration_ms.toFixed(2)} ms</p>}
    </div>
  );
}