import { useEffect, useState } from "react";
import { ChatWindow } from "./components/ChatWindow";
import { InputBar } from "./components/InputBar";
import { SamplePanel } from "./components/SamplePanel";
import { checkHealth, sendChat } from "./api/chat";
import type { Message } from "./types";

export default function App() {
  const [messages, setMessages] = useState<Message[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [health, setHealth] = useState<{ chunks: number; model: string } | null>(null);

  useEffect(() => {
    checkHealth()
      .then((h) => setHealth({ chunks: h.indexed_chunks, model: h.model }))
      .catch(() => setHealth(null));
  }, []);

  const handleSend = async (text: string) => {
    setError(null);
    const userMsg: Message = { role: "user", content: text };
    const next = [...messages, userMsg];
    setMessages(next);
    setLoading(true);
    try {
      const res = await sendChat(text, next);
      setMessages([...next, { role: "assistant", content: res.answer, sources: res.sources }]);
    } catch (e) {
      setError(e instanceof Error ? e.message : "Unknown error");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="flex flex-col h-full bg-bg-main">
      <header className="border-b border-border-card bg-bg-card px-4 py-3">
        <div className="max-w-4xl mx-auto flex items-center justify-between">
          <div>
            <h1 className="text-lg font-semibold">Azure AI RAG Chatbot</h1>
            <p className="text-xs text-text-muted">
              NVIDIA NIM · MiniLM embeddings · FAISS · grounded in TTBS Azure AI collateral
            </p>
          </div>
          {health && (
            <div className="text-right text-xs text-text-muted">
              <div className="font-mono text-accent-secondary">{health.chunks} chunks indexed</div>
              <div className="font-mono">{health.model}</div>
            </div>
          )}
        </div>
      </header>

      {error && (
        <div className="bg-red-900/40 border-b border-red-700 px-4 py-2 text-sm text-red-200 text-center">
          {error}
        </div>
      )}

      <main className="flex-1 flex flex-col overflow-hidden max-w-4xl mx-auto w-full">
        <ChatWindow messages={messages} loading={loading} />
        <SamplePanel onPick={handleSend} disabled={loading} />
        <InputBar onSend={handleSend} disabled={loading} />
      </main>
    </div>
  );
}
