import json
import os
from langchain_core.tools import tool

@tool
def kpi_calculator(internal_transfers: int, total_headcount: int) -> str:
    """
    Calculate the Talent Mobility Rate for HR reporting.
    Use this when the user asks about mobility metrics across Gucci brands.
    """
    if total_headcount <= 0:
        return "Error: Total headcount must be greater than zero."
    
    mobility_rate = (internal_transfers / total_headcount) * 100
    
    return (f"Talent Mobility Rate: {mobility_rate:.2f}%\n"
            f"Calculation: ({internal_transfers} transfers / {total_headcount} employees) * 100")

@tool
def hr_ab_simulator(strategy_a: str, strategy_b: str) -> str:
    """
    Simulate outcomes for two different HR rollout strategies (e.g., Centralized vs Decentralized).
    """
    results = {
        "Centralized": {"engagement": "45%", "retention": "Low", "risk": "High Brand DNA dilution"},
        "Decentralized": {"engagement": "88%", "retention": "High", "risk": "Complexity in coordination"}
    }
    
    res_a = results.get(strategy_a, {"engagement": "N/A", "retention": "N/A", "risk": "Unknown"})
    res_b = results.get(strategy_b, {"engagement": "N/A", "retention": "N/A", "risk": "Unknown"})
    
    return (f"A/B Test Results:\n"
            f"- Strategy A ({strategy_a}): Engagement {res_a['engagement']}, Risk: {res_a['risk']}\n"
            f"- Strategy B ({strategy_b}): Engagement {res_b['engagement']}, Risk: {res_b['risk']}")

@tool
def get_safety_disclaimer() -> str:
    """
    Fetch the mandatory safety disclaimers required for all AI suggestions.
    Ensures compliance with responsible AI guidelines.
    """
    return "DISCLAIMER: AI suggestions are drafts; learners must confirm sources; no wagering language; use neutral phrasing."

@tool
def export_portfolio_pack(plan: str, posts: str, summary: str) -> str:
    """
    One-click export of the plan, social posts, and executive update into a file.
    Creates a tangible outcome for the user's portfolio[cite: 41].
    """
    os.makedirs("exports", exist_ok=True)
    file_path = "exports/gucci_portfolio_pack.txt"
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write("=== GUCCI LEADERSHIP DEVELOPMENT PORTFOLIO ===\n\n")
        f.write(f"--- STRATEGIC PLAN ---\n{plan}\n\n")
        f.write(f"--- INTERNAL POSTS ---\n{posts}\n\n")
        f.write(f"--- EXECUTIVE SUMMARY ---\n{summary}\n")
    
    return f"Success! Portfolio pack exported to {file_path}. Ready for employer review."

