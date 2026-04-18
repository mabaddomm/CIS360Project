import React from "react";

export default function AnswerCard({ answer, toolUsed }) {
  return (
    <div className="card">
      <h2>Answer</h2>
      <p style={{ whiteSpace: "pre-wrap" }}>{answer}</p>
      {toolUsed && (
        <p className="tool-line">
          <strong>Tool used:</strong> {toolUsed}
        </p>
      )}
    </div>
  );
}