import { useState } from "react";
import Login from "./pages/Login";
import Upload from "./pages/Upload";
import Dashboard from "./pages/Dashboard";

function App() {
  const [loggedIn, setLoggedIn] = useState(!!localStorage.getItem("token"));
  const [jobId, setJobId] = useState(null);

  if (!loggedIn) {
    return <Login onLogin={() => setLoggedIn(true)} />;
  }

  return (
    <div>
      <Upload onJobCreated={setJobId} />
      {jobId && <Dashboard jobId={jobId} />}
    </div>
  );
}

export default App;