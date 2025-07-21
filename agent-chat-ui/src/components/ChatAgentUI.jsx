import React, { useState } from "react";

export default function ChatAgentUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const sendMessage = async () => {
    if (!input.trim()) return;
    const res = await fetch("/api/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input }),
    });
    const data = await res.json();
    setMessages([...messages, { role: "user", content: input }, { role: "agent", content: data.reply }]);
    setInput("");
  };

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <div style={{ maxHeight: "400px", overflowY: "auto", marginBottom: "1rem" }}>
        {messages.map((msg, idx) => (
          <div key={idx} style={{ marginBottom: "0.5rem" }}>
            <strong>{msg.role}:</strong> {msg.content}
          </div>
        ))}
      </div>
      <input
        value={input}
        onChange={e => setInput(e.target.value)}
        placeholder="Ask the agent..."
        style={{ width: "80%", padding: "0.5rem" }}
      />
      <button onClick={sendMessage} style={{ marginLeft: "1rem", padding: "0.5rem 1rem" }}>Send</button>
    </div>
  );
}

