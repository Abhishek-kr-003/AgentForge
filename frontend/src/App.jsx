import { useState } from "react";

function App() {
  const [message, setMessage] = useState("");
  
  const [messages, setMessages] = useState([]);

  const sendMessage = async () => {
     setMessages((previousMessages) => [
    ...previousMessages,
    {
      role: "user",
      content: message,
    },
  ]);

  setMessage("");

    const result = await fetch("http://localhost:8000/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message,
        messages: messages,
      }),
    });

    const data = await result.json();

    setMessages((previousMessages) => [
  ...previousMessages,
  {
    role: "assistant",
    content: data.message,
  },
]);
  };

  return (
    <div>
      <h1>AgentForge</h1>

      <input
        value={message}
        onChange={(e) => setMessage(e.target.value)}
        placeholder="Ask something..."
      />

      <button onClick={sendMessage}>
        Send
      </button>

     <div className="chat-container">
  {messages.map((msg, index) => (
    <div
      key={index}
      className={
        msg.role === "user"
          ? "message user-message"
          : "message assistant-message"
      }
    >
      <strong>
        {msg.role === "user" ? "You" : "AgentForge"}
      </strong>

      <p>{msg.content}</p>
    </div>
  ))}
</div>
    </div>
  );
}

export default App;