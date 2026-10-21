#!/usr/bin/env python3
"""Checks events.json with the same rules the Card Circuit / Pocket Vendor app applies
(scripts/show_store.gd _validate_feed / _validate_event). Run before every push:
    python3 tools/validate.py events.json
Exit code 0 = the app will accept the file; otherwise the first problem is printed."""
import json, re, sys
from datetime import date

EVENT_STATUSES = {"Scheduled", "Postponed", "Cancelled"}
TABLE_STATUSES = {"Unknown", "Open", "Waitlist", "Sold out"}
POPULARITY = {"Unknown", "Low", "Medium", "High"}
TEXT = ["id", "title", "organizer", "city", "province", "address", "venue", "start_date", "end_date", "start_time", "end_time",
        "timezone", "application_deadline", "vendor_url", "source_url", "verified_at", "last_checked", "description", "parking",
        "setup_time", "event_status", "table_status", "popularity", "popularity_note", "popularity_source_url",
        "table_booking_open_date", "table_booking_source_url"]

def valid_date(v):
    if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", v or ""): return False
    try: date.fromisoformat(v); return True
    except ValueError: return False

def check_event(e):
    if not isinstance(e, dict): return "every event must be an object"
    for f in TEXT:
        if f in e and not isinstance(e[f], str): return f"field '{f}' must be text"
    g = lambda f: (e.get(f) or "").strip()
    if not g("id") or len(g("id")) > 120 or not re.fullmatch(r"[A-Za-z0-9_-]+", g("id")): return "id must be 1-120 letters, digits, _ or -"
    if not g("title") or len(g("title")) > 200: return "title required (max 200)"
    if not g("city"): return "city required"
    if not g("venue"): return "venue required (use 'Venue TBA' and venue_pending=true if unknown)"
    if not valid_date(g("start_date")): return "start_date must be YYYY-MM-DD"
    end = g("end_date") or g("start_date")
    if not valid_date(end) or end < g("start_date"): return "end_date must be valid and on/after start_date"
    for f in ["start_time", "end_time", "setup_time"]:
        if g(f) and not re.fullmatch(r"([01]\d|2[0-3]):[0-5]\d", g(f)): return f"{f} must be HH:MM (24 h) or blank"
    if g("application_deadline") and not valid_date(g("application_deadline")): return "application_deadline must be YYYY-MM-DD"
    if g("table_booking_open_date"):
        if not valid_date(g("table_booking_open_date")) or g("table_booking_open_date") > end: return "table_booking_open_date invalid or after the show"
    pop = g("popularity") or "Unknown"
    if pop not in POPULARITY: return "popularity must be Unknown/Low/Medium/High"
    if pop != "Unknown" and not g("popularity_note"): return "popularity needs popularity_note"
    for f in ["source_url", "vendor_url", "popularity_source_url", "table_booking_source_url"]:
        if g(f) and not re.fullmatch(r"https?://\S+", g(f)): return f"{f} must start with https:// and have no spaces"
    for f in ["admission_cents", "table_fee_cents"]:
        v = e.get(f, -1)
        if not isinstance(v, int) or isinstance(v, bool) or v < -1: return f"{f} must be whole cents or -1"
    if not isinstance(e.get("categories", []), list) or not all(isinstance(c, str) for c in e.get("categories", [])): return "categories must be a list of text"
    if (g("event_status") or "Scheduled") not in EVENT_STATUSES: return "event_status must be Scheduled/Postponed/Cancelled"
    if (g("table_status") or "Unknown") not in TABLE_STATUSES: return "table_status must be Unknown/Open/Waitlist/Sold out"
    for f in ["archived", "is_demo", "venue_pending"]:
        if f in e and not isinstance(e[f], bool): return f"{f} must be true/false"
    for f in ["verified_at", "last_checked"]:
        if g(f) and not valid_date(g(f)[:10]): return f"{f} must start with YYYY-MM-DD"
    return None

def main(path):
    data = json.load(open(path, encoding="utf-8"))
    if not isinstance(data, dict) or data.get("schema_version") != 1: return "top level must be an object with schema_version 1"
    rows = data.get("events")
    if not isinstance(rows, list) or len(rows) > 10000: return "events must be a list (max 10,000)"
    seen = set()
    for i, e in enumerate(rows, 1):
        problem = check_event(e)
        if problem: return f"event {i} ({e.get('id', '?') if isinstance(e, dict) else '?'}): {problem}"
        if e["id"] in seen: return f"duplicate id {e['id']}"
        seen.add(e["id"])
    print(f"OK: {len(rows)} shows, checked_at {data.get('checked_at', '?')}")
    return None

if __name__ == "__main__":
    error = main(sys.argv[1] if len(sys.argv) > 1 else "events.json")
    if error: print("INVALID:", error); sys.exit(1)
