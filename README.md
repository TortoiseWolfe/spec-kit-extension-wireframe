# spec-kit-extension-wireframe

**Visual feedback loop for Spec-Driven Development.** Generate SVG wireframes from your specs, review them for issues, sign them off, and have `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` automatically honor your signed-off wireframes as visual constraints.

## Why

Spec-Driven Development is great at turning natural language into code. It's less great at catching "this doesn't look right" before implementation is already written. This extension adds a visual sign-off step to the SDD workflow:

```
/speckit.specify
     ↓
/speckit.clarify
     ↓
/speckit.wireframe.generate  ← NEW: SVG mockups from spec
     ↓
/speckit.wireframe.review    ← NEW: review + sign-off writes paths into spec.md
     ↓
/speckit.plan                 (reads spec.md → honors wireframes)
     ↓
/speckit.tasks                (reads spec.md → honors wireframes)
     ↓
/speckit.implement            (reads spec.md → honors wireframes)
     ↓
/speckit.wireframe.screenshots ← NEW: regression check vs signed-off wireframes
```

**The binding mechanism is simple:** on sign-off, approved wireframe paths get written into `spec.md` under a `## UI Mockup` section. Because every downstream SpecKit command already reads `spec.md` as constraint context, the wireframe becomes a visual benchmark without any changes to core SpecKit commands.

## Installation

### Via catalog (recommended, once published)

```bash
specify extension add wireframe
```

### Local development

```bash
git clone https://github.com/TortoiseWolfe/spec-kit-extension-wireframe
cd /path/to/your/speckit-project
specify extension add --dev /path/to/spec-kit-extension-wireframe
```

Verify:

```bash
specify extension list
# ✓ Wireframe Visual Feedback Loop (v0.1.0)
#   Commands: 5 | Hooks: 3 | Status: Enabled
```

## Commands

| Command | Purpose |
|---------|---------|
| `/speckit.wireframe.prep` | Load spec + rules context before generating |
| `/speckit.wireframe.generate` | Create SVG wireframes from spec.md (light/dark/both themes) |
| `/speckit.wireframe.review` | Review wireframes, classify issues, **sign off into spec.md** |
| `/speckit.wireframe.inspect` | Cross-SVG consistency check |
| `/speckit.wireframe.screenshots` | Capture standardized PNGs (Tier-2, needs Python or Docker) |

## Hooks

The extension registers three optional hooks into SpecKit's workflow:

| Hook | Prompts | What it offers |
|------|---------|----------------|
| `after_specify` | "Generate wireframes for this feature now?" | Runs `wireframe.generate` right after spec creation |
| `before_plan` | "Review and sign off wireframes before planning?" | Ensures wireframes are signed off before `/speckit.plan` locks in the implementation plan |
| `after_implement` | "Capture implementation screenshots and compare?" | Regression check: captures the built UI and compares against signed-off wireframes |

All hooks are **optional** — the extension prompts before executing, and you can decline to continue the SpecKit workflow unchanged.

## Theme convention

The extension ships two canonical templates in `templates/`:

- **Light theme** (`light-theme.svg`) — parchment/tan canvas for **frontend** features (UI screens, forms, dashboards)
- **Dark theme** (`dark-theme.svg`) — charcoal/slate canvas for **backend** features (architecture diagrams, RLS policies, OAuth flows, API contracts)

The generator auto-classifies each User Story from `spec.md` as frontend (UI-describing narrative) or backend (system-describing narrative). Features that mix both → one wireframe per theme.

Override auto-detection with `--theme {light|dark|both}`.

Theme tokens are documented in `templates/THEME-CONVENTION.md`.

## Configuration

Copy `config-template.yml` to `.specify/extensions/wireframe/wireframe-config.yml` and customize. All settings are optional. Common overrides:

```yaml
themes:
  frontend: "light"   # default
  backend: "dark"     # default
  hybrid: "both"      # default

output:
  svg_dir: "specs/{feature}/wireframes"  # where SVGs land

validator:
  enabled: false      # set true if you install the optional Python validator
```

## Tiers

The extension is designed with **progressive enhancement**:

- **Tier 1** (zero deps): `generate`, `prep`, `review`, `inspect` — AI does all the work via reading SVG source + reasoning. Works on any machine.
- **Tier 2** (optional): `screenshots` and a validator script use Python (`playwright` + `cairosvg`) or Docker for standardized PNG capture and mechanical validation. When unavailable, commands gracefully degrade with an informational message — they don't fail.

You can use this extension with just Tier 1 — everything core works. Tier 2 adds richer visual review and regression checking when you want it.

## Example: full loop

Scratch SpecKit project:

```bash
specify init my-demo
cd my-demo
specify extension add wireframe
```

Then in your agent:

```
/speckit.specify   "User login page with email and password, shows error on invalid credentials"
  → creates specs/001-user-login/spec.md

after_specify hook: "Generate wireframes for this feature now?" → y
  → runs /speckit.wireframe.generate 001
  → auto-classifies as frontend → generates light-theme SVG
  → writes specs/001-user-login/wireframes/01-login.svg

/speckit.wireframe.review 001
  → analyzes SVG, reports: PASS
  → prompts sign-off → y
  → updates specs/001-user-login/spec.md with ## UI Mockup block

/speckit.plan
  → reads spec.md (now includes wireframe reference)
  → plan.md now lists the wireframe as a visual constraint

/speckit.tasks    → tasks honor layout constraints from wireframe
/speckit.implement → implementation matches signed-off mockup

after_implement hook: "Capture implementation screenshots and compare?" → y
  → captures built UI
  → side-by-side diff vs signed-off wireframe
  → reports visual drift (if any)
```

## What this extension does NOT do

- **Orchestration** — no queue, no multi-terminal dispatch, no terminal status files. If you want that layer, see [TortoiseWolfe/First-Frame](https://github.com/TortoiseWolfe/First-Frame), which builds on this extension with a Planner/Generator/Reviewer/Inspector terminal model.
- **Style guides** — the extension enforces its own canvas and color conventions. If you want different conventions, fork the `templates/` directory and publish a preset that overrides them.
- **Replace `/speckit.constitution`** — project-wide design standards still belong in the constitution. This extension handles per-feature wireframes.

## Prior art

This extension supersedes [github/spec-kit#1410](https://github.com/github/spec-kit/pull/1410), which proposed adding wireframe generation to SpecKit core. That PR predated the extension system (#2130); this extension takes the same ideas into the post-extension-system architecture and extends them with the sign-off binding mechanism and tier-based graceful degradation.

## License

MIT — see [LICENSE](LICENSE).

## Version

- Version: 0.1.0
- Compatible with Spec Kit: `>=0.6.0`
