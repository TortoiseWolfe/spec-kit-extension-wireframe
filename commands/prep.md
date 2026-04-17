---
description: "Load spec context and validation rules before generating wireframes"
---

# speckit.wireframe.prep

Prime context for wireframe work. Run before `/speckit.wireframe.generate` when you want to pre-load spec context, validation rules, and any prior review issues.

## User Input

```text
$ARGUMENTS
```

Accepts:
- Feature identifier (e.g. `001-user-auth` or `001`) — prep for specific feature
- No args — prep for patch mode (load prior issues only)

## Workflow

### Step 1: Resolve feature

If an argument is provided, resolve it to the full feature directory:

```bash
# Accept "001" or "001-user-auth" or "user-auth"
FEATURE_DIR="specs/$(ls specs/ | grep -E "^${ARG}" | head -1)"
```

If no argument, set `FEATURE_DIR=""` (patch mode).

### Step 2: Load mandatory files

Read these files and summarize nothing — the AI loads them silently for reasoning, then produces the priming block in Step 5.

1. **Validator rules** (if present):
   `.specify/extensions/wireframe/scripts/validate.py` — understand every check
2. **Known issues log** (if present):
   `.specify/extensions/wireframe/GENERAL_ISSUES.md` — avoid recurring mistakes
3. **Extension configuration** (if present):
   `.specify/extensions/wireframe/wireframe-config.yml` — theme defaults, output paths

If any of these files don't exist, continue without them — they're conveniences, not requirements.

### Step 3: Load feature context

**If `FEATURE_DIR` is set:**

Read `<FEATURE_DIR>/spec.md` and extract:
- Feature ID and title
- Overview / description
- User Stories (each `### User Story N` section)
- Functional Requirements (FR-NNN)
- Success Criteria (SC-NNN)
- Any `## UI Mockup` block (prior sign-off)

If `<FEATURE_DIR>/wireframes/` exists, list existing SVGs and their `.issues.md` files.

**If `FEATURE_DIR` is empty (patch mode):**

Find all `.issues.md` files under `specs/*/wireframes/` and load them. These describe patches needed across features.

### Step 4: Escalation check

Scan loaded issues for patterns that recur across multiple features. If a pattern appears in ≥3 features' issues files, flag it as an escalation candidate — it should probably be documented in `.specify/extensions/wireframe/GENERAL_ISSUES.md` to prevent repetition.

Output escalation candidates (if any):

```
═══════════════════════════════════════════
ESCALATION CANDIDATES
═══════════════════════════════════════════
Pattern: "Touch targets below 44px on mobile footer"
  Seen in: 001, 003, 005 (3 features)
  Suggest: Add to GENERAL_ISSUES.md

Pattern: "Badge overflow on annotation panel"
  Seen in: 002, 004 (2 features, 1 more and it should escalate)
═══════════════════════════════════════════
```

### Step 5: Output priming block

```
═══════════════════════════════════════════════════════════════
WIREFRAME PREP COMPLETE
═══════════════════════════════════════════════════════════════

MODE: [feature | patch]
FEATURE: [NNN-feature-name | n/a]

NON-NEGOTIABLES:
  - Canvas 1920×1080, no deviation
  - Light theme panels #e8d4b8 (never #ffffff)
  - Minimum font 14px, touch targets 44px
  - FR/SC badges only in annotation panel
  - Each annotation group anchored by a User Story

CRITICAL VALIDATOR RULES (if validator loaded):
  [list of top 5 rules by frequency from GENERAL_ISSUES.md]

FEATURE STATE:
  Existing SVGs: [count]
  Issues files: [count]
  Signed off: [yes/no — yes if spec.md has `## UI Mockup` block]

PRIOR ISSUES (if any):
  [count] PATCHABLE
  [count] REGENERATE

NEXT STEPS:
  Generate: /speckit.wireframe.generate [feature]
  Review:   /speckit.wireframe.review [feature]
═══════════════════════════════════════════════════════════════
```

---

## DO NOT

- Summarize the contents of loaded files — they're context for the AI, not output to the user
- Skip the escalation check — it's how recurring issues get promoted to shared knowledge
- Modify any files in this step — prep is read-only
