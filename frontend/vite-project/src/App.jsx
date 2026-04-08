import { useState, useCallback } from "react";
import Sidebar from "./components/Sidebar";
import ChatPanel from "./components/ChatPanel";
import "./styles/globals.css";

export default function App() {
  const [documents, setDocuments] = useState([]);
  const [messages, setMessages] = useState([]);
  const [isQuerying, setIsQuerying] = useState(false);

  const addDocument = useCallback((doc) => {
    setDocuments((prev) => [...prev, doc]);
  }, []);

  const addMessage = useCallback((msg) => {
    setMessages((prev) => [...prev, msg]);
  }, []);

  return (
    <div className="app-shell">
      <header className="app-header">
        <div className="header-brand">
          <span className="brand-icon">◈</span>
          <span className="brand-name">DocMind</span>
          <span className="brand-tagline">Local AI Research Assistant</span>
        </div>
        <div className="header-status">
          <span className="status-dot" />
          <span className="status-label">Llama 3.2 · Ollama</span>
        </div>
      </header>

      <main className="app-body">
        <Sidebar documents={documents} onDocumentAdded={addDocument} />
        <ChatPanel
          messages={messages}
          onAddMessage={addMessage}
          isQuerying={isQuerying}
          setIsQuerying={setIsQuerying}
          hasDocuments={documents.length > 0}
        />
      </main>
    </div>
  );
}