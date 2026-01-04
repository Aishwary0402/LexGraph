import React from "react";

function GraphBubble({ graph }) {
  if (!graph || !graph.nodes?.length) {
    return <p>No graph data available.</p>;
  }

  return (
    <div>
      <h4>🧠 Legal Reasoning Graph</h4>
      <ul>
        {graph.edges.map((e, i) => (
          <li key={i}>
            {e.source} → <strong>{e.relation}</strong> → {e.target}
          </li>
        ))}
      </ul>
    </div>
  );
}

export default GraphBubble;
