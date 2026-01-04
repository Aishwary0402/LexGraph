export default function GraphView({ graph }) {
  if (!graph || !graph.nodes) {
    return <p>No graph data available.</p>;
  }

  return (
    <div className="mt-3 text-sm">
      <p><strong>Nodes:</strong> {graph.nodes.length}</p>
      <p><strong>Edges:</strong> {graph.edges.length}</p>

      <pre className="bg-slate-100 p-3 rounded mt-2 overflow-x-auto text-xs">
        {JSON.stringify(graph, null, 2)}
      </pre>
    </div>
  );
}
