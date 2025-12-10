import React, { useState } from "react";
import axios from "axios";

export default function CreateRFP(){
  const [text, setText] = useState("");
  const [result, setResult] = useState(null);

  const submit = async () => {
    const res = await axios.post("http://localhost:8000/rfp", { text });
    setResult(res.data.rfp);
  };

  return (
    <div>
      <h2>Create RFP</h2>
      <textarea rows={8} style={{ width: "100%" }} value={text} onChange={e=>setText(e.target.value)} />
      <button onClick={submit}>Create</button>
      {result && <pre style={{ maxHeight: 300, overflow: "auto" }}>{JSON.stringify(result, null, 2)}</pre>}
    </div>
  );
}
