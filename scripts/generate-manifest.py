#!/usr/bin/env python3
"""
Generate wireframes-manifest.json for the viewer.

Scans specs/*/wireframes/*.svg and emits a JSON manifest the viewer can fetch.
Also reads any *.issues.md files to surface review status in the manifest.

Usage:
  python3 scripts/generate-manifest.py [--output PATH] [--specs-dir PATH]

Writes to .specify/extensions/wireframe/viewer/wireframes-manifest.json by default.
"""
import argparse
import json
import re
import sys
from pathlib import Path


def extract_title(svg_path: Path) -> str:
    """Read the first <title>-like text from the SVG, fall back to filename."""
    try:
        content = svg_path.read_text(errors="ignore")
        # Look for the centered title text element (v5 convention: y="28")
        m = re.search(r'<text[^>]*y=["\']28["\'][^>]*>([^<]+)</text>', content)
        if m:
            return m.group(1).strip()
    except Exception:
        pass
    # Fall back to filename: "01-sign-in.svg" → "Sign In"
    stem = svg_path.stem
    parts = stem.split("-", 1)
    title = parts[1] if len(parts) > 1 and parts[0].isdigit() else stem
    return title.replace("-", " ").title()


def detect_status(svg_path: Path) -> str:
    """Derive review status from sibling .issues.md file."""
    issues = svg_path.with_suffix(".issues.md")
    if not issues.exists():
        return "draft"
    try:
        content = issues.read_text()
    except Exception:
        return "draft"
    # Extract Status: line
    m = re.search(r'^\*\*Status:\*\*\s*(\w+)', content, re.MULTILINE)
    if not m:
        return "draft"
    status = m.group(1).upper()
    return {"PASS": "approved", "PATCH": "review", "REGENERATE": "review", "REGEN": "review"}.get(status, "draft")


def detect_theme(svg_path: Path) -> str:
    """Guess theme by peeking at the background fill."""
    try:
        content = svg_path.read_text(errors="ignore")[:1000]
    except Exception:
        return "unknown"
    if "bg-dark" in content or "#0f172a" in content or "#1a1a2e" in content:
        return "dark"
    if "#c7ddf5" in content or "#e8d4b8" in content:
        return "light"
    return "unknown"


def feature_label(feature_dir: str) -> str:
    """Turn '001-user-login' into '001 - User Login'."""
    m = re.match(r'^(\d+)-(.+)$', feature_dir)
    if not m:
        return feature_dir
    num, slug = m.groups()
    return f"{num} - {slug.replace('-', ' ').title()}"


def build_manifest(specs_dir: Path) -> dict:
    features = []
    if not specs_dir.exists():
        return {"schema_version": "1.0", "features": [], "wireframes": [], "total": 0}

    for feature_dir in sorted(specs_dir.iterdir()):
        if not feature_dir.is_dir():
            continue
        wireframes_dir = feature_dir / "wireframes"
        if not wireframes_dir.is_dir():
            continue
        svgs = sorted(wireframes_dir.glob("*.svg"))
        if not svgs:
            continue

        feature_entries = []
        for svg in svgs:
            rel_path = f"{feature_dir.name}/wireframes/{svg.name}"
            feature_entries.append({
                "path": rel_path,
                "title": extract_title(svg),
                "status": detect_status(svg),
                "theme": detect_theme(svg),
                "svg_file": svg.name,
            })
        features.append({
            "id": feature_dir.name,
            "label": feature_label(feature_dir.name),
            "wireframes": feature_entries,
        })

    # Flat list is easier for the viewer's navigation state machine.
    # Paths are absolute from the server root (project root). The view command
    # serves from the project root so both viewer.html and specs/ are reachable
    # under one origin without needing `..` traversal (which http.server blocks).
    flat = [
        {
            "path": f"/specs/{wf['path']}",
            "title": wf["title"],
            "feature": f["id"],
            "feature_label": f["label"],
            "status": wf["status"],
            "theme": wf["theme"],
        }
        for f in features
        for wf in f["wireframes"]
    ]

    return {
        "schema_version": "1.0",
        "features": features,
        "wireframes": flat,
        "total": len(flat),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--specs-dir",
        default="specs",
        help="Root directory containing feature folders (default: specs)",
    )
    parser.add_argument(
        "--output",
        default=".specify/extensions/wireframe/viewer/wireframes-manifest.json",
        help="Path to write the manifest JSON",
    )
    args = parser.parse_args()

    specs_dir = Path(args.specs_dir)
    manifest = build_manifest(specs_dir)

    output = Path(args.output)
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(manifest, indent=2) + "\n")

    print(f"Wrote manifest: {output}")
    print(f"  Features: {len(manifest['features'])}")
    print(f"  Wireframes: {manifest['total']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
