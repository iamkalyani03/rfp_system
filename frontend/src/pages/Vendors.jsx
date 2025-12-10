import React, { useEffect, useState } from "react";
import axios from "axios";

export default function Vendors(){
  const [vendors, setVendors] = useState([]);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [rfpIdToSend, setRfpIdToSend] = useState("");
  const [selected, setSelected] = useState([]);

  async function load(){
    const v = await axios.get("http://localhost:8000/vendors");
    setVendors(v.data);
  }
  useEffect(()=>{ load(); }, []);

  const add = async () => {
    await axios.post("http://localhost:8000/vendors", { name, email });
    setName(""); setEmail("");
    load();
  };

  const toggle = id => {
    setSelected(s => s.includes(id) ? s.filter(x=>x!==id) : [...s, id]);
  };

  const send = async () => {
    await axios.post("http://localhost:8000/vendors/send-rfp", { vendor_ids:selected, rfp_id: Number(rfpIdToSend) });
    alert("Sent (background).");
  };

  return (
    <div>
      <h2>Vendors</h2>
      <input placeholder="Name" value={name} onChange={e=>setName(e.target.value)} />
      <input placeholder="Email" value={email} onChange={e=>setEmail(e.target.value)} />
      <button onClick={add}>Add Vendor</button>

      <h3>Existing</h3>
      <div style={{ maxHeight: 200, overflow: "auto" }}>
        {vendors.map(v => (
          <div key={v.id}>
            <input type="checkbox" checked={selected.includes(v.id)} onChange={()=>toggle(v.id)} /> {v.name} ({v.email})
          </div>
        ))}
      </div>

      <div>
        <input placeholder="RFP ID to send" value={rfpIdToSend} onChange={e=>setRfpIdToSend(e.target.value)} />
        <button onClick={send}>Send RFP</button>
      </div>
    </div>
  );
}
