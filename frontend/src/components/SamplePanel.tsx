import { useState } from "react";
import { SAMPLE_QUESTIONS } from "../sampleQuestions";

interface Props {
  onPick: (question: string) => void;
  disabled: boolean;
}

export function SamplePanel({ onPick, disabled }: Props) {
  const [open, setOpen] = useState(true);
  const [activeCat, setActiveCat] = useState(SAMPLE_QUESTIONS[0].key);

  const cat = SAMPLE_QUESTIONS.find((c) => c.key === activeCat)!;

  return (
    <div className="border-t border-border-card bg-bg-card">
      <button
        onClick={() => setOpen((v) => !v)}
        className="w-full max-w-4xl mx-auto flex items-center justify-between px-4 py-2 text-sm text-text-muted hover:text-accent-primary transition-colors"
      >
        <span className="font-medium">
          {open ? "▼" : "▶"} Sample Questions for Evaluation ({SAMPLE_QUESTIONS.reduce((n, c) => n + c.questions.length, 0)})
        </span>
        <span className="text-xs">Click any question to run it</span>
      </button>

      {open && (
        <div className="max-w-4xl mx-auto px-4 pb-3">
          <div className="flex flex-wrap gap-2 mb-3">
            {SAMPLE_QUESTIONS.map((c) => (
              <button
                key={c.key}
                onClick={() => setActiveCat(c.key)}
                className={`px-3 py-1 rounded-full text-xs font-medium border transition-colors ${
                  activeCat === c.key
                    ? c.color
                    : "bg-bg-elevated text-text-muted border-border-card hover:text-text-primary"
                }`}
              >
                {c.label} ({c.questions.length})
              </button>
            ))}
          </div>

          <p className="text-xs text-text-muted mb-2 italic">{cat.description}</p>

          <div className="grid gap-2 sm:grid-cols-2">
            {cat.questions.map((q, i) => (
              <button
                key={i}
                onClick={() => onPick(q)}
                disabled={disabled}
                className="text-left text-sm bg-bg-elevated border border-border-card rounded-lg px-3 py-2 hover:border-accent-primary hover:bg-bg-main transition-colors disabled:opacity-40 disabled:cursor-not-allowed"
              >
                <span className="text-accent-secondary font-mono text-xs mr-2">Q{i + 1}.</span>
                {q}
              </button>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}
