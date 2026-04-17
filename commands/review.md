---
description: "Review wireframes, classify issues as PATCH or REGENERATE, sign off approved wireframes into spec.md"
---

# speckit.wireframe.review

**The critical binding step.** When a wireframe is approved, paths get written into `spec.md` under `## UI Mockup`. Because SpecKit's `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` all load `spec.md` as context, signed-off wireframes automatically become visual constraints on the downstream chain.

## User Input

```text
$ARGUMENTS
```

Accepts:
- Feature identifier (e.g. `001`) — review all wireframes for that feature
- `NNN:NN` — review a single wireframe (e.g. `002:01` → `002-*/01-*.svg`)
- No args — review the current feature

## Workflow

### Step 1: Capture screenshots (optional, Tier-2)

If Python + Docker available, run screenshot capture for richer visual review:

```bash
python3 .specify/extensions/wireframe/scripts/screenshots.py $ARGUMENTS
```

If not available, skip to Step 2 — the AI reviews the SVG source directly.

### Step 2: Read each wireframe

For each SVG being reviewed:

1. Read the SVG source (`Read` tool)
2. If screenshots exist, read them too (`overview.png`, `quadrant-tl.png`, etc.)
3. Read the corresponding spec.md to understand what the wireframe is meant to represent

### Step 3: Apply checks

**Structural checks** (from the SVG source):

| Check | Rule | Code |
|-------|------|------|
| Canvas size | 1920×1080 viewBox | STR-001 |
| Title position | y=28, centered | STR-002 |
| Signature | y=1060, bold, correct format | STR-003 |
| Desktop mockup bounds | x=40, y=60, 1280×720 (light) | STR-004 |
| Mobile mockup bounds | x=1360, y=60, 360×720 (light) | STR-005 |
| Annotation panel | y=800, full width | STR-006 |
| Font sizes | All text ≥ 14px | STR-007 |
| Panel color | `#e8d4b8` (light), never `#ffffff` | STR-008 |
| Badge containment | All badges within container bounds | STR-009 |
| US anchoring | Every annotation group has a US badge first | STR-010 |

**Visual checks** (from screenshots if available, or from reasoning about SVG):

| Check | What to look for | Code |
|-------|------------------|------|
| Theme match | Dark bg on UI wireframe, or vice versa | VIS-001 |
| Text readability | Truncated, overlapping, or illegible text | VIS-002 |
| Arrow collisions | Arrows crossing text or UI elements | VIS-003 |
| Element overflow | Content outside container bounds | VIS-004 |
| Missing sections | Expected UI components not visible | VIS-005 |
| Visual balance | Awkward spacing, cramped layout | VIS-006 |
| Callout placement | Callouts obscuring important UI | VIS-007 |

**Coverage checks** (cross-referencing spec.md):

| Check | Rule | Code |
|-------|------|------|
| US coverage | Every User Story from spec.md has an annotation group | COV-001 |
| FR coverage | Every Functional Requirement is badged somewhere | COV-002 |
| SC coverage | Every Success Criterion is badged somewhere | COV-003 |

### Step 4: Classify each issue

- **PATCH** — Color, font size, typo, badge position, single-element fix
- **REGENERATE** — Layout change, structure change, missing sections, theme mismatch

**Rule:** If ANY issue is classified REGENERATE, the whole SVG needs regeneration. Don't mix-and-match.

### Step 5: Log issues

Write findings to `specs/<feature>/wireframes/<svg-name>.issues.md`:

```markdown
# [SVG Name] Review

**Status:** REGENERATE | PATCH | PASS
**Date:** [YYYY-MM-DD]
**Structural issues:** [N]
**Visual issues:** [N]
**Coverage issues:** [N]

## Issues

| # | Check | Location | Issue | Classification |
|---|-------|----------|-------|----------------|
| 1 | VIS-002 | Desktop header | Text truncated | PATCH |
| 2 | COV-001 | Annotation panel | US-003 not represented | REGENERATE |
```

**NEVER delete `.issues.md` files.** They're audit trail — on resolution, append a "Resolved: [date]" note, don't delete.

### Step 6: Report

```
═══════════════════════════════════════════
REVIEW COMPLETE
═══════════════════════════════════════════
Feature: [NNN-feature-name]

SVG                   Status     Issues
────────────────────  ─────────  ──────
01-landing.svg        PASS       0
02-signup-flow.svg    PATCH      3
03-dashboard.svg      REGEN      1 (layout)

Actions needed:
  PATCH:     /speckit.wireframe.generate [feature] --patch
  REGEN:     /speckit.wireframe.generate [feature] --regen

Issues logged to:
  specs/[NNN-feature]/wireframes/*.issues.md
═══════════════════════════════════════════
```

### Step 7: Sign-off (CRITICAL — the binding step)

**If all reviewed wireframes are PASS**, offer sign-off:

```
═══════════════════════════════════════════
READY FOR SIGN-OFF
═══════════════════════════════════════════
All wireframes for [NNN-feature-name] passed review.

Sign off means:
  1. Wireframe paths get written to spec.md under `## UI Mockup`
  2. /speckit.plan, /speckit.tasks, /speckit.implement will load
     these wireframes as spec constraints
  3. Implementation will be visually bound to what you approve

Proceed with sign-off? [y/N]
═══════════════════════════════════════════
```

On user approval, edit `specs/<feature>/spec.md` to add or update a `## UI Mockup` section near the top (after the feature overview, before User Stories):

```markdown
## UI Mockup

Signed off: [YYYY-MM-DD]

- Desktop + Mobile: [`wireframes/01-landing.svg`](./wireframes/01-landing.svg) (light theme)
- Backend flow: [`wireframes/02-auth-flow.svg`](./wireframes/02-auth-flow.svg) (dark theme)

These wireframes are spec constraints — implementation should match their layout,
component structure, and interaction flow. Deviations require spec revision.
```

If a `## UI Mockup` block already exists, update it (preserve sign-off date history as a nested list if the user prefers).

Output confirmation:

```
═══════════════════════════════════════════
SIGNED OFF
═══════════════════════════════════════════
spec.md updated: specs/[NNN-feature]/spec.md

The following commands will now honor these wireframes:
  /speckit.plan      (reads spec.md as plan constraint)
  /speckit.tasks     (reads spec.md for task derivation)
  /speckit.implement (validates against spec.md)

Ready: /speckit.plan
═══════════════════════════════════════════
```

---

## DO NOT

- Sign off wireframes that have any REGENERATE or PATCH issues unresolved
- Delete `.issues.md` files — they're audit trail
- Write to `.terminal-status.json` or any queue file — this extension does not manage orchestration state
- Modify `spec.md` content outside the `## UI Mockup` block — the rest is the spec author's territory
