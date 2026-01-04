import { useState } from "react";
import ChatBubble from "../components/ChatBubble";
import ShapExplanation from "../components/ShapExplanation";
import EvidenceTable from "../components/EvidenceTable";
import GraphView from "../components/GraphView";
import GraphBubble from "../components/GraphView";



function ChatbotPage() {
  const [messages, setMessages] = useState([]);
  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);

  const askQuestion = async () => {
    if (!question.trim()) return;

    const userMsg = { role: "user", content: question };
    setMessages((prev) => [...prev, userMsg]);
    setQuestion("");
    setLoading(true);

    const res = await fetch("http://localhost:8000/api/ask", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ question }),
    });

    const data = await res.json();
    console.log("API RESPONSE:", data);

    setMessages((prev) => [
      ...prev,
      { role: "assistant", content: data.answer },
      { role: "shap", content: data.shap_explanation },
      { role: "evidence", content: data.shap_explanation.explanation_ranked },
      { role: "graph", content: data.graph },
    ]);

    setLoading(false);
  };

  return (
    <div
      style={{
        minHeight: "100vh",
        background: "linear-gradient(135deg, #020617, #0f172a)",
        padding: "40px 0",
      }}
    >
      <div
        style={{
          maxWidth: "900px",
          margin: "auto",
          background: "#ffffff",
          borderRadius: "18px",
          padding: "24px",
          boxShadow: "0 30px 60px rgba(0,0,0,0.35)",
        }}
      >
        <h1 style={{ fontSize: "26px", fontWeight: "700", marginBottom: "20px" }}>
          ⚖️ LexGraph Legal Assistant
        </h1>

        <div style={{ minHeight: "400px", marginBottom: "20px" }}>
          {messages.map((msg, idx) => {
            if (msg.role === "user") {
              return (
                <ChatBubble key={idx} role="user">
                  {msg.content}
                </ChatBubble>
              );
            }

            if (msg.role === "assistant") {
              return (
                <ChatBubble key={idx} role="assistant">
                  {msg.content}
                </ChatBubble>
              );
            }

            if (msg.role === "shap") {
                return (
                    <ChatBubble key={idx} role="assistant">
                    <strong>🧠 Why this answer?</strong>
                    <p style={{ marginTop: "8px" }}>
                        {msg.content.summary || "Explanation generated from legal evidence."}
                    </p>
                    <ShapExplanation shap={msg.content} />
                    </ChatBubble>
                );
            }


            if (msg.role === "evidence") {
              return (
                <ChatBubble key={idx} role="assistant">
                  <strong>🧾 Evidence</strong>
                  <EvidenceTable evidence={msg.content} />
                </ChatBubble>
              );
            }
            if (msg.role === "graph") {
                return (
                    <ChatBubble key={idx} role="assistant">
                    <strong>🕸 Legal Reasoning Graph</strong>
                    <GraphView graph={msg.content} />
                    </ChatBubble>
                );


            }

            return null;
          })}

          {loading && (
            <ChatBubble role="assistant">
              ⏳ Thinking…
            </ChatBubble>
          )}
        </div>

        <div style={{ display: "flex", gap: "10px" }}>
          <textarea
            value={question}
            onChange={(e) => setQuestion(e.target.value)}
            placeholder="Describe your legal issue..."
            style={{
              flex: 1,
              padding: "12px",
              borderRadius: "10px",
              border: "1px solid #cbd5f5",
              resize: "none",
            }}
          />
          <button
            onClick={askQuestion}
            style={{
              background: "#2563eb",
              color: "white",
              padding: "12px 20px",
              borderRadius: "10px",
              fontWeight: "600",
            }}
          >
            Ask
          </button>
        </div>
      </div>
    </div>
  );
}

export default ChatbotPage;
