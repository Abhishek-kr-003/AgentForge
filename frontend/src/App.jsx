import { useState } from "react";
import "./App.css";

function App() {
  const [message, setMessage] = useState("");
  
  const [messages, setMessages] = useState([]);
  const [conversations, setConversations] = useState([
  {
    id: 1,
    title: "Conversation 1",
    messages: [],
  },
]);


const [nextConversationNumber, setNextConversationNumber] = useState(2);
const [activeConversation, setActiveConversation] = useState(1);

  const sendMessage = async () => {
  if (!message.trim()) {
    return;
  }

  setMessages((previousMessages) => [
    ...previousMessages,
    {
      role: "user",
      content: message,
    },
  ]);

  setConversations((previous) =>
  previous.map((conversation) =>
    conversation.id === activeConversation
      ? {
          ...conversation,
          title:
            conversation.messages.length === 0
              ? message.trim().slice(0, 30) +
                (message.trim().length > 30 ? "..." : "")
              : conversation.title,
          messages: [
            ...conversation.messages,
            {
              role: "user",
              content: message,
            },
          ],
        }
      : conversation
  )
);

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
setConversations((previous) =>
  previous.map((conversation) =>
    conversation.id === activeConversation
      ? {
          ...conversation,
          messages: [
            ...conversation.messages,
            {
              role: "assistant",
              content: data.message,
            },
          ],
        }
      : conversation
  )
);
  };

  const deleteConversation = (id) => {
  const remainingConversations = conversations.filter(
    (conversation) => conversation.id !== id
  );

  setConversations(remainingConversations);

  if (activeConversation === id) {
    if (remainingConversations.length > 0) {
      const nextConversation = remainingConversations[0];

      setActiveConversation(nextConversation.id);
      setMessages(nextConversation.messages);
    } else {
      const newConversation = {
        id: Date.now(),
        title: "New Chat",
        messages: [],
      };

      setConversations([newConversation]);
      setActiveConversation(newConversation.id);
      setMessages([]);
    }
  }
};

  return (
     
  <div className="app">

    <header className="header">
      <h1>AgentForge</h1>
    </header>

    <div className="main-layout">

      {/* SIDEBAR */}
      <aside className="sidebar">

        <button
  className="new-chat-button"
  onClick={() => {
    const newConversation = {
      id: Date.now(),
      title: "New Chat",
      messages: [],
    };

    setConversations((previous) => [
      ...previous,
      newConversation,
    ]);

    setActiveConversation(newConversation.id);
    setMessages([]);
    setNextConversationNumber((number) => number + 1);
  }}
>
  + New Chat
</button>

        <div className="conversation-list">
  {conversations.map((conversation) => (
    <div
      key={conversation.id}
      className="conversation-row"
    >
      <button
        className="conversation-item"
        onClick={() => {
          setActiveConversation(conversation.id);
          setMessages(conversation.messages);
        }}
      >
        {conversation.title}
      </button>

      <button
        className="delete-chat-button"
        onClick={() => deleteConversation(conversation.id)}
        title="Delete conversation"
        aria-label={`Delete ${conversation.title}`}
      >
        🗑
      </button>
    </div>
  ))}
</div>

      </aside>


      {/* CHAT AREA */}
      <main className="chat-area">

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
                {msg.role === "user"
                  ? "You"
                  : "AgentForge"}
              </strong>

              <p>{msg.content}</p>
            </div>
          ))}

        </div>


        {/* INPUT AREA */}
        <div className="input-area">

          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") {
                e.preventDefault();
                sendMessage();
              }
            }}
            placeholder="Ask something..."
          />

          <button onClick={sendMessage}>
            Send
          </button>

        </div>

      </main>

    </div>

  </div>
);
}

export default App;