import { useNavigate } from "react-router-dom";
import { useState } from "react";
import api from "../api/client";

export default function Upload({ onJobCreated }) {
  const navigate = useNavigate();

  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("sequential");
  const [workers, setWorkers] = useState(1);

  const submit = async () => {
    if (!file) return alert("Select a file");

    const form = new FormData();
    form.append("file", file);

    const res = await api.post(
      `/jobs/upload?mode=${mode}&workers=${workers}`,
      form
    );

    onJobCreated?.(res.data.id); 
    navigate("/dashboard");
  };

  return (
    <div>
      <h2>Upload Log File</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />

      <select value={mode} onChange={e => setMode(e.target.value)}>
        <option value="sequential">Sequential</option>
        <option value="parallel">Parallel</option>
      </select>

      <select value={workers} onChange={e => setWorkers(Number(e.target.value))}>
        <option value={1}>1 Worker</option>
        <option value={2}>2 Workers</option>
        <option value={4}>4 Workers</option>
      </select>

      <button onClick={submit}>Start Job</button>
    </div>
  );
}
