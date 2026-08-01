# AI Research Agent

A LangGraph-based research agent that takes a natural language question, searches multiple sources (web + Wikipedia), and synthesizes a cited, well-organized answer.

## How it works

The agent is a LangGraph `StateGraph` with the following flow:

1. **Analyze query** — rewrites the user's question into a focused search query using Gemini
2. **Search (parallel)** — queries Tavily (web) and Wikipedia simultaneously
3. **Evaluate sufficiency** — Gemini judges whether gathered sources are enough to answer well; if not, it generates a refined query and the agent searches again (capped at 3 iterations to prevent infinite loops)
4. **Summarize** — synthesizes all sources into one final, cited answer

## Setup

1. Clone this repo and create a virtual environment:
   \`\`\`bash
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   \`\`\`

2. Get free API keys:
   - Gemini: https://aistudio.google.com/apikey
   - Tavily: https://tavily.com

3. Copy `.env.example` to `.env` and add your keys:
   \`\`\`bash
   cp .env.example .env
   \`\`\`

## Usage

\`\`\`bash
python main.py
\`\`\`
You'll be prompted to enter a research question, and the agent will print a synthesized, cited answer.

## Tech stack

- **LangGraph** — agent orchestration (state graph, conditional routing, checkpointing)
- **Gemini 3.5 Flash** — LLM for query refinement, sufficiency evaluation, and summarization
- **Tavily** — web search API
- **Wikipedia REST API** — secondary knowledge source

## Project structure

\`\`\`
agent/
  state.py       # shared state schema (TypedDict)
  tools.py       # raw search functions (Tavily, Wikipedia)
  llm.py         # centralized LLM configuration
  nodes.py       # LangGraph node functions
  graph.py       # graph assembly and routing logic
tests/
  test_tools.py  # unit tests for search tools
main.py          # CLI entry point
\`\`\`

## Testing

\`\`\`bash
pytest tests/
\`\`\`

## 👩‍💻 Author

**Shreyaa Katiyar**

If you found this project helpful, consider giving it a ⭐ on GitHub.