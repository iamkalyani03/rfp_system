import React from "react";
import CreateRFP from "./pages/CreateRFP";
import Vendors from "./pages/Vendors";
import Compare from "./pages/Compare";

export default function App() {
  return (
    <div style={{ padding: 20, fontFamily: "Arial, sans-serif" }}>
      <h1>AI RFP Management</h1>
      <div style={{ display: "flex", gap: 20 }}>
        <div style={{ flex: 1 }}>
          <CreateRFP />
        </div>
        <div style={{ flex: 1 }}>
          <Vendors />
        </div>
        <div style={{ flex: 1 }}>
          <Compare />
        </div>
      </div>
    </div>
  );
}
