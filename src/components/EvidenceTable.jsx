function EvidenceTable({ evidence }) {
  if (!evidence || evidence.length === 0) {
    return <p>No evidence found.</p>;
  }

  return (
    <table
      style={{
        width: "100%",
        marginTop: "12px",
        borderCollapse: "collapse",
      }}
    >
      <thead>
        <tr>
          <th style={th}>Doc</th>
          <th style={th}>SHAP Score</th>
          <th style={th}>Snippet</th>
        </tr>
      </thead>
      <tbody>
        {evidence.map((e, i) => (
          <tr key={i}>
            <td style={td}>{e.doc_index}</td>
            <td style={td}>{e.shap_importance.toFixed(4)}</td>
            <td style={td}>{e.snippet.slice(0, 120)}...</td>
          </tr>
        ))}
      </tbody>
    </table>
  );
}

const th = {
  borderBottom: "2px solid #e5e7eb",
  padding: "8px",
  textAlign: "left",
};

const td = {
  padding: "8px",
  borderBottom: "1px solid #e5e7eb",
};

export default EvidenceTable;
