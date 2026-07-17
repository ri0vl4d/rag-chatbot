export interface SampleCategory {
  key: string;
  label: string;
  description: string;
  color: string;
  questions: string[];
}

export const SAMPLE_QUESTIONS: SampleCategory[] = [
  {
    key: "direct",
    label: "Direct Retrieval",
    description: "Single-fact answers lifted from one chunk.",
    color: "bg-emerald-500/20 text-emerald-300 border-emerald-500/40",
    questions: [
      "Who is the product manager for Azure AI at TTBS and what is their contact number?",
      "What is the toll-free number for Azure AI support?",
      "How much is Progressive saving annually with AI-powered chatbots?",
      "Which Indian languages does the TTBS Azure OpenAI chatbot support?",
      "How many AI customers does TTBS Azure AI currently serve?",
    ],
  },
  {
    key: "synthesis",
    label: "Multi-chunk Synthesis",
    description: "Requires combining information across sections.",
    color: "bg-indigo-500/20 text-indigo-300 border-indigo-500/40",
    questions: [
      "List all six key value propositions of Azure AI.",
      "What are the three specialized use cases of TTBS Azure OpenAI Services and what does each do?",
      "Compare Cognitive Services and Applied AI Services — what is the difference?",
    ],
  },
  {
    key: "guard",
    label: "Hallucination Guard",
    description: "Not in the corpus — expect refusal.",
    color: "bg-rose-500/20 text-rose-300 border-rose-500/40",
    questions: [
      "What is the per-token pricing for Azure OpenAI GPT-4?",
      "Who is the current CEO of Microsoft?",
      "What was Tata Teleservices' revenue in FY2024?",
    ],
  },
  {
    key: "paraphrase",
    label: "Paraphrased",
    description: "Reworded questions — semantic search should still work.",
    color: "bg-amber-500/20 text-amber-300 border-amber-500/40",
    questions: [
      "How does Azure AI keep customer data safe?",
      "Whom should I reach out to if I want to discuss Azure AI at Tata?",
      "What kind of savings did EY achieve using intelligent document automation?",
    ],
  },
];

export const CORPUS_SUMMARY = {
  title: "About this chatbot",
  intro:
    "This assistant answers questions strictly from a Microsoft Azure AI sales & marketing corpus published by Tata Tele Business Services (TTBS).",
  sources: [
    "Azure AI Battlecard — value props, customer challenges, objection handling, testimonials, contacts",
    "Azure AI Customer Deck — industry trends, ROI stats (Progressive, EY, Carmax), product portfolio",
    "Azure AI Flyer — industry use cases and key features",
    "Azure AI Product Catalogue — Applied AI Services, Cognitive Services, Machine Learning, TTBS OpenAI use cases, FAQs",
  ],
  guarantees: [
    "Answers are grounded ONLY in the four source documents.",
    "If the answer isn't in the corpus, the bot will say so — it will not invent.",
    "Every answer shows the source chunks it used — click 'Sources' under any reply.",
  ],
};
