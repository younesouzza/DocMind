import { useState, useRef, useEffect } from "react";
import axios from "axios";
import MessageBubble from "./MessageBubble";

const API = "http://127.0.0.1:8000";

export default function ChatPanel({ messages, onAddMessage, isQuerying, setIsQuerying, hasDocuments }) {
  const [input, setInput] = useState("");
  const [error, setError] = useState(null);
  const bottomRef = useRef();
  const textareaRef = useRef();

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages, isQuerying]);

  const submit = async () => {
    const q = input.trim();
    if (!q || isQuerying) return;

    setInput("");
    setError(null);
    setIsQuerying(true);

    onAddMessage({ role: "user", content: q, id: Date.now() });

    try {
        const { data } = await axios.post(`${API}/api/query`, { question: q });
      onAddMessage({
        role: "assistant",
        content: data.answer,
        sources: data.sources || [],
        sourceType: data.source_type,
        confidence: data.confidence,
        id: Date.now() + 1,
      });
    } catch (err) {
      setError(err.response?.data?.detail || "Query failed. Is the backend running?");
      onAddMessage({
        role: "error",
        content: err.response?.data?.detail || "Something went wrong. Please try again.",
        id: Date.now() + 1,
      });
    } finally {
      setIsQuerying(false);
    }
  };

  const onKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      submit();
    }
  };

  // Auto-resize textarea
  const handleInput = (e) => {
    setInput(e.target.value);
    const ta = textareaRef.current;
    if (ta) {
      ta.style.height = "auto";
      ta.style.height = Math.min(ta.scrollHeight, 160) + "px";
    }
  };

  return (
    <section className="chat-panel">
      {/* Messages */}
      <div className="messages-area">
        {messages.length === 0 ? (
          <div className="chat-empty">
            <div className="chat-empty-icon">◈</div>
            <div className="chat-empty-title">Ask anything about your documents</div>
            <div className="chat-empty-sub">
              {hasDocuments
                ? "Your documents are indexed and ready."
                : "Upload documents in the sidebar to get started, or ask a general question."}
            </div>
            <div className="chat-suggestions">
              {[
                "Summarize the main points",
                "What are the key findings?",
                "List all mentioned dates",
                "Who are the main authors?",
              ].map((s) => (
                <button
                  key={s}
                  className="suggestion-chip"
                  onClick={() => { setInput(s); textareaRef.current?.focus(); }}
                >
                  {s}
                </button>
              ))}
            </div>
          </div>
        ) : (
          <>
            {messages.map((msg) => (
              <MessageBubble key={msg.id} message={msg} />
            ))}
            {isQuerying && (
              <div className="message assistant thinking">
                <div className="message-avatar">◈</div>
                <div className="message-body">
                  <div className="thinking-dots">
                    <span /><span /><span />
                  </div>
                </div>
              </div>
            )}
          </>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div className="input-bar">
        <div className="input-wrap">
          <textarea
            ref={textareaRef}
            className="chat-input"
            rows={1}
            placeholder="Ask a question about your documents…"
            value={input}
            onChange={handleInput}
            onKeyDown={onKeyDown}
            disabled={isQuerying}
          />
          <button
            className={`send-btn ${isQuerying || !input.trim() ? "disabled" : ""}`}
            onClick={submit}
            disabled={isQuerying || !input.trim()}
            title="Send (Enter)"
          >
            {isQuerying ? <span className="send-spinner" /> : "⟶"}
          </button>
        </div>
        <div className="input-hint">
          Enter to send · Shift+Enter for new line
        </div>
      </div>
    </section>
  );
}