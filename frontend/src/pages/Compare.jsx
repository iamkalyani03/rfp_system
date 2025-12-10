import React, { useState } from "react";
import axios from "axios";

export default function Compare(){
  const [rfpId, setRfpId] = useState("");
  const [result, setResult] = useState(null);

  const doCompare = async () => {
    const res = await axios.get(`http://localhost:8000/compare/${rfpId}`);
    setResult(res.data);
  };

  return (
    <div>
      <h2>Compare Proposals</h2>
      <input placeholder="RFP ID" value={rfpId} onChange={e=>setRfpId(e.target.value)} />
      <button onClick={doCompare}>Compare</button>

      {result && <pre style={{ maxHeight: 400, overflow: "auto" }}>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
