import type { Message } from "../types";
import { SourceCitation } from "./SourceCitation";

export function MessageBubble({ message }: { message: Message }) {
  const isUser = message.role === "user";
  return (
    <div className={`flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[85%] rounded-2xl px-4 py-3 ${
          isUser
            ? "bg-accent-primary text-white"
            : "bg-bg-card text-text-primary border border-border-card"
        }`}
      >
        <div className="whitespace-pre-wrap text-sm leading-relaxed">{message.content}</div>
        {!isUser && message.sources && <SourceCitation sources={message.sources} />}
      </div>
    </div>
  );
}
