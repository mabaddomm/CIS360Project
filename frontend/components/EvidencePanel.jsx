import React from "react";

export default function EvidencePanel({ rawData }) {
  return (
    <div className="card">
      <h2>Evidence</h2>
      <pre className="evidence-box">
        {JSON.stringify(rawData, null, 2)}
      </pre>
    </div>
  );
}