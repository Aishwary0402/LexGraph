function ChatBubble({ role, children }) {
  const isUser = role === "user";

  return (
    <div
      style={{
        display: "flex",
        justifyContent: isUser ? "flex-end" : "flex-start",
        marginBottom: "16px",
      }}
    >
      <div
        style={{
          maxWidth: "75%",
          padding: "16px 18px",
          borderRadius: "18px",
          backgroundColor: isUser ? "#2563eb" : "#f1f5f9",
          color: isUser ? "#ffffff" : "#0f172a",
          boxShadow: "0 6px 16px rgba(0,0,0,0.15)",
          whiteSpace: "pre-wrap",
          lineHeight: "1.6",
          fontSize: "15px",
        }}
      >
        {children}
      </div>
    </div>
  );
}

export default ChatBubble;
