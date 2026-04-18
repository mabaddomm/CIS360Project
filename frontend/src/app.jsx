import React, { useState } from "react";
import SearchBox from "../components/SearchBox";
import AnswerCard from "../components/AnswerCard";
import EvidencePanel from "../components/EvidencePanel";
import ExampleQueries from "../components/ExampleQueries";
import { askAgent } from "./services/api";

export default function App() {
  const [query, setQuery] = useState("");
  const [answer, setAnswer] = useState("");
  const [toolUsed, setToolUsed] = useState("");
  const [rawData, setRawData] = useState(null);
  const [loading, setLoading] = useState(false);
  const [showThinking, setShowThinking] = useState(false);
  const [error, setError] = useState("");

  const handleAsk = async () => {
    if (!query.trim()) {
      setError("Please enter a question.");
      return;
    }

    setLoading(true);
    setShowThinking(true);
    setError("");
    setAnswer("");
    setToolUsed("");
    setRawData(null);

    try {
      const result = await askAgent(query);

      await new Promise((r) => setTimeout(r, 800));

      setAnswer(result.answer || "No answer returned.");
      setToolUsed(result.tool_used || "");
      setRawData(result.raw_data || result.evidence || null);
    } catch (err) {
      setError(err.message || "Something went wrong.");
    } finally {
      setLoading(false);

      setTimeout(() => {
        setShowThinking(false);
      }, 300);
    }
  };

  return (
    <div className="container">
      <h1>ResearchAI Agent Search</h1>
      <p className="subtitle">
        Ask questions about papers, datasets, methods, and uncertainty.
      </p>

      <SearchBox
        query={query}
        setQuery={setQuery}
        onSearch={handleAsk}
        loading={loading}
      />

      <ExampleQueries setQuery={setQuery} />

      {error && <div className="error-box">{error}</div>}

      {showThinking && (
        <div className={`thinking-box ${loading ? "fade-in" : "fade-out"}`}>
          <span className="spinner"></span>
          <p>⏳ Model is thinking... working hard on your query...</p>
        </div>
      )}

      {answer && <AnswerCard answer={answer} toolUsed={toolUsed} />}

      {rawData && <EvidencePanel rawData={rawData} />}
    </div>
  );
}