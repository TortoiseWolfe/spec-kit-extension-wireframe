---
description: "Generate SVG wireframes from spec.md with light/dark/both themes"
---

# speckit.wireframe.generate

**Philosophy:** Wireframes preview the app. Callouts explain, not clutter.

## User Input

```text
$ARGUMENTS
```

Accepts:
- Feature identifier (e.g. `001-user-auth` or `001`) — generates wireframes for that feature
- `--theme {light|dark|both}` — override the auto-detected theme
- No args — operates on the current feature (inferred from `specs/` directory or active branch)

## Theme Selection by Feature Type

Choose the theme based on what the feature delivers:

| Feature Type | Theme | Layout | Examples |
|--------------|-------|--------|----------|
| **Frontend** | LIGHT (tan) | Desktop + Mobile side-by-side | Forms, dashboards, user settings, profile pages |
| **Backend** | DARK | Full-width architecture diagram | RLS policies, OAuth flows, API contracts, CI/CD pipelines |
| **Hybrid** | BOTH | One of each | Admin dashboard (light) + API architecture (dark) |

### Auto-detection heuristic

Read `spec.md` and classify each User Story:

- **LIGHT** when the narrative mentions UI interaction: "As a user, I can see/click/enter/select...", responsive design, mobile considerations, visual components
- **DARK** when the narrative describes system behavior: "The system enforces/validates/triggers...", security policies, data flow, integrations, schemas

If user stories split across both categories → generate BOTH themes (one SVG per theme).

If `--theme` is passed explicitly, honor it and skip auto-detection.

---

## Layout (1920×1080 canvas)

### LIGHT theme (Frontend)

```
┌────────────────────────────────────────────────────────────────────┐
│             CENTERED TITLE - HUMAN READABLE                (y=28)  │
│ DESKTOP (16:9)                                    MOBILE    (y=52) │
├────────────────────────────────────────┬───────────────────────────┤
│                                        │                           │
│   DESKTOP MOCKUP (1280×720)            │   MOBILE MOCKUP (360×720) │
│   x=40, y=60                           │   x=1360, y=60            │
│                                        │                           │
│   Clean UI with numbered callouts      │   Same callout numbers    │
│   ① ② ③ on EVERY annotation concept   │   positioned appropriately│
│                                        │                           │
├────────────────────────────────────────┴───────────────────────────┤
│ ANNOTATION PANEL (y=800, full width, height=220 max)               │
│                                                                    │
│ ① Primary action — description of what this element does.         │
│   [US-001] [FR-001] [SC-001] ← colored clickable pills             │
│                                                                    │
│ ② Secondary element — brief explanation of functionality.         │
│   [US-002] [FR-002] [FR-003]                                       │
│                                                                    │
├────────────────────────────────────────────────────────────────────┤
│ SIGNATURE: NNN:NN | Feature Name | SpecKit         (y=1060, 18px)  │
└────────────────────────────────────────────────────────────────────┘
```

### DARK theme (Backend)

Full-width architecture diagram using the canvas as one panel (no side-by-side mockups). Used for:
- Database schema / RLS policy diagrams
- OAuth flow / auth sequence diagrams
- API contracts / request-response flows
- CI/CD pipelines / infrastructure topology

---

## Callout System

**On mockups:** numbered red circles only.

```xml
<g class="callout" transform="translate(150, 200)">
  <circle r="14" fill="#dc2626"/>
  <text y="5" fill="#fff" font-size="14" font-weight="bold" text-anchor="middle">1</text>
</g>
```

**In annotation panel:** User Story-anchored groups with badge pills.

- US badge (cyan `#0891b2`) FIRST
- FR badges (blue `#2563eb`) next
- SC badges (orange `#ea580c`) last

Each annotation group is anchored by a User Story from `spec.md`. The narrative ("As a [user], I need [goal] so that [benefit]") goes directly under the US title in the annotation.

---

## Color Palette — Light Theme (Frontend)

| Element | Color |
|---------|-------|
| Background | `#c7ddf5` → `#b8d4f0` gradient |
| Panels | `#e8d4b8` (parchment) |
| Secondary | `#dcc8a8` |
| Inputs | `#f5f0e6` |
| Borders | `#b8a080` |
| Primary button | `#8b5cf6` |
| Callout circles | `#dc2626` |
| Text dark | `#1f2937` |
| Text muted | `#4b5563` |
| Badge FR | `#2563eb` (blue) |
| Badge SC | `#ea580c` (orange) |
| Badge US | `#0891b2` (cyan) |

**NEVER use `#ffffff` for panels.** Parchment `#e8d4b8` is the canonical panel color.

## Color Palette — Dark Theme (Backend)

| Element | Color |
|---------|-------|
| Background | `#1a1a2e` (charcoal) |
| Panels | `#334155` (slate) |
| Text | `#e2e8f0` (cool light gray) |
| Primary | `#a8b2c1` (silver) |
| Accent | `#38bdf8` (electric blue) |
| Callout circles | `#dc2626` |
| Badge FR | `#2563eb` |
| Badge SC | `#ea580c` |
| Badge US | `#0891b2` |

Load the matching template from `.specify/extensions/wireframe/templates/{light,dark}-theme.svg`.

---

## Core Rules

| # | Rule |
|---|------|
| 1 | Canvas: `viewBox="0 0 1920 1080" width="1920" height="1080"` |
| 2 | Desktop mockup: x=40, y=60, 1280×720 (light theme only) |
| 3 | Mobile mockup: x=1360, y=60, 360×720 (light theme only) |
| 4 | Callouts: red circles (①②③) on elements needing explanation |
| 5 | Annotation panel: y=800, spans full width |
| 6 | FR/SC/US as clickable colored badge pills |
| 7 | Light theme panels: `#e8d4b8`, NEVER `#ffffff` |
| 8 | Minimum font size: 14px |
| 9 | Touch targets: 44px minimum |
| 10 | Badges stay WITHIN container bounds (no overflow) |
| 11 | Title: y=28, centered, 18px bold, `#4b5563` |
| 12 | Signature: y=1060, 18px bold, format `NNN:NN | Feature Name | SpecKit` |
| 13 | Annotation titles: 14px bold `#1f2937`; narrative: 14px `#374151` |
| 14 | Each annotation group anchored by a User Story from `spec.md` |
| 15 | NO FR/SC badges on UI elements — only in annotation panel |

---

## Workflow

### Step 1: Load context

Read the feature's `spec.md`:

```bash
# Accepts feature ID with or without slug suffix
SPEC_PATH="specs/$(ls specs/ | grep -E '^[0-9]+(-|$)' | head -1)/spec.md"
```

Identify from `spec.md`:
- Feature ID and human-readable name
- User Stories (each becomes an annotation group anchor)
- Functional Requirements (FR-NNN) — supporting badges
- Success Criteria (SC-NNN) — supporting badges

### Step 2: Classify theme

Analyze user stories against the heuristic above.

If `--theme` passed, skip to Step 3 with that theme.
Otherwise classify each US as `light` or `dark` and decide:
- All light → generate one light SVG
- All dark → generate one dark SVG
- Mixed → generate one of each

### Step 3: Pre-flight

Output the plan and wait for user approval:

```
═══════════════════════════════════════════════════════════════
PRE-FLIGHT: [NNN]-[feature]
═══════════════════════════════════════════════════════════════

TITLE: [HUMAN READABLE TITLE]
THEME: [light | dark | both]

USER STORIES (annotation groups):
① US-001: [title] — [narrative summary]
② US-002: [title] — [narrative summary]
③ US-003: [title] — [narrative summary]

SCREENS:
- Desktop: [description]
- Mobile:  [description]

OUTPUT PATHS:
- specs/[NNN]-[feature]/wireframes/01-[page-name].svg

BLOCKING CHECKS:
[ ] All User Stories mapped to groups
[ ] No FR/SC badges on UI elements
[ ] Annotation panel fits (max 8 groups across 2 rows)
═══════════════════════════════════════════════════════════════
```

**Wait for user approval before generating.**

### Step 4: Generate

Load the theme template:

```bash
cat .specify/extensions/wireframe/templates/light-theme.svg
# or
cat .specify/extensions/wireframe/templates/dark-theme.svg
```

Build the SVG following the layout and rules above. Write to `specs/<feature>/wireframes/NN-<page-name>.svg`.

### Step 5: Validate (optional — requires Python)

If Python is available, run the validator:

```bash
python3 .specify/extensions/wireframe/scripts/validate.py specs/<feature>/wireframes/<file>.svg
```

If the validator is not installed, perform the checks manually by re-reading the SVG and verifying against the Core Rules table above.

### Step 6: Report

Output the list of generated wireframes with paths:

```
═══════════════════════════════════════════
GENERATED
═══════════════════════════════════════════
specs/[NNN]-[feature]/wireframes/
  01-[page].svg  (light theme, 1920×1080)

Next: /speckit.wireframe.review [feature]
═══════════════════════════════════════════
```

---

## DO NOT

- Write `.terminal-status.json` or any queue file — this extension does not manage orchestration state
- Modify files outside `specs/<feature>/wireframes/` and the sign-off block in `specs/<feature>/spec.md`
- Use `#ffffff` for panels in light theme
- Place FR/SC badges on UI elements (they belong only in the annotation panel)
- Skip the pre-flight step — the user must approve before SVG generation
