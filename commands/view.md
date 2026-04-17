---
description: "Launch the interactive wireframe viewer in a browser"
---

# speckit.wireframe.view

Open the interactive viewer for all wireframes in this project. Side-navigation auto-discovered from `specs/*/wireframes/*.svg`, with keyboard shortcuts, zoom, focus mode, and status badges derived from `.issues.md` files.

## User Input

```text
$ARGUMENTS
```

Accepts:
- `--port N` — override default port 3000
- `--no-open` — start the server but don't auto-open the browser
- `--rebuild-manifest` — regenerate the wireframes-manifest.json before launching
- No args — sensible defaults

## Workflow

### Step 1: Verify prerequisites

The viewer needs **Python 3.9+** for the manifest generator + static server. Check:

```bash
python3 --version
```

If Python 3.9+ is missing, print this and stop:

```
═══════════════════════════════════════════
VIEWER REQUIRES PYTHON 3.9+
═══════════════════════════════════════════
The wireframe viewer uses Python's built-in http.server
for a zero-dependency static server.

Install Python 3.9+ and re-run this command.

Alternative: open
  .specify/extensions/wireframe/viewer/viewer.html
directly in a browser. (Some features like manifest
auto-discovery will not work without a server.)
═══════════════════════════════════════════
```

### Step 2: Generate/refresh the manifest

Always regenerate unless `--rebuild-manifest` is explicitly disabled — the cost is sub-second and manifests drift when wireframes get added or reviewed.

```bash
python3 .specify/extensions/wireframe/scripts/generate-manifest.py \
  --specs-dir specs \
  --output .specify/extensions/wireframe/viewer/wireframes-manifest.json
```

Output shows feature + wireframe count:

```
Wrote manifest: .specify/extensions/wireframe/viewer/wireframes-manifest.json
  Features: 3
  Wireframes: 7
```

### Step 3: Write project config

Create `.specify/extensions/wireframe/viewer/viewer-config.json` with the current project name (derived from the current directory basename if not otherwise set):

```json
{
  "project_name": "<project-dir-basename>",
  "project_repo": ""
}
```

If a repo URL can be inferred (e.g. from `git remote get-url origin`), include it. Otherwise leave empty — the viewer degrades gracefully.

### Step 4: Launch the server

Serve from the **project root** (not the viewer directory) so absolute paths like `/specs/<feature>/wireframes/<svg>` resolve without Python's `http.server` blocking `..` traversal:

```bash
python3 -m http.server 3000 --bind 127.0.0.1
```

The viewer is then reachable at `/.specify/extensions/wireframe/viewer/viewer.html` and the SVGs at `/specs/...`.

Report:

```
═══════════════════════════════════════════
VIEWER RUNNING
═══════════════════════════════════════════
URL:     http://localhost:3000/.specify/extensions/wireframe/viewer/viewer.html
Manifest: 3 features, 7 wireframes

Keyboard shortcuts:
  ← →      Previous / next wireframe
  1-9      Jump to feature N
  F        Toggle focus mode
  L        Toggle legend
  +/-      Zoom
  ?        Show all shortcuts

Stop the server with Ctrl+C.
═══════════════════════════════════════════
```

If `--no-open` was not passed, attempt to open the browser:

```bash
URL="http://localhost:3000/.specify/extensions/wireframe/viewer/viewer.html"

# Linux
xdg-open "$URL" 2>/dev/null

# macOS
open "$URL" 2>/dev/null

# Windows / WSL
start "$URL" 2>/dev/null
```

Fall back to printing the URL if auto-open fails.

---

## What the viewer shows

- **Left sidebar**: auto-generated nav grouped by feature, with status badges:
  - 📝 draft (no `.issues.md` yet)
  - 🚧 review (`.issues.md` present, status PATCH or REGENERATE)
  - ✅ approved (`.issues.md` present, status PASS — signed off in spec.md)
- **Center**: the SVG at configurable zoom
- **Footer**: project link, extension link, portfolio link, coffee link
- **Focus mode** (F): hides nav and footer for full-canvas review
- **Legend drawer** (L): shows callout color legend and badge keys

## Manifest refresh

The manifest is generated fresh each `/speckit.wireframe.view` invocation. If wireframes change while the viewer is running, re-run this command to refresh, or refresh the browser after running:

```bash
python3 .specify/extensions/wireframe/scripts/generate-manifest.py
```

## DO NOT

- Bind to `0.0.0.0` without explicit user consent — localhost-only by default for security
- Keep the server running in the background after the command exits — leave it foreground so Ctrl+C works cleanly
