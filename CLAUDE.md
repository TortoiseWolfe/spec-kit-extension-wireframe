# spec-kit-extension-wireframe — project notes for Claude

## Maintenance commands

Use these slash commands for repo health checks. They're read-only and safe to run any time.

| Command | What it does |
|---|---|
| `/extension-status` | Full report: support triage, traffic stats, release/catalog health, external mentions, repo hygiene |
| `/extension-status --triage` | Same as the daily scheduled routine — open issues/PRs, upstream `github/spec-kit` mentions, external mentions only |
| `/extension-status --traffic` | Stars, clones, views, top referrers/paths (last 14d) |
| `/extension-status --mentions` | External GitHub mentions only (issue + code search for `"spec-kit-extension-wireframe"`) |

A weekday triage routine (`trig_01UKnJVB3zjxgVr83kvnjLVn`) runs at 9am ET (13:00 UTC) Mon–Fri and posts results to issue [#3 — 📬 Extension status triage log](https://github.com/TortoiseWolfe/spec-kit-extension-wireframe/issues/3). Manage at https://claude.ai/code/routines.
