# main.py
import os
import shutil
import textwrap
import unicodedata
from dotenv import load_dotenv
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, Field
from langchain_anthropic import ChatAnthropic
from langchain.output_parsers import PydanticOutputParser, OutputFixingParser
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain.agents import create_tool_calling_agent, AgentExecutor
from tools import search_tool, wiki_tool, pairing_kb_tool
from tabulate import tabulate



load_dotenv()  # expects ANTHROPIC_API_KEY in .env

# ---------- schema ----------
class MenuSection(BaseModel):
    appetizers: List[str] = Field(default_factory=list)
    mains: List[str] = Field(default_factory=list)
    sides: List[str] = Field(default_factory=list)
    desserts: List[str] = Field(default_factory=list)

class DrinkSection(BaseModel):
    alcoholic: List[str] = Field(default_factory=list)
    non_alcoholic: List[str] = Field(default_factory=list)

class PairingResponse(BaseModel):
    event: str
    audience: Optional[str] = None      # "adults", "kids", "mixed", "21+"
    constraints: List[str] = Field(default_factory=list)  # e.g., ["vegetarian","nut-free","budget:$"]
    cuisine_pref: Optional[str] = None  # e.g., "italian"
    menu: MenuSection
    drinks: DrinkSection
    rationale: str
    sources: List[str] = Field(default_factory=list)
    tools_used: List[str] = Field(default_factory=list)

# ---------- LLM ----------
llm = ChatAnthropic(model="claude-3-5-sonnet-20241022", temperature=0.2)

# ---------- parsers ----------
target_parser = PydanticOutputParser(pydantic_object=PairingResponse)
fixing_parser = OutputFixingParser.from_llm(llm=llm, parser=target_parser)

# ---------- prompt ----------
SYSTEM = """
You are Scittino’s culinary pairing assistant for a Maryland Italian deli/market/butcher & bakery.
Recommend food & drink pairings tailored to an EVENT and optional AUDIENCE/CONSTRAINTS.

STRICT SOURCE POLICY (in order of truth):
1) Use the curated Scittino’s presets via the `pairing_kb` tool (source tag: "Scittino’s KB").
2) If the preset is missing or incomplete, you may use web search **only** with domain restriction
   to Scittino’s owned sites (use `search` with 'site:' queries and cite the page):
   - scittinosdeli.com (house specialties, subs/sandwiches, small plates)
   - scittinositalianmarketplace.com (catering platters, antipasti, bakery/desserts)
   Add exact pages you referenced to `sources`.
3) If still needed, generate a Scittino’s-inspired custom plan limited to classic Italian deli/market/butcher items
   (e.g., fresh pasta, sauces, pesto, sausage links, meatballs, salumi, antipasti, cannoli, biscotti, espresso bar).
   Tag source as "Scittino’s-inspired custom plan". DO NOT invent exotic items outside an Italian deli/butcher scope.

Must-follow principles:
- Prefer Scittino’s staples: pizzas, stromboli, calzone, meatballs, chicken/eggplant parm, lasagna,
  pasta trays (marinara/vodka/pesto/bolognese), Italian cold cuts, antipasti, cannoli/biscotti,
  espresso/cappuccino, butcher packs (sausage, marinated chicken, meatballs), and DIY pasta kits.
- Include market/butchery options when relevant (build-your-own kits, raw proteins, sauces).
- Respect constraints (vegetarian/vegan/nut-free/halal/kosher/gluten-free, non-alcoholic, budget $, $$, $$$).
- Never suggest alcohol for minors; for kids/mixed audiences ALWAYS include non-alcoholic options.
- If user is vague, make reasonable assumptions and explain them in 'rationale'.
- Keep each list section concise and useful (3–6 items).

Output:
Return ONLY valid JSON per this schema:
{format_instructions}

Population rules:
- Always set 'tools_used' accurately (e.g., ["pairing_kb"], or ["pairing_kb","search"]).
- Always set 'sources'. If using KB only, include ["Scittino’s KB"]. If you search,
  include specific Scittino’s URLs or page titles (domain-restricted). If custom,
  include ["Scittino’s-inspired custom plan"].
"""

FEWSHOT = """
User: "Coffee & pastry break for the office."
Assistant (thinking): Use pairing_kb('coffee & pastry break'); include bakery items + espresso bar; no alcohol.
User: "We want a butcher grill pack for a tailgate."
Assistant (thinking): Use pairing_kb('butcher grill pack'); add NA drinks for mixed ages; note serving suggestions.
User: "I need a build-your-own pasta kit for 6, nut-free."
Assistant (thinking): Use pairing_kb('build-your-own pasta kit'); ensure nut-free sauce choices; include cappuccino optional.
"""

prompt = ChatPromptTemplate.from_messages(
    [
        ("system", SYSTEM),
        ("system", FEWSHOT),
        MessagesPlaceholder("chat_history"),
        ("human", "{query}"),
        MessagesPlaceholder("agent_scratchpad"),
    ]
).partial(format_instructions=target_parser.get_format_instructions())

# ---------- tools ----------
# Keep wiki_tool only if you want general food background; otherwise the source policy above will keep it unused.
tools = [pairing_kb_tool, search_tool, wiki_tool]

# ---------- agent ----------
agent = create_tool_calling_agent(llm=llm, prompt=prompt, tools=tools)
agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True)


# NEW: small helpers for professional-looking output
def _banner(title: str) -> str:
    title = title.strip()
    return f"\n🍝  {title.upper()} RECOMMENDATIONS  🍷\n" + ("=" * (len(title) + 25))

def _kv_summary(pairs):
    # pairs: list[tuple[str, str]]
    left_width = max((len(k) for k, _ in pairs), default=0)
    return "\n".join([f"{k:<{left_width}}  : {v}" for k, v in pairs if v])
def _normalize_text(s: str) -> str:
    """Replace smart quotes/dashes with ASCII so widths render predictably."""
    if not isinstance(s, str):
        return s
    s = unicodedata.normalize("NFKC", s)
    replacements = {
        "“": '"', "”": '"', "‘": "'", "’": "'",
        "–": "-", "—": "-", "−": "-",
        "…": "...",
    }
    for k, v in replacements.items():
        s = s.replace(k, v)
    return s

def _bulleted(items):
    """Turn a list into a neat multi-line bullet list."""
    items = [_normalize_text(x) for x in items]
    return "\n".join(f"• {x}" for x in items) if items else "—"

def _wrap_cell(text: str, width: int) -> str:
    text = _normalize_text(text or "")
    # Wrap each line independently so bullets stay aligned
    lines = []
    for ln in text.splitlines():
        lines.append(textwrap.fill(ln, width=width, replace_whitespace=False))
    return "\n".join(lines)


def _render_menu_and_drinks(menu, drinks):
    """
    Returns a string with two tables (Menu, Drinks), wrapped to terminal width.
    Uses 'tabulate' if available; otherwise neat plain text.
    """
    # Make each cell a multi-line bullet list instead of one long comma string
    menu_rows = [
        ["Appetizers", _bulleted(menu.appetizers)],
        ["Mains",       _bulleted(menu.mains)],
        ["Sides",       _bulleted(menu.sides)],
        ["Desserts",    _bulleted(menu.desserts)],
    ]
    drink_rows = [
        ["Alcoholic",     _bulleted(drinks.alcoholic)],
        ["Non-Alcoholic", _bulleted(drinks.non_alcoholic)],
    ]

    # Determine a safe width for the right column
    term_width = shutil.get_terminal_size((100, 20)).columns
    # Leave space for borders/left column; clamp for narrow terminals
    rec_col_width = max(24, min(80, term_width - 26))

    # Wrap the right-hand cells so they don’t explode the table
    for r in menu_rows:
        r[1] = _wrap_cell(r[1], rec_col_width)
    for r in drink_rows:
        r[1] = _wrap_cell(r[1], rec_col_width)

    if tabulate:
        # Prefer ASCII grid on very narrow terminals to avoid box-drawing glitches
        tablefmt = "github" if term_width < 90 else "fancy_grid"

        # Newer tabulate supports maxcolwidths; if your version is older, wrapping above already handles it.
        try:
            menu_txt = tabulate(menu_rows,
                                headers=["Course", "Recommendations"],
                                tablefmt=tablefmt,
                                maxcolwidths=[12, rec_col_width],
                                stralign="left",
                                disable_numparse=True)
            drink_txt = tabulate(drink_rows,
                                 headers=["Drinks", "Suggestions"],
                                 tablefmt=tablefmt,
                                 maxcolwidths=[12, rec_col_width],
                                 stralign="left",
                                 disable_numparse=True)
        except TypeError:
            # Fallback if tabulate doesn’t have maxcolwidths
            menu_txt = tabulate(menu_rows, headers=["Course", "Recommendations"],
                                tablefmt=tablefmt, stralign="left", disable_numparse=True)
            drink_txt = tabulate(drink_rows, headers=["Drinks", "Suggestions"],
                                 tablefmt=tablefmt, stralign="left", disable_numparse=True)
        return f"{menu_txt}\n\n{drink_txt}"

    # Plain-text fallback with wrapping
    def as_lines(rows, header_left, header_right):
        left_width = max(len(r[0]) for r in rows + [[header_left, header_right]])
        sep = "-" * (left_width + 3 + rec_col_width)
        lines = [f"{header_left:<{left_width}} | {header_right}", sep]
        for k, v in rows:
            # Pad wrapped right column line-by-line
            for i, ln in enumerate(v.splitlines() or ["—"]):
                if i == 0:
                    lines.append(f"{k:<{left_width}} | {ln}")
                else:
                    lines.append(f"{'':<{left_width}} | {ln}")
        return "\n".join(lines)

    menu_txt  = as_lines(menu_rows,  "Course", "Recommendations")
    drink_txt = as_lines(drink_rows, "Drinks", "Suggestions")
    return f"{menu_txt}\n\n{drink_txt}"


# ---------- simple in-memory chat loop ----------
def run_cli():
    print("🍽️ Pairings Assistant — type 'exit' to quit.")
    chat_history: List[Dict[str, Any]] = []

    while True:
        user_in = input("\nWhat event + any constraints? ")
        if user_in.strip().lower() in {"exit", "quit"}:
            print("Goodbye!")
            break

        raw = agent_executor.invoke({"query": user_in, "chat_history": chat_history})

        # Normalize Anthropic output to string for parsing
        model_text = fix_output(raw.get("output", ""))
        if not model_text:
            print("No output from model; raw:", raw)
            continue

        try:
            result = target_parser.parse(model_text)
        except Exception:
            try:
                result = fixing_parser.parse(model_text)
            except Exception as ex:
                print("Parsing failed. Raw model output:\n", model_text)
                print("Error:", ex)
                continue

        # NEW: Professional output
        print(_banner(result.event))

        meta_lines = []
        meta_lines.append(("Audience",     result.audience or "—"))
        meta_lines.append(("Cuisine",      result.cuisine_pref or "Italian"))
        meta_lines.append(("Constraints",  ", ".join(result.constraints) if result.constraints else "—"))
        print(_kv_summary(meta_lines))

        print()  # spacing
        print(_render_menu_and_drinks(result.menu, result.drinks))

        print("\nWHY THIS WORKS")
        print("-" * 16)
        print(result.rationale.strip())

        if result.sources:
            print("\nSOURCES")
            print("-" * 7)
            print("\n".join(f"• {s}" for s in result.sources))

        print("\nTOOLS")
        print("-" * 5)
        print(", ".join(result.tools_used) if result.tools_used else "—")

        # A short footer summary (tweak to taste)
        guests_hint = "Great for family-style sharing."
        scope_hint = "Grounded in Scittino’s menu & market."
        print(f"\n✅ {guests_hint}  •  {scope_hint}")


        # Optional save
        save = input("Save this to pairings_output.txt? [y/n] ").strip().lower()
        if save == "y":
            from tools import save_to_txt
            save_msg = save_to_txt(model_text)
            print(save_msg)

        # Chat history for context
        chat_history.append({"role": "user", "content": user_in})
        chat_history.append({"role": "assistant", "content": model_text})

def fix_output(output):
    """
    Accepts either a string, a list of {type:'text', text:'...'}, or nested dicts.
    Returns a single string for downstream JSON parsing.
    """
    if isinstance(output, str):
        return output

    # Anthropic-style list of segments
    if isinstance(output, list):
        texts = []
        for item in output:
            if isinstance(item, dict) and isinstance(item.get("text"), str):
                texts.append(item["text"])
        return "\n".join(texts).strip()

    # Sometimes you might get a dict with 'output' inside (defensive)
    if isinstance(output, dict) and "output" in output:
        return fix_output(output["output"])

    # Fallback: stringify
    return str(output)


if __name__ == "__main__":
    run_cli()
