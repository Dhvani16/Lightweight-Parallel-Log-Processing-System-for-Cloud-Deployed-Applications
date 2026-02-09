import { useEffect, useState } from "react";
import api from "../api/client";
import DurationBar from "../charts/DurationBar";

export default function Dashboard() {
  const [jobs, setJobs] = useState([]);
  const [results, setResults] = useState({});

  useEffect(() => {
    const fetchJobs = async () => {
      const res = await api.get("/jobs");
      setJobs(res.data);
    };

    fetchJobs();
    const interval = setInterval(fetchJobs, 1500);
    return () => clearInterval(interval);
  }, []);

  const cancelJob = async (id) => {
    await api.post(`/jobs/${id}/cancel`);
  };

  const fetchResult = async (jobId) => {
    if (results[jobId]) return;

    try {
      const res = await api.get(`/results/${jobId}`);
      setResults(prev => ({
        ...prev,
        [jobId]: res.data,
      }));
    } catch {
      // result not ready yet
    }
  };

  return (
    <div>
      <h2>Jobs</h2>

      {jobs.map((job) => {
        const progress = job.progress ?? 0;

        // 🔑 Trigger result fetch once job completes
        if (job.status === "completed") {
          fetchResult(job.id);
        }

        return (
          <div key={job.id} style={{ marginBottom: 20 }}>
            <div>
              <strong>Job #{job.id}</strong> — {job.status}
            </div>

            <div
              style={{
                background: "#eee",
                borderRadius: 4,
                overflow: "hidden",
              }}
            >
              <div
                style={{
                  width: `${progress}%`,
                  background:
                    job.status === "completed"
                      ? "green"
                      : job.status === "cancelled"
                      ? "red"
                      : "#007bff",
                  height: 12,
                  transition: "width 0.3s",
                }}
              />
            </div>

            <div>{progress}%</div>

            {job.status === "running" && (
              <button onClick={() => cancelJob(job.id)}>Cancel</button>
            )}

            {job.status === "completed" && (
              <>
                <div>Duration: {job.duration_ms.toFixed(2)} ms</div>

                {results[job.id] && (
                  <div style={{ marginTop: 6 }}>
                    <div>Total lines: {results[job.id].total_lines}</div>
                    <div>Errors: {results[job.id].error_count}</div>
                    <div>Warnings: {results[job.id].warning_count}</div>
                  </div>
                )}
              </>
            )}

            {job.status === "failed" && (
              <div style={{ color: "red", marginTop: 6 }}>
                Failed: {job.error_message || "Unknown error"}
              </div>
            )}
          </div>
        );
      })}

      <DurationBar jobs={jobs.filter((j) => j.status === "completed")} />
    </div>
  );
}