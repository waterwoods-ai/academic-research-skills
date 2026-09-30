#!/usr/bin/env python3
"""Stage 0 Automator: Initialize an academic security research paper project.

Automates Stage 0 (Environment Preparation & Project Initialization) per HOWTO.md:
1. Checks and repairs the personal skill links opencode reads (HOWTO Step 0.1).
2. Creates the paper project directory.
3. Generates dual anchor files (CLAUDE.md for Claude Code, AGENTS.md for Codex/opencode).
4. Runs the Stage 0 smoke test (validating against major_revision_playbook.md).
5. Displays the next-step prompts for Stage A (Topic Scouting).

Usage:
    python3 init_project.py --name paper-cps-spoofing --venue "NDSS 2027"
    python3 init_project.py --help
"""

import argparse
import os
import re
import sys
from pathlib import Path

# Venues recognized in the Big-4 / tier-2 profiles
CANONICAL_BIG4 = ["IEEE S&P", "USENIX Security", "ACM CCS", "NDSS"]

DEFAULT_TRACK = "CPS / IoT / AI Security"
DEFAULT_PAPER_FILE = "./paper.tex"
# No dated default: a venue cycle goes stale, and dates come only from deadlines_current.md.
DEFAULT_VENUE = "TBD (pick from deadlines_current.md)"
DEFAULT_DEST = (
    Path.home() / "Documents" / "research"
    if (Path.home() / "Documents" / "research").exists()
    else (Path.home() / "Document" / "research" if (Path.home() / "Document" / "research").exists() else Path.home() / "Documents" / "research")
)


def parse_arguments() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize a new academic security paper project (Stage 0 Automator)."
    )
    parser.add_argument(
        "--name",
        "-n",
        type=str,
        required=True,
        help="Project directory name (e.g., paper-iot-auth, cps-sensor-spoofing).",
    )
    parser.add_argument(
        "--venue",
        "-v",
        type=str,
        default=DEFAULT_VENUE,
        help="Target venue and year, e.g. 'NDSS 2027'. Left as TBD if omitted; never guessed.",
    )
    parser.add_argument(
        "--track",
        "-t",
        type=str,
        default=DEFAULT_TRACK,
        help=f"Research track/subfield (default: '{DEFAULT_TRACK}').",
    )
    parser.add_argument(
        "--dest",
        "-d",
        type=Path,
        default=DEFAULT_DEST,
        help=f"Destination directory where project folder will be created (default: '{DEFAULT_DEST}').",
    )
    parser.add_argument(
        "--paper-file",
        type=str,
        default=DEFAULT_PAPER_FILE,
        help=f"Relative path to main paper manuscript (default: '{DEFAULT_PAPER_FILE}').",
    )
    parser.add_argument(
        "--skip-symlinks",
        action="store_true",
        help="Skip checking/repairing the personal skill links.",
    )
    parser.add_argument(
        "--skip-smoke-test",
        action="store_true",
        help="Skip the automated NDSS Major Revision smoke test.",
    )
    return parser.parse_args()


def get_repo_roots() -> tuple[Path, Path]:
    """Resolve the academic-research-skills and security-track root paths."""
    script_path = Path(__file__).resolve()
    # script is in security-track/scripts/ or skills/security-track/scripts/
    if (script_path.parent.parent / "templates").is_dir():
        security_track_dir = script_path.parent.parent
    else:
        # Fallback search
        candidate = script_path.parents[1]
        security_track_dir = candidate if (candidate / "templates").is_dir() else script_path.parent

    # ARS root
    if (security_track_dir / "academic-paper").is_dir():
        ars_root = security_track_dir
    elif (security_track_dir.parent / "academic-paper").is_dir():
        ars_root = security_track_dir.parent
    elif (security_track_dir.parents[1] / "academic-paper").is_dir():
        ars_root = security_track_dir.parents[1]
    else:
        ars_root = security_track_dir.parent

    return ars_root, security_track_dir


def check_and_repair_symlinks(ars_root: Path) -> list[str]:
    """Verify and link the required skills into the personal skills folder."""
    skills_dir = Path.home() / ".claude" / "skills"
    skills_dir.mkdir(parents=True, exist_ok=True)

    repaired = []
    # The six skills opencode reads (HOWTO Step 0.1). The three browser skills
    # (find-research-topic, verify-research-topic, novelty-filter) ship in the
    # Claude Code plugin and are deliberately NOT linked: a personal link would
    # load a second copy next to the plugin's.
    ars_skills = [
        "academic-paper",
        "academic-paper-reviewer",
        "academic-pipeline",
        "deep-research",
        "security-track",
        "novelty-engine",
    ]
    for skill_name in ars_skills:
        target = ars_root / skill_name
        if not target.exists():
            target = ars_root / "skills" / skill_name
        if target.exists():
            link = skills_dir / skill_name
            if not link.exists() or (link.is_symlink() and not os.path.exists(link)):
                if link.is_symlink() or link.exists():
                    link.unlink()
                link.symlink_to(target.resolve())
                repaired.append(f"{skill_name} -> {target.resolve()}")

    return repaired


def run_smoke_test(security_track_dir: Path) -> tuple[bool, str]:
    """Verify that major_revision_playbook.md contains authoritative Big-4 review facts."""
    playbook_path = security_track_dir / "references" / "major_revision_playbook.md"
    if not playbook_path.is_file():
        return False, f"Playbook file not found at {playbook_path}"

    content = playbook_path.read_text(encoding="utf-8")

    # Authoritative facts per Step 0.3 of HOWTO.md:
    # 1. NDSS is the ONLY Big-4 venue with a true Major Revision
    # 2. S&P retired revision in 2024 (Accept/Reject only)
    # 3. USENIX Security eliminated Major Revision in 2026
    # 4. ACM CCS has Minor Revision only
    checks = [
        ("NDSS is the ONLY", "NDSS sole Major Revision retention"),
        ("IEEE S&P", "IEEE S&P rules specified"),
        ("USENIX Security", "USENIX Security rules specified"),
        ("ACM CCS", "ACM CCS rules specified"),
        ("Major Revision", "Major Revision terminology active"),
    ]

    missing = [desc for pattern, desc in checks if pattern.lower() not in content.lower()]
    if missing:
        return False, f"Missing critical review facts in playbook: {', '.join(missing)}"

    return True, (
        "Playbook check PASSED: major_revision_playbook.md is present and covers all four "
        "Big-4 venues' decision rules.\n"
        "      This checks the file only. To confirm each tool loads the skill, ask it the "
        "HOWTO Step 0.3 question."
    )


def generate_anchor_content(template_content: str, name: str, venue: str, track: str, paper_file: str) -> str:
    """Fill project anchor template with project-specific metadata."""
    # Replace title
    content = re.sub(
        r"#\s+<Project Name>\s+—\s+Security Research\s+\(anchor file\)",
        f"# {name} — Security Research ({track})",
        template_content,
    )
    # Replace venue
    content = re.sub(
        r"- Target venue:\s+<[^>]+>",
        f"- Target venue: {venue}",
        content,
    )
    # Replace stage
    content = re.sub(
        r"- Research-loop stage:\s+<[^>]+>",
        "- Research-loop stage: S0 topic viability",
        content,
    )
    # Replace paper file
    content = re.sub(
        r"- Paper file:\s+<[^>]+>",
        f"- Paper file: {paper_file}",
        content,
    )
    return content


def main() -> int:
    args = parse_arguments()
    print("=" * 68)
    print("  Academic Security Research Project Initializer (Stage 0 Automator)")
    print("=" * 68)

    ars_root, sec_track = get_repo_roots()

    # 1. Symlink verification
    if not args.skip_symlinks:
        print(f"\n[*] Step 0.1: Checking skill links in {Path.home() / '.claude' / 'skills'}...")
        if not (ars_root / "academic-paper").is_dir():
            print("    [--] Skipped: the links apply to the Claude fork checkout only.")
        else:
            repaired = check_and_repair_symlinks(ars_root)
            if repaired:
                for item in repaired:
                    print(f"    [+] Linked: {item}")
            else:
                print("    [OK] All six skills are linked.")

    # 2. Directory Creation
    project_dir = (args.dest / args.name).resolve()
    print(f"\n[*] Step 0.2: Setting up project workspace: {project_dir}")
    project_dir.mkdir(parents=True, exist_ok=True)
    print(f"    [OK] Directory ready: {project_dir}")

    # 3. Anchor Files
    templates_dir = sec_track / "templates"
    claude_tpl = templates_dir / "project-anchor-CLAUDE.md"
    agents_tpl = templates_dir / "project-anchor-AGENTS.md"

    if not claude_tpl.is_file() or not agents_tpl.is_file():
        print(f"    [!] Error: Template files missing in {templates_dir}", file=sys.stderr)
        return 1

    claude_content = generate_anchor_content(
        claude_tpl.read_text(encoding="utf-8"),
        name=args.name,
        venue=args.venue,
        track=args.track,
        paper_file=args.paper_file,
    )
    agents_content = generate_anchor_content(
        agents_tpl.read_text(encoding="utf-8"),
        name=args.name,
        venue=args.venue,
        track=args.track,
        paper_file=args.paper_file,
    )

    claude_dest = project_dir / "CLAUDE.md"
    agents_dest = project_dir / "AGENTS.md"

    for dest, content, reader in (
        (claude_dest, claude_content, "Claude Code"),
        (agents_dest, agents_content, "Codex and opencode"),
    ):
        if dest.exists():
            print(f"    [--] Kept existing {dest.name} (not overwritten)")
        else:
            dest.write_text(content, encoding="utf-8")
            print(f"    [OK] Generated {dest.name} (read by {reader})")

    # 4. Smoke Test
    if not args.skip_smoke_test:
        print("\n[*] Step 0.3: Checking the Big-4 decision-rules playbook...")
        passed, msg = run_smoke_test(sec_track)
        if passed:
            print(f"    [OK] {msg}")
        else:
            print(f"    [FAIL] {msg}", file=sys.stderr)
            return 2

    # 5. Success Summary & Next Step Prompts
    print("\n" + "=" * 68)
    print("  STAGE 0 COMPLETE: Environment & Anchor Files Ready")
    print("=" * 68)
    print(f"Project Path : {project_dir}")
    print(f"Target Venue : {args.venue}")
    print(f"Track/Focus  : {args.track}")
    print(f"Current Stage: S0 (Topic Viability)")
    print("\nNext step -> enter the project directory and start Phase A (HOWTO):")
    print(f"  cd {project_dir}")
    print("\nPick the entry that matches what you have:")
    print("  - Only a broad area   -> Claude Code:  find-research-topic <broad area>")
    print("  - A specific area     -> HOWTO Step 1: ars-lit-review <your area>, ensure broad coverage.")
    print("  - Your own method     -> HOWTO Step 5b (the Evaluate line)")
    print("  - Led step by step    -> Be my security research mentor")
    print("=" * 68)

    return 0


if __name__ == "__main__":
    sys.exit(main())
