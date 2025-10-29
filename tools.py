# tools.py
from langchain_community.tools import WikipediaQueryRun, DuckDuckGoSearchRun
from langchain_community.utilities import WikipediaAPIWrapper
from langchain.tools import Tool
from datetime import datetime
from kb import lookup_pairings

# ---------- domain tool ----------
def pairing_kb(event: str) -> str:
    """Looks up curated pairings for a given event from the local KB."""
    data = lookup_pairings(event)
    if not data:
        return "NO_MATCH"
    # Return a compact, deterministic JSON-ish string (LLM will parse)
    return {
        "event": event,
        "menu": data["food"],
        "drinks": data["drinks"],
        "tags": data.get("tags", [])
    }.__repr__()

pairing_kb_tool = Tool(
    name="pairing_kb",
    func=pairing_kb,
    description=(
        "Look up curated pairings for a specific event (e.g., 'football party', 'wedding dinner', "
        "'kids birthday'). Returns menu and drinks if found, else 'NO_MATCH'."
    ),
)

# ---------- save to file ----------
def save_to_txt(data: str, filename: str = "pairings_output.txt"):
    """Save nicely formatted pairing output instead of raw JSON."""
    import json, re
    from datetime import datetime

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    # Normalize to dict if possible
    parsed = None
    if isinstance(data, dict):
        parsed = data
    else:
        # Try direct JSON
        try:
            parsed = json.loads(data)
        except Exception:
            # Try to extract the first JSON object from mixed text
            m = re.search(r"\{.*\}", data, flags=re.S)
            if m:
                try:
                    parsed = json.loads(m.group(0))
                except Exception:
                    parsed = None

    formatted = []
    if parsed is not None:
        # Pretty, human-readable card
        formatted.append("🍝  SCITTINO’S PAIRING RECOMMENDATION  🍷")
        formatted.append(f"Generated on: {timestamp}\n")
        formatted.append(f"Event: {parsed.get('event','N/A').title()}")
        formatted.append("-" * 45 + "\n")

        menu = parsed.get("menu", {})
        drinks = parsed.get("drinks", {})

        def fmt_list(label, items):
            if items:
                formatted.append(f"{label}:")
                for i in items:
                    formatted.append(f"  • {i}")
                formatted.append("")

        fmt_list("Appetizers",       menu.get("appetizers", []))
        fmt_list("Mains",            menu.get("mains", []))
        fmt_list("Sides",            menu.get("sides", []))
        fmt_list("Desserts",         menu.get("desserts", []))
        fmt_list("Drinks (Alcoholic)",     drinks.get("alcoholic", []))
        fmt_list("Drinks (Non-Alcoholic)", drinks.get("non_alcoholic", []))

        rationale = (parsed.get("rationale") or "").strip()
        if rationale:
            formatted.append("Rationale:")
            formatted.append("  " + rationale + "\n")

        sources = parsed.get("sources", [])
        if sources:
            formatted.append("Sources:")
            for s in sources:
                formatted.append(f"  • {s}")
            formatted.append("")

        tools_used = parsed.get("tools_used", [])
        if tools_used:
            formatted.append("Tools Used:")
            formatted.append("  " + ", ".join(tools_used))

        formatted.append("\n" + "=" * 60 + "\n")
    else:
        # Fallback: save whatever text we got
        formatted = [
            "🍝  SCITTINO’S PAIRING RECOMMENDATION  🍷",
            f"Generated on: {timestamp}\n",
            str(data),
            "\n" + "=" * 60 + "\n",
        ]

    with open(filename, "a", encoding="utf-8") as f:
        f.write("\n".join(formatted))

    return f"✅ Pairing successfully saved to {filename}"



# ---------- web/wiki enrichment (optional) ----------
search = DuckDuckGoSearchRun()
search_tool = Tool(
    name="search",
    func=search.run,
    description="Search the web for menu or drink details if the KB is insufficient.",
)

api_wrapper = WikipediaAPIWrapper(top_k_results=1, doc_content_chars_max=600)
wiki_tool = WikipediaQueryRun(api_wrapper=api_wrapper)
