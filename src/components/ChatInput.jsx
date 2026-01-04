import { useState } from "react";

export default function ChatInput({ onAsk, loading }) {
  const [query, setQuery] = useState("");

  const submit = () => {
    if (query.trim()) {
      onAsk(query);
    }
  };

  return (
    <div className="card">
      <textarea
        rows={3}
        placeholder="Ask a legal question..."
        value={query}
        onChange={(e) => setQuery(e.target.value)}
        style={{ width: "100%", padding: "10px" }}
      />
      <button onClick={submit} disabled={loading}>
        {loading ? "Thinking..." : "Ask LexGraph"}
      </button>
    </div>
  );
}
