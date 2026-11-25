
import { useState, useRef, useLayoutEffect } from "react";
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

  const [nextConversationNumber, setNextConversationNumber] =
    useState(2);

  const [activeConversation, setActiveConversation] =
    useState(1);

  // Reference to the chat container
  const chatContainerRef = useRef(null);

  // Automatically scroll to the latest message
  useLayoutEffect(() => {
    const chatContainer = chatContainerRef.current;

    if (!chatContainer) return;

    const animationFrame = requestAnimationFrame(() => {
      chatContainer.scrollTo({
        top: chatContainer.scrollHeight,
        behavior: "smooth",
      });
    });

    return () => cancelAnimationFrame(animationFrame);
  }, [messages]);

  // Send message to backend
  const sendMessage = async () => {
    if (!message.trim()) {
      return;
    }

    const currentMessage = message.trim();

    setMessages((previousMessages) => [
      ...previousMessages,
      {
        role: "user",
        content: currentMessage,
      },
    ]);

    setConversations((previous) =>
      previous.map((conversation) =>
        conversation.id === activeConversation
          ? {
              ...conversation,
              title:
                conversation.messages.length === 0
                  ? currentMessage.slice(0, 30) +
                    (currentMessage.length > 30 ? "..." : "")
                  : conversation.title,
              messages: [
                ...conversation.messages,
                {
                  role: "user",
                  content: currentMessage,
                },
              ],
            }
          : conversation
      )
    );

    setMessage("");

    try {
      const result = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          message: currentMessage,
          messages: messages,
        }),
      });

      if (!result.ok) {
        throw new Error("Backend request failed.");
      }

      const data = await result.json();

      const assistantMessage = {
        role: "assistant",
        content: data.message,
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        assistantMessage,
      ]);

      setConversations((previous) =>
        previous.map((conversation) =>
          conversation.id === activeConversation
            ? {
                ...conversation,
                messages: [
                  ...conversation.messages,
                  assistantMessage,
                ],
              }
            : conversation
        )
      );

    } catch (error) {
      console.error("Chat error:", error);

      const errorMessage = {
        role: "assistant",
        content:
          "Unable to connect to AgentForge backend. Please try again.",
      };

      setMessages((previousMessages) => [
        ...previousMessages,
        errorMessage,
      ]);

      setConversations((previous) =>
        previous.map((conversation) =>
          conversation.id === activeConversation
            ? {
                ...conversation,
                messages: [
                  ...conversation.messages,
                  errorMessage,
                ],
              }
            : conversation
        )
      );
    }
  };

  // Delete conversation
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

      {/* HEADER */}
      <header className="header">
        <h1>AgentForge</h1>
      </header>

      <div className="main-layout">

        {/* SIDEBAR */}
        <aside className="sidebar">

          {/* NEW CHAT BUTTON */}
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

              setNextConversationNumber(
                (number) => number + 1
              );
            }}
          >
            + New Chat
          </button>

          {/* CONVERSATION LIST */}
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
                  onClick={() =>
                    deleteConversation(conversation.id)
                  }
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

          {/* CHAT MESSAGES */}
          <div
            className="chat-container"
            ref={chatContainerRef}
          >
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
