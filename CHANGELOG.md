# Changelog

All notable changes to this extension will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

## [0.1.1] - 2026-04-21

### Fixed

- Corrected slash-command references in `extension.yml` description and `README.md` to use the `/speckit.`-prefixed names (`/speckit.plan`, `/speckit.tasks`, `/speckit.implement`) instead of the unprefixed forms. The unprefixed names never existed in published Spec Kit releases; the previous text would have misled users following the docs. Resolves #1.

## [0.1.0] - 2026-04-17

### Added

- Initial release.
- Command `/speckit.wireframe.generate` — create SVG wireframes from `spec.md` with light/dark/both theme auto-detection.
- Command `/speckit.wireframe.prep` — pre-load spec context, validation rules, and prior review issues.
- Command `/speckit.wireframe.review` — review wireframes, classify issues as PATCH/REGENERATE/PASS, and on sign-off write wireframe paths into `spec.md` under `## UI Mockup`.
- Command `/speckit.wireframe.inspect` — cross-SVG consistency check for features with multiple wireframes.
- Command `/speckit.wireframe.screenshots` — capture standardized PNGs (Tier-2, requires Python or Docker; degrades gracefully).
- Hooks `after_specify`, `before_plan`, `after_implement` for end-to-end loop integration.
- Light (tan parchment) and dark (charcoal slate) SVG theme templates, ported from the ScriptHammer conventions.
- Configuration template with theme defaults, output paths, and optional validator/screenshot settings.

### Binding mechanism

On sign-off, approved wireframe paths are inserted into `spec.md` under a `## UI Mockup` block. Because `/speckit.plan`, `/speckit.tasks`, and `/speckit.implement` already load `spec.md` as constraint context, signed-off wireframes automatically become visual benchmarks for downstream commands — no changes to core SpecKit commands required.

### Prior art

Supersedes [github/spec-kit#1410](https://github.com/github/spec-kit/pull/1410), which predated SpecKit's extension system (#2130).

### Requirements

- Spec Kit: `>=0.6.0`
- Tier-1 commands: no external dependencies
- Tier-2 (optional): Python 3.9+ with `playwright` and `cairosvg`, or Docker

---

[Unreleased]: https://github.com/TortoiseWolfe/spec-kit-extension-wireframe/compare/v0.1.1...HEAD
[0.1.1]: https://github.com/TortoiseWolfe/spec-kit-extension-wireframe/compare/v0.1.0...v0.1.1
[0.1.0]: https://github.com/TortoiseWolfe/spec-kit-extension-wireframe/releases/tag/v0.1.0
