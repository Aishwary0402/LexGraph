function ShapExplanation({ shap }) {
  if (!shap || !shap.explanation_ranked) {
    return <p>No explanation available.</p>;
  }

  return (
    <ul style={{ marginTop: "10px" }}>
      {shap.explanation_ranked.map((item, idx) => (
        <li key={idx} style={{ marginBottom: "8px" }}>
          <strong>Doc {item.doc_index}:</strong>{" "}
          {item.snippet.slice(0, 120)}...
        </li>
      ))}
    </ul>
  );
}

export default ShapExplanation;
