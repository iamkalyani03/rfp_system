# backend/app/ai.py
import json
from typing import List

# ---------------------------
# Dummy AI mode (offline)
# ---------------------------
# This file intentionally does NOT call OpenAI. It provides
# deterministic, local parsing and comparison so the app works
# without API keys or billing.

async def generate_rfp_structured(text: str):
    """
    Convert free text RFP -> structured JSON using simple heuristics.
    - Title: use first non-empty line (full)
    - Description: whole text
    - budget, timeline: find lines containing keywords
    - requirements: lines starting with '-' or bullet words
    - deliverables: simple inferred deliverables
    """
    title = first_nonempty_line(text)
    budget = extract_line(text, ["budget", "₹", "rs", "lakhs"])
    timeline = extract_line(text, ["timeline", "month", "week"])
    requirements = extract_list(text, ["- ", "• ", "backend", "frontend", "database", "cloud"])
    deliverables = infer_deliverables(requirements)

    structured = {
        "title": title,
        "description": text,
        "budget": budget,
        "timeline": timeline,
        "requirements": requirements,
        "deliverables": deliverables
    }
    return structured


async def parse_vendor_email(text: str):
    """
    Dummy parser: extract vendor name, pricing, timeline, technical_details, terms.
    Uses simple heuristics.
    """
    return {
        "vendor_name": guess_vendor_name(text),
        "pricing": extract_line(text, ["price", "cost", "budget", "₹", "rs"]),
        "timeline": extract_line(text, ["timeline", "month", "week"]),
        "technical_details": extract_line(text, ["tech", "stack", "api", "backend", "frontend"]),
        "terms": extract_line(text, ["term", "condition", "support", "warranty"])
    }


async def compare_proposals_ai(rfp: dict, proposals: List[dict]):
    """
    Dummy comparator:
      - If proposals include numeric pricing, picks the lowest-priced vendor
      - Otherwise picks first vendor
      - Returns summary, best_vendor and comparison array
    """
    if not proposals:
        return {
            "summary": "No proposals to compare.",
            "best_vendor": "",
            "comparison": []
        }

    best_idx = None
    best_price = float("inf")
    for i, p in enumerate(proposals):
        price = extract_price_number(p.get("pricing", "") or "")
        if price < best_price:
            best_price = price
            best_idx = i

    if best_idx is None:
        best_idx = 0

    best_vendor = proposals[best_idx].get("vendor_name", "") or proposals[best_idx].get("email", "")

    comparison = []
    for p in proposals:
        price = extract_price_number(p.get("pricing", "") or "")
        strengths = []
        weaknesses = []
        if price != float("inf"):
            strengths.append("Competitive pricing")
        else:
            weaknesses.append("No pricing provided")
        # small heuristic: if technical details present mark as strength
        if p.get("technical_details"):
            strengths.append("Technical details provided")
        comparison.append({
            "vendor_name": p.get("vendor_name", "") or p.get("email", ""),
            "strengths": strengths,
            "weaknesses": weaknesses
        })

    return {
        "summary": "Offline comparator: selected vendor based on lowest numeric pricing where available.",
        "best_vendor": best_vendor,
        "comparison": comparison
    }


# ---------------------------
# Helper functions
# ---------------------------

def first_nonempty_line(text: str):
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s
    return text[:60]

def extract_line(text: str, keywords):
    for line in text.splitlines():
        lower = line.lower()
        for k in keywords:
            if k in lower:
                return line.strip()
    return ""

def extract_list(text: str, keywords):
    out = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        # treat dash/• bullet as requirement
        if s.startswith("-") or s.startswith("•"):
            out.append(s.lstrip("-• ").strip())
            continue
        low = s.lower()
        if any(k in low for k in keywords):
            out.append(s)
    return out

def infer_deliverables(requirements):
    # Basic educated defaults
    base = ["Project Plan", "Source Code", "Deployment", "Documentation"]
    if requirements:
        return base
    return base

def guess_vendor_name(text: str):
    # Try to infer vendor name from "From:" or signature lines
    for line in text.splitlines():
        ln = line.strip()
        if ln.lower().startswith("from:"):
            return ln.split(":", 1)[1].strip()
    # fallback: first word
    parts = text.strip().split()
    return parts[0] if parts else "Vendor"

def extract_price_number(text: str):
    """
    Return an integer price if found, else infinity.
    Accepts formats like:
      - ₹400000
      - Rs 4,00,000
      - 350000
      - 3.5 lakh (NOT handled precisely; returns inf)
    """
    import re
    if not text:
        return float("inf")
    clean = text.replace(",", "")
    # find numbers
    m = re.findall(r"\d+", clean)
    if not m:
        return float("inf")
    try:
        return int(m[0])
    except:
        return float("inf")
