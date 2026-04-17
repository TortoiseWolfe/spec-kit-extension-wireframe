---
description: "Cross-SVG consistency check for features with multiple wireframes"
---

# speckit.wireframe.inspect

**Purpose:** Check consistency across multiple wireframes in the same feature, or across the whole project. Runs after `/speckit.wireframe.review` passes — catches cross-SVG drift that per-SVG review can't see.

## User Input

```text
$ARGUMENTS
```

Accepts:
- Feature identifier (e.g. `001`) — inspect all wireframes for one feature
- `--all` — inspect every wireframe across all features
- No args — inspect current feature

## What cross-SVG inspection catches

Per-SVG review catches issues within one wireframe. Inspection catches drift **between** wireframes:

| Pattern | Expected | Drift example |
|---------|----------|---------------|
| Title position | All SVGs: x=960, y=28 | One SVG has y=35 |
| Signature | All SVGs same format | One uses different separator |
| Header include | All use `includes/header-desktop.svg` | One embeds header inline |
| Mockup bounds | All: desktop x=40, mobile x=1360 | One has desktop at x=50 |
| Color palette | Light theme: `#e8d4b8` panels | One uses `#e8d5b9` (close but different) |
| Callout style | Red circle, 14px text, white fill | One uses blue circle |
| Badge style | Height=22, rx=4 | One uses height=24 |

## Workflow

### Step 1: Discover SVGs

**If feature ID:**
```bash
find specs/<feature>/wireframes -name "*.svg" -not -path "*/includes/*"
```

**If `--all`:**
```bash
find specs/*/wireframes -name "*.svg" -not -path "*/includes/*"
```

### Step 2: Extract patterns

For each SVG, extract measurable patterns (use Python script if available, otherwise do via SVG text scan):

```bash
python3 .specify/extensions/wireframe/scripts/inspect.py --report specs/<feature>/wireframes/
```

If the script is not installed, read each SVG and extract:
- Title `<text>` element: x, y, font-size, fill
- Signature `<text>` element: x, y, font-size
- Desktop mockup `<rect>` or `<g>`: x, y, width, height
- Mobile mockup: same
- Annotation panel: x, y
- `<use>` references (headers, footers)
- Unique colors used (extract `fill="#...."` values)

### Step 3: Compute majority patterns

For each measurable attribute, find the **majority value** across all SVGs. Flag any SVG that deviates from the majority.

Example:
- Title y position:
  - 8 SVGs have y=28 (majority)
  - 1 SVG has y=35 → **DEVIATION: SVG-005**
  - 1 SVG has y=30 → **DEVIATION: SVG-009**

### Step 4: Apply pattern checks

Also verify each SVG against hard expectations (independent of majority):

| Check | Expected |
|-------|----------|
| Title position | x=960, y=28 (centered, 1920/2) |
| Signature position | y=1060 |
| Desktop mockup (light) | x=40, y=60, 1280×720 |
| Mobile mockup (light) | x=1360, y=60, 360×720 |
| Annotation panel | x=40 (or full-width container), y=800 |
| Canvas | `viewBox="0 0 1920 1080"` |

### Step 5: Log pattern violations

Append to each affected SVG's `.issues.md`:

```markdown
## Inspector Issues (YYYY-MM-DD)

| Check | Expected | Actual | Classification |
|-------|----------|--------|----------------|
| title_y_position | y=28 (majority, 8/10 SVGs) | y=35 | PATTERN_VIOLATION |
| panel_color_light | #e8d4b8 (majority) | #e8d5b9 | PATTERN_VIOLATION |
```

### Step 6: Report

```
═══════════════════════════════════════════
INSPECTION COMPLETE
═══════════════════════════════════════════
Scope: [feature NNN | all features]
Total SVGs inspected: [N]

PASS: [count] SVGs follow consistent patterns
FAIL: [count] SVGs have pattern violations

Top violations:
  1. title_y_position: 2 SVGs deviate (001/03, 002/01)
  2. panel_color_light: 1 SVG uses near-match color (005/02)

Violations logged to:
  specs/*/wireframes/*.issues.md

Next: /speckit.wireframe.generate [feature] --regen
  (to regenerate pattern-violating SVGs)
═══════════════════════════════════════════
```

---

## When to run

1. **After** `/speckit.wireframe.review` passes for a feature (per-SVG checks are clean)
2. **Before** `/speckit.wireframe.review` for sign-off (to catch inter-SVG drift before it locks in)
3. **Periodically** across the whole project (`--all`) to audit cumulative drift

## Classification

Inspection issues are always classified as `PATTERN_VIOLATION` — they're neither PATCH nor REGEN in the review sense. They're drift findings. Treatment:

- **Small drift** (e.g. y=30 vs y=28) → patch during next `generate --patch`
- **Large drift** (e.g. different layout structure) → regenerate

## DO NOT

- Run before per-SVG review passes — noise obscures real drift
- Manually edit `.issues.md` files — they're auto-generated and append-only
- Write to `.terminal-status.json` or any queue file
- Ignore pattern violations — they signal template/convention drift that compounds over time
