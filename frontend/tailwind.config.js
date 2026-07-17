/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        bg: { main: "#0b0f19", card: "#151b2b", elevated: "#1e2637" },
        border: { card: "#252d42" },
        text: { primary: "#e7ebf3", muted: "#8b93a7" },
        accent: { primary: "#7c8cff", secondary: "#4fd1c5" },
      },
      fontFamily: {
        sans: ["Inter", "system-ui", "sans-serif"],
        mono: ["JetBrains Mono", "monospace"],
      },
    },
  },
  plugins: [],
};
