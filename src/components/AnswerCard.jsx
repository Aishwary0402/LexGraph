export default function AnswerCard({ answer }) {
  if (!answer) return null;

  return (
    <div className="card">
      <h3>📌 Final Answer</h3>
      <p>{answer}</p>
    </div>
  );
}
