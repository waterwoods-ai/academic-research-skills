#!/usr/bin/env python3
"""Fetch upcoming submission deadlines for the 22 tracked security/crypto
conferences from sec-deadlines.github.io and render deadlines_current.md.

Run at every upstream sync (wired into the `git sync-upstream` alias).
Source of truth: https://sec-deadlines.github.io (community-maintained YAML).
Static venue knowledge lives in big4_venue_profiles.md; dates live here only.
"""

import ssl
import urllib.error
import urllib.request
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

try:
    import certifi

    SSL_CONTEXT = ssl.create_default_context(cafile=certifi.where())
except ImportError:  # fall back to system trust store
    SSL_CONTEXT = ssl.create_default_context()

SOURCE_URL = (
    "https://raw.githubusercontent.com/sec-deadlines/"
    "sec-deadlines.github.io/master/_data/conferences.yml"
)
OUTPUT_PATH = Path(__file__).parent / "deadlines_current.md"
FETCH_TIMEOUT_SECONDS = 30

# yaml name (exact match in sec-deadlines data) -> (ranking name, CIF rank 2025)
TRACKED = {
    "S&P (Oakland)": ("IEEE S&P", 1),
    "Eurocrypt": ("Eurocrypt", 2),
    "NDSS": ("NDSS", 3),
    "CCS": ("ACM CCS", 4),
    "Crypto": ("Crypto", 5),
    "USENIX Security": ("USENIX Security", 6),
    "CHES": ("CHES", 7),
    "FC": ("FC", 8),
    "Euro S&P": ("IEEE EuroS&P", 9),
    "ACNS": ("ACNS", 10),
    "ACSAC": ("ACSAC", 11),
    "ASIA CCS": ("ACM AsiaCCS", 12),
    "PETS": ("PETS", 13),
    "Asiacrypt": ("Asiacrypt", 14),
    "PKC": ("PKC", 15),
    "ESORICS": ("ESORICS", 16),
    "FSE": ("FSE", 17),
    "WiSec": ("ACM WiSec", 18),
    "RAID": ("RAID", 19),
    "CT-RSA": ("CT-RSA", 20),
    "CSF": ("IEEE CSF", 21),
    "TCC": ("TCC", 22),
}

BIG4_RANKS = {1, 3, 4, 6}


def fetch_source() -> str:
    """Download the sec-deadlines YAML; fail loudly on network errors."""
    try:
        with urllib.request.urlopen(
            SOURCE_URL, timeout=FETCH_TIMEOUT_SECONDS, context=SSL_CONTEXT
        ) as resp:
            return resp.read().decode("utf-8")
    except (urllib.error.URLError, TimeoutError) as error:
        raise SystemExit(
            f"Could not fetch {SOURCE_URL}: {error}\n"
            "Deadline calendar NOT updated — retry when online."
        ) from error


def parse_deadline(raw: str) -> datetime | None:
    """Parse one deadline string; return None for TBA/unparseable values."""
    text = str(raw).strip().strip("'\"")
    for fmt in ("%Y-%m-%d %H:%M", "%Y-%m-%d %H:%M:%S", "%Y-%m-%d"):
        try:
            return datetime.strptime(text, fmt).replace(tzinfo=timezone.utc)
        except ValueError:
            continue
    return None


def aoe_now() -> datetime:
    """Current time on the Anywhere-on-Earth clock (UTC-12), as UTC-naive-equivalent."""
    return datetime.now(timezone.utc) - timedelta(hours=12)


def collect_rows(entries: list[dict]) -> list[dict]:
    """Filter tracked conferences and compute their upcoming deadlines."""
    now = aoe_now()
    rows = []
    for entry in entries:
        tracked = TRACKED.get(str(entry.get("name", "")))
        if tracked is None:
            continue
        ranking_name, rank = tracked
        deadlines = entry.get("deadline") or []
        if not isinstance(deadlines, list):
            deadlines = [deadlines]
        parsed = [d for d in (parse_deadline(x) for x in deadlines) if d]
        upcoming = sorted(d for d in parsed if d >= now)
        rows.append(
            {
                "rank": rank,
                "name": ranking_name,
                "year": entry.get("year", ""),
                "upcoming": upcoming,
                "all_tba": not parsed,
                "date": entry.get("date", "TBA"),
                "place": entry.get("place", ""),
                "link": entry.get("link", ""),
                "comment": entry.get("comment", ""),
            }
        )
    return rows


def next_deadline_key(row: dict) -> tuple:
    """Sort key: rows with an upcoming deadline first (soonest first), then by rank."""
    if row["upcoming"]:
        return (0, row["upcoming"][0], row["rank"])
    return (1, datetime.max.replace(tzinfo=timezone.utc), row["rank"])


def render_markdown(rows: list[dict]) -> str:
    """Render the deadline table, soonest deadline first."""
    fetched = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    header = [
        "# Upcoming Deadlines — 22 Tracked Conferences",
        "",
        f"> GENERATED FILE — do not edit. Refreshed by `fetch_deadlines.py` "
        f"at every `git sync-upstream`. Fetched {fetched}.",
        f"> Source: {SOURCE_URL.replace('raw.githubusercontent.com/', 'github.com/').replace('/master/', '/blob/master/')}",
        "> All deadlines are AoE (UTC-12) unless the venue states otherwise.",
        "",
        "| Next deadline | Conference | CIF rank | Edition | Event date / place | Notes |",
        "|---|---|---|---|---|---|",
    ]
    lines = []
    for row in sorted(rows, key=next_deadline_key):
        if row["upcoming"]:
            first = row["upcoming"][0].strftime("%Y-%m-%d")
            extra = len(row["upcoming"]) - 1
            when = f"**{first}**" + (f" (+{extra} later)" if extra else "")
        else:
            when = "TBA" if row["all_tba"] else "passed"
        big4 = " ★" if row["rank"] in BIG4_RANKS else ""
        name = f"[{row['name']}]({row['link']})" if row["link"] else row["name"]
        lines.append(
            f"| {when} | {name}{big4} | #{row['rank']} | {row['year']} "
            f"| {row['date']}, {row['place']} | {row['comment']} |"
        )
    footer = ["", "★ = Big 4. Rank = CIF 2025 (`conference_ranking_2025.json`)."]
    return "\n".join(header + lines + footer) + "\n"


def main() -> None:
    entries = yaml.safe_load(fetch_source())
    if not isinstance(entries, list):
        raise SystemExit("Unexpected data shape from sec-deadlines (expected a list).")
    rows = collect_rows(entries)
    found = {row["name"] for row in rows}
    missing = {name for name, _ in TRACKED.values()} - found
    OUTPUT_PATH.write_text(render_markdown(rows), encoding="utf-8")
    print(f"Wrote {OUTPUT_PATH.name}: {len(rows)} entries for {len(found)}/22 conferences.")
    if missing:
        print(f"WARNING — not found in source (name drift?): {', '.join(sorted(missing))}")


if __name__ == "__main__":
    main()
