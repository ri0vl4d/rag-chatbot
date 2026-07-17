import { CORPUS_SUMMARY } from "../sampleQuestions";

export function CorpusSummary() {
  return (
    <div className="mx-auto max-w-2xl bg-bg-card border border-border-card rounded-xl p-6 mt-8">
      <h2 className="text-lg font-semibold text-accent-primary mb-2">
        {CORPUS_SUMMARY.title}
      </h2>
      <p className="text-sm text-text-primary mb-4 leading-relaxed">
        {CORPUS_SUMMARY.intro}
      </p>

      <div className="mb-4">
        <h3 className="text-xs font-semibold uppercase tracking-wide text-text-muted mb-2">
          Trained on 4 documents
        </h3>
        <ul className="space-y-1.5">
          {CORPUS_SUMMARY.sources.map((s, i) => (
            <li key={i} className="text-xs text-text-muted flex gap-2">
              <span className="text-accent-secondary font-mono">›</span>
              <span>{s}</span>
            </li>
          ))}
        </ul>
      </div>

      <div>
        <h3 className="text-xs font-semibold uppercase tracking-wide text-text-muted mb-2">
          How it behaves
        </h3>
        <ul className="space-y-1.5">
          {CORPUS_SUMMARY.guarantees.map((g, i) => (
            <li key={i} className="text-xs text-text-muted flex gap-2">
              <span className="text-emerald-400 font-mono">✓</span>
              <span>{g}</span>
            </li>
          ))}
        </ul>
      </div>

      <p className="text-xs text-text-muted mt-4 italic text-center">
        Try a sample question below, or type your own.
      </p>
    </div>
  );
}
