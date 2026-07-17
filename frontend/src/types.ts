export type Role = "user" | "assistant";

export interface Message {
  role: Role;
  content: string;
  sources?: Source[];
}

export interface Source {
  content: string;
  source: string;
  chunk_id?: number | null;
}

export interface ChatResponse {
  answer: string;
  sources: Source[];
}
