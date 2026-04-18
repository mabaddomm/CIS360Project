import React from "react";

export default function SearchBox({ query, setQuery, onSearch, loading }) {
  return (
    <div className="search-box">
      <input
        type="text"
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        placeholder="Ask something like: Show me papers with U2 uncertainty for Satellite Imagery"
        className="search-input"
      />
      <button onClick={onSearch} className="search-button" disabled={loading}>
        {loading ? "Searching..." : "Ask"}
      </button>
    </div>
  );
}