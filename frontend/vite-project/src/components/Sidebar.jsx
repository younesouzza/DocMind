import { useState, useRef } from "react";
import axios from "axios";

const API = "http://127.0.0.1:8000";

const FILE_ICONS = {
  pdf: "⬛",
  docx: "⬜",
  doc: "⬜",
  txt: "▭",
  png: "▣",
  jpg: "▣",
  jpeg: "▣",
  webp: "▣",
};

function fileIcon(name) {
  const ext = name.split(".").pop()?.toLowerCase();
  return FILE_ICONS[ext] || "▪";
}

function formatSize(bytes) {
  if (!bytes) return "";
  if (bytes < 1024) return `${bytes}B`;
  if (bytes < 1024 * 1024) return `${(bytes / 1024).toFixed(1)}KB`;
  return `${(bytes / (1024 * 1024)).toFixed(1)}MB`;
}

export default function Sidebar({ documents, onDocumentAdded }) {
  const [uploading, setUploading] = useState(false);
  const [dragOver, setDragOver] = useState(false);
  const [uploadError, setUploadError] = useState(null);
  const [uploadProgress, setUploadProgress] = useState(null);
  const fileRef = useRef();

  const upload = async (file) => {
    setUploading(true);
    setUploadError(null);
    setUploadProgress(`Uploading ${file.name}…`);

    const form = new FormData();
    form.append("file", file);

    try {
      const { data } = await axios.post(`${API}/api/upload`, form, {
        headers: { "Content-Type": "multipart/form-data" },
      });
      onDocumentAdded({
        id: data.doc_id,
        name: data.filename,
        chunks: data.chunks_created,
        size: file.size,
        uploadedAt: new Date(),
      });
      setUploadProgress(null);
    } catch (err) {
      setUploadError(
        err.response?.data?.detail || "Upload failed. Is the backend running?"
      );
      setUploadProgress(null);
    } finally {
      setUploading(false);
    }
  };

  const handleFiles = (files) => {
    const allowed = ["pdf", "docx", "doc", "txt", "png", "jpg", "jpeg", "webp"];
    for (const file of files) {
      const ext = file.name.split(".").pop()?.toLowerCase();
      if (allowed.includes(ext)) {
        upload(file);
      } else {
        setUploadError(`Unsupported file type: .${ext}`);
      }
    }
  };

  const onDrop = (e) => {
    e.preventDefault();
    setDragOver(false);
    handleFiles([...e.dataTransfer.files]);
  };

  return (
    <aside className="sidebar">
      <div className="sidebar-section-label">Documents</div>

      {/* Upload Zone */}
      <div
        className={`upload-zone ${dragOver ? "drag-over" : ""} ${uploading ? "uploading" : ""}`}
        onDragOver={(e) => { e.preventDefault(); setDragOver(true); }}
        onDragLeave={() => setDragOver(false)}
        onDrop={onDrop}
        onClick={() => !uploading && fileRef.current?.click()}
      >
        <input
          ref={fileRef}
          type="file"
          hidden
          multiple
          accept=".pdf,.docx,.doc,.txt,.png,.jpg,.jpeg,.webp"
          onChange={(e) => handleFiles([...e.target.files])}
        />
        {uploading ? (
          <div className="upload-zone-inner">
            <div className="upload-spinner" />
            <span className="upload-hint">{uploadProgress}</span>
          </div>
        ) : (
          <div className="upload-zone-inner">
            <span className="upload-icon">⊕</span>
            <span className="upload-hint">
              Drop files or click to upload
            </span>
            <span className="upload-types">PDF · DOCX · TXT · Images</span>
          </div>
        )}
      </div>

      {uploadError && (
        <div className="upload-error" onClick={() => setUploadError(null)}>
          ⚠ {uploadError}
        </div>
      )}

      {/* Document List */}
      <div className="doc-list">
        {documents.length === 0 ? (
          <div className="doc-empty">No documents yet</div>
        ) : (
          documents.map((doc) => (
            <div className="doc-item" key={doc.id}>
              <span className="doc-icon">{fileIcon(doc.name)}</span>
              <div className="doc-meta">
                <span className="doc-name" title={doc.name}>{doc.name}</span>
                <span className="doc-info">
                  {doc.chunks} chunks · {formatSize(doc.size)}
                </span>
              </div>
              <span className="doc-badge">✓</span>
            </div>
          ))
        )}
      </div>

      <div className="sidebar-footer">
        <span>{documents.length} document{documents.length !== 1 ? "s" : ""} indexed</span>
      </div>
    </aside>
  );
}