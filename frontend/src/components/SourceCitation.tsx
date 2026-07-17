import { useState } from "react";
import type { Source } from "../types";

export function SourceCitation({ sources }: { sources: Source[] }) {
  const [open, setOpen] = useState(false);
  if (!sources || sources.length === 0) return null;

  return (
    <div className="mt-2 border-t border-border-card pt-2">
      <button
        onClick={() => setOpen((v) => !v)}
        className="text-xs text-text-muted hover:text-accent-primary transition-colors"
      >
        {open ? "▼" : "▶"} Sources ({sources.length})
      </button>
      {open && (
        <div className="mt-2 space-y-2">
          {sources.map((s, i) => (
            <div key={i} className="rounded-md bg-bg-main p-2 text-xs">
              <div className="mb-1 font-mono text-accent-secondary">
                [{s.source}] chunk #{s.chunk_id ?? "?"}
              </div>
              <div className="text-text-muted whitespace-pre-wrap line-clamp-6">
                {s.content}
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
