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

## Machine-generated text never tags anyone

GitHub emails every person whose `@handle` appears in an issue or comment body. The triage routine copies handles from upstream search results, so people outside this repo were emailed on every run ([#4](https://github.com/TortoiseWolfe/spec-kit-extension-wireframe/issues/4)).

Before posting any generated issue body or comment (triage log, cleanup note, anything), pipe it through the filter. It puts an invisible zero-width character after the `@` of every handle, so the text reads the same but GitHub sends no email:

```bash
python3 scripts/neutralize-mentions.py < body.md > body.safe.md
gh issue comment <N> --body-file body.safe.md
```

Write handles in inline code as well, never bare, and never mention anyone in the "log is long, consider closing" cleanup note. Tests: `python3 -m unittest discover -s tests -v`.
