import { useState } from "react";
import api from "../api/client";

export default function Upload({ onJobCreated }) {
  const [file, setFile] = useState(null);
  const [mode, setMode] = useState("sequential");
  const [workers, setWorkers] = useState(1);

  const submit = async () => {
    const form = new FormData();
    form.append("file", file);

    const res = await api.post(
      `/jobs/upload?mode=${mode}&workers=${workers}`,
      form
    );

    onJobCreated(res.data.id);
  };

  return (
    <div>
      <h2>Upload Log File</h2>

      <input type="file" onChange={e => setFile(e.target.files[0])} />

      <select onChange={e => setMode(e.target.value)}>
        <option value="sequential">Sequential</option>
        <option value="parallel">Parallel</option>
      </select>

      <select onChange={e => setWorkers(Number(e.target.value))}>
        <option value={1}>1 Worker</option>
        <option value={2}>2 Workers</option>
        <option value={4}>4 Workers</option>
      </select>

      <button onClick={submit}>Start Job</button>
    </div>
  );
}