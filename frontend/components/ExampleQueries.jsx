import React from "react";

export default function ExampleQueries({ setQuery }) {
  const examples = [
    "Show me all fusion methods used for Traffic Dataset.",
    "List all papers that report U2 uncertainty for Satellite Imagery.",
    "Find the most popular dataset in the graph.",
    "Find fusion methods applied to both Weather Dataset and Exchange Rate Dataset.",
    "Show papers whose methods include both U1 and U3 uncertainty."
  ];

  return (
    <div className="examples">
      <h3>Example Queries</h3>
      <div className="example-list">
        {examples.map((item, index) => (
          <button
            key={index}
            className="example-button"
            onClick={() => setQuery(item)}
          >
            {item}
          </button>
        ))}
      </div>
    </div>
  );
}