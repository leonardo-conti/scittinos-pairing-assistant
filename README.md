🍝 Scittino’s AI Pairing Assistant

An AI-powered culinary recommendation system that generates customized food & drink pairings for events, 
designed for Scittino’s Italian Market & Deli. The assistant suggests curated menus based on event type,
audience, and constraints, drawing from Scittino’s catering, bakery, and butcher shop offerings.

🧠 Project Overview

This project builds an intelligent assistant that blends AI reasoning, structured retrieval, and culinary knowledge.
The assistant can:

Suggest Italian-inspired pairings for events (e.g., pizza night, office party, Ravens tailgate).

Use a Scittino’s-based knowledge base (KB) for deterministic recommendations.

Fall back on AI generation (Anthropic Claude) when no preset fits.

Output structured JSON (via Pydantic) or formatted, human-readable menus.

Persist results to file, creating printable event pairing summaries.

⚙️ Tech Stack
Component	Purpose
Python 3.13+	Core language
LangChain	LLM orchestration & tool management
Anthropic Claude 3.5 Sonnet	AI reasoning model for dynamic recommendations
Pydantic	Structured output parsing and validation
DuckDuckGo Search	Optional search enrichment tool
Wikipedia API	Context enrichment for culinary terms
dotenv	Secure API key management
tabulate	Clean, terminal-friendly tables
Custom Tools	Scittino’s KB lookup, file saver, fallback AI pairing
🧩 Folder Structure
researchAgent/
│
├── main.py          # Orchestrates the AI agent, CLI interface, and parsing
├── kb.py            # Scittino’s curated pairing presets (Italian food, market, bakery)
├── tools.py         # Tool definitions: search, wiki, KB, save-to-file
├── requirements.txt # Dependencies
└── .env             # Contains ANTHROPIC_API_KEY

🚀 How to Run
1. Clone and set up
git clone https://github.com/leonardo-conti/scittinos-pairing-assistant.git
cd scittinos-pairing-assistant
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

2. Add your Anthropic API key

Create a .env file:

ANTHROPIC_API_KEY=sk-ant-xxxxxxxxxxxxxxxxxxxxxxxx

3. Run the assistant
python3 main.py


You’ll see:

🍽️ Pairings Assistant — type 'exit' to quit.


Example:

What event + any constraints? pizza night

💬 Example Output (CLI)
🍝  PIZZA NIGHT RECOMMENDATIONS  🍷
==================================

Audience     : Mixed family
Cuisine      : Italian
Constraints  : —

╒═══════════════╤══════════════════════════════════════════════════════╕
│ Course        │ Recommendations                                      │
╞═══════════════╪══════════════════════════════════════════════════════╡
│ Appetizers    │ • Garlic knots                                       │
│               │ • Arancini (Sicilian rice balls)                     │
│               │ • House salad                                        │
├───────────────┼──────────────────────────────────────────────────────┤
│ Mains         │ • Scittino’s pizzas (Cheese, Pepperoni, Margherita)  │
│               │ • Stromboli                                          │
│               │ • Calzone                                            │
╘═══════════════╧══════════════════════════════════════════════════════╛

WHY THIS WORKS
---------------
A balanced menu featuring Scittino’s signature Italian comfort foods, 
with both hot and cold options perfect for sharing.

✅ Family-style • Based on Scittino’s menu & market

🗂️ Example Saved File

Saved in pairings_output.txt with clear formatting:

🍝  SCITTINO’S PAIRING RECOMMENDATION  🍷
Generated on: 2025-10-27 22:31:11

Event: Pizza Night
---------------------------------------------
Appetizers:
  • Garlic knots
  • Arancini (Sicilian rice balls)
  • House salad
Mains:
  • Scittino’s signature pizzas
  • Stromboli
  • Calzone
Drinks (Non-Alcoholic):
  • Lemonade
  • Sparkling water

Rationale:
  Classic Italian comfort fare highlighting Scittino’s deli and bakery.
Sources:
  • Scittino’s KB
============================================================

💡 Features

✅ Dynamic Dual-Mode Generation

Uses deterministic Scittino’s KB first

Falls back to AI if event not found

✅ Human-Readable Outputs

Pretty CLI tables and saved summaries

✅ Structured JSON Parsing

Every response validated with Pydantic schema

✅ Safe & Extendable Architecture

Easily plug in new sources or replace the model

✅ Future Expansion

Streamlit or FastAPI front-end for customer use

PDF export of event menus

Personalized recommendations via embeddings

🏗️ Future Enhancements
Feature	Description
🖥️ Web Dashboard	Streamlit app for event entry + downloadable menu cards
🧾 PDF Export	Generate branded menu PDFs for catering clients
🧠 Learning Mode	Remember user feedback (like/dislike dishes)
🥂 Seasonal Specials	Rotate bakery/catering items by month
🔍 Vector Search	Use embeddings to suggest similar pairings
🧑‍💻 Author

Leo Conti
B.S. Computer Science, University of Maryland
AI & Business Integration | Data Science | Product Innovation