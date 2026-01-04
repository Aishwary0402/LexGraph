import ForceGraph2D from "react-force-graph-2d";
import { useRef, useEffect } from "react";

export default function GraphView({ graph }) {
  const fgRef = useRef();

  if (!graph || !graph.nodes || !graph.edges) {
    return <p>No graph data available.</p>;
  }

  const graphData = {
    nodes: graph.nodes.map((n) => ({
      id: n.id,
      label: n.label,
      type: n.type || "DEFAULT",
    })),
    links: graph.edges.map((e) => ({
      source: e.source,
      target: e.target,
      label: e.relation,
    })),
  };

  // ✅ Center graph AFTER physics finishes
  useEffect(() => {
    if (fgRef.current) {
      fgRef.current.d3Force("charge").strength(-180);
    }
  }, []);

  return (
    <div
      style={{
        height: "500px",
        width: "100%",
        background: "#020617",
        borderRadius: "12px",
        overflow: "hidden",
      }}
    >
      <ForceGraph2D
        ref={fgRef}
        graphData={graphData}
        backgroundColor="#020617"

        /* ---------- PHYSICS ---------- */
        linkDistance={100}
        d3VelocityDecay={0.4}
        cooldownTicks={200}
        onEngineStop={() => fgRef.current.zoomToFit(400)}

        /* ---------- NODES ---------- */
        nodeRelSize={3}
        nodeCanvasObject={(node, ctx, globalScale) => {
          const label = node.label;
          const fontSize = 9 / globalScale;
          ctx.font = `${fontSize}px Sans-Serif`;

          const padding = 4;
          const textWidth = ctx.measureText(label).width;
          const width = textWidth + padding * 2;
          const height = fontSize + padding * 2;

          const colors = {
            ANSWER: "#22c55e",
            EVIDENCE: "#38bdf8",
            LAW: "#2563eb",
            SECTION: "#a78bfa",
            REMEDY: "#ef4444",
            DEFAULT: "#64748b",
          };

          ctx.fillStyle = colors[node.type] || colors.DEFAULT;
          ctx.fillRect(
            node.x - width / 2,
            node.y - height / 2,
            width,
            height
          );

          ctx.textAlign = "center";
          ctx.textBaseline = "middle";
          ctx.fillStyle = "#ffffff";
          ctx.fillText(label, node.x, node.y);
        }}

        /* ---------- LINKS ---------- */
        linkColor={() => "#94a3b8"}
        linkDirectionalArrowLength={6}
        linkDirectionalArrowRelPos={1}
        linkLabel={(link) => link.label}
      />
    </div>
  );
}
