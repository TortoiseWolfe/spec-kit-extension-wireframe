---
description: "Capture standardized screenshots of wireframes (requires Python or Docker)"
---

# speckit.wireframe.screenshots

Capture standardized PNG screenshots of SVG wireframes for review. Takes 6 shots per SVG: one overview plus 5 quadrants at 2× resolution for detail inspection.

## User Input

```text
$ARGUMENTS
```

Accepts:
- `--all` — every wireframe across all features
- `--feature NNN` — one feature
- `--svg NNN:NN` — one specific SVG (e.g. `002:01` → `specs/002-*/wireframes/01-*.svg`)
- `--batch N` — process N features at a time
- No args — current feature

## Capability check

This command requires either:
- **Python 3.9+** with `playwright` and `cairosvg`, OR
- **Docker** with the screenshot container built

If neither is available, output a graceful degradation message and stop:

```
═══════════════════════════════════════════
SCREENSHOTS UNAVAILABLE
═══════════════════════════════════════════
This command requires Python 3.9+ with playwright installed,
or Docker for containerized capture.

To install Python dependencies:
  pip install playwright cairosvg && playwright install chromium

To build Docker image:
  docker build -t speckit-wireframe-screenshots \
    .specify/extensions/wireframe/scripts/

Alternative: /speckit.wireframe.review works without screenshots
(reviews the SVG source directly).
═══════════════════════════════════════════
```

## Workflow

### Step 1: Detect capability

```bash
# Prefer Python (faster, simpler)
if python3 -c "import playwright, cairosvg" 2>/dev/null; then
  MODE="python"
elif command -v docker >/dev/null 2>&1; then
  MODE="docker"
else
  # Graceful degradation message above
  exit 0
fi
```

### Step 2: Discover wireframes

```bash
# Based on --all, --feature, --svg
find specs/*/wireframes -name "*.svg" -not -path "*/includes/*"
```

### Step 3: Display plan

```
═══════════════════════════════════════════════════════════════
WIREFRAME SCREENSHOTS
═══════════════════════════════════════════════════════════════

Mode:     [--all | --feature NNN | --svg NNN:NN]
Capture:  [python playwright | docker]

Features to process:
  ☐ 001-user-auth        (2 SVGs)
  ☐ 002-dashboard        (3 SVGs)

Total: 2 features, 5 SVGs, 30 screenshots
Output: specs/*/wireframes/screenshots/

═══════════════════════════════════════════════════════════════
```

Wait for user confirmation before executing (the capture takes several seconds per SVG).

### Step 4: Execute

**Python mode:**
```bash
python3 .specify/extensions/wireframe/scripts/screenshots.py [args]
```

**Docker mode:**
```bash
docker run --rm -v "$PWD:/work" -w /work \
  speckit-wireframe-screenshots [args]
```

### Step 5: Report

```
═══════════════════════════════════════════════════════════════
RESULTS
═══════════════════════════════════════════════════════════════

Feature                 SVGs    Screenshots    Errors
──────────────────────  ──────  ─────────────  ──────
001-user-auth           2       12             0
002-dashboard           3       18             1

TOTAL                   5       30             1

Output:
  specs/001-user-auth/wireframes/screenshots/
  specs/002-dashboard/wireframes/screenshots/

Review:
  /speckit.wireframe.review [feature]
═══════════════════════════════════════════════════════════════
```

## Output structure

```
specs/<feature>/wireframes/screenshots/
├── <svg-name>/
│   ├── overview.png          # Full canvas
│   ├── quadrant-center.png   # Center region (2×)
│   ├── quadrant-tl.png       # Top-left corner (2×)
│   ├── quadrant-tr.png       # Top-right corner (2×)
│   ├── quadrant-bl.png       # Bottom-left corner (2×)
│   ├── quadrant-br.png       # Bottom-right corner (2×)
│   └── manifest.json         # Paths + metadata
└── summary.json              # Feature summary
```

## Integration with review

After screenshots are captured, `/speckit.wireframe.review` automatically reads them if present. The review command works without screenshots (analyzing SVG source directly) but is more thorough with them.

## Post-implement regression check

When invoked via the `after_implement` hook, this command:

1. Captures screenshots of the **built UI** (not just the SVG wireframe)
2. Compares them side-by-side with signed-off wireframes from `spec.md`'s `## UI Mockup` block
3. Reports drift: what the implementation does vs what was approved

This is the "visual regression" end of the feedback loop.

---

## DO NOT

- Require Python or Docker for the command to be *defined* — gracefully degrade when missing
- Overwrite SVG source files — this command only reads SVGs and writes PNGs
- Write to `.terminal-status.json` or any queue file
- Skip the capability check — failing confusingly is worse than skipping with a clear message
