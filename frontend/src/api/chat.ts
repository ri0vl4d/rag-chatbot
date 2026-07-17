import type { ChatResponse, Message } from "../types";

const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000";

export async function sendChat(question: string, history: Message[]): Promise<ChatResponse> {
  const res = await fetch(`${API_URL}/api/chat`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({
      question,
      history: history.map(({ role, content }) => ({ role, content })),
    }),
  });
  if (!res.ok) {
    const detail = await res.text();
    throw new Error(`Backend error (${res.status}): ${detail}`);
  }
  return res.json();
}

export async function checkHealth(): Promise<{ status: string; indexed_chunks: number; model: string }> {
  const res = await fetch(`${API_URL}/health`);
  if (!res.ok) throw new Error("Backend unreachable");
  return res.json();
}
