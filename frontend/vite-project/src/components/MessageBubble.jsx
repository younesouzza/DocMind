import { useState } from "react";

function SourceTag({ source }) {
  const [expanded, setExpanded] = useState(false);

  return (
    <div className={`source-tag ${expanded ? "expanded" : ""}`}>
      <button className="source-toggle" onClick={() => setExpanded((v) => !v)}>
        <span className="source-file">
          {source.source_type === "web" ? "🌐" : "◻"} {source.source}
        </span>
        {source.score != null && (
          <span className="source-score">{Math.round(source.score * 100)}%</span>
        )}
        <span className="source-chevron">{expanded ? "▲" : "▼"}</span>
      </button>
      {expanded && source.content && (
        <div className="source-excerpt">
          <p>{source.content}</p>
          {source.page && <span className="source-page">Page {source.page}</span>}
        </div>
      )}
    </div>
  );
}

function SourceBadge({ type }) {
  if (!type) return null;
  const isWeb = type === "web_search";
  return (
    <span className={`source-badge ${isWeb ? "web" : "doc"}`}>
      {isWeb ? "🌐 Web Search" : "◻ Documents"}
    </span>
  );
}

export default function MessageBubble({ message }) {
  const { role, content, sources, sourceType, confidence } = message;

  if (role === "user") {
    return (
      <div className="message user">
        <div className="message-body user-body">
          <p>{content}</p>
        </div>
        <div className="message-avatar user-avatar">U</div>
      </div>
    );
  }

  if (role === "error") {
    return (
      <div className="message error">
        <div className="message-avatar error-avatar">⚠</div>
        <div className="message-body error-body">
          <p>{content}</p>
        </div>
      </div>
    );
  }

  // Assistant
  return (
    <div className="message assistant">
      <div className="message-avatar">◈</div>
      <div className="message-body assistant-body">
        <div className="message-meta">
          <SourceBadge type={sourceType} />
          {confidence != null && (
            <span className="confidence-bar-wrap" title={`Confidence: ${Math.round(confidence * 100)}%`}>
              <span className="confidence-fill" style={{ width: `${Math.round(confidence * 100)}%` }} />
            </span>
          )}
        </div>

        <div className="message-content">
          {content.split("\n").map((line, i) =>
            line.trim() ? <p key={i}>{line}</p> : <br key={i} />
          )}
        </div>

        {sources?.length > 0 && (
          <div className="sources-section">
            <div className="sources-label">Sources</div>
            <div className="sources-list">
              {sources.map((src, i) => (
                <SourceTag key={i} source={src} />
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}