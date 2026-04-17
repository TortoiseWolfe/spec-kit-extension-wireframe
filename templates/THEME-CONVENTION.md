# Wireframe Templates

## When to Use

### Feature Type Classification

| Feature Type | Theme | What to Generate                                    |
| ------------ | ----- | --------------------------------------------------- |
| **Frontend** | LIGHT | Desktop + Mobile wireframes showing UI screens      |
| **Backend**  | DARK  | Architecture/flow diagrams showing system design    |
| **Hybrid**   | BOTH  | Light wireframes for UI + Dark diagrams for backend |

### Decision Guide

**Frontend Features (LIGHT theme):**

- User-facing screens: forms, modals, dashboards, settings pages
- User Stories describe interactions: "As a user, I can see/click/enter..."
- Responsive design required (desktop + mobile layouts)
- Examples: User Profile, Cookie Consent, Blog Posts, Account Settings

**Backend Features (DARK theme):**

- Infrastructure/system features with no direct UI
- User Stories describe system behavior: "The system enforces/validates..."
- Security policies, data flows, API integrations
- Examples: RLS Policies, OAuth Flow, CSRF Protection, CI/CD Pipeline

**Hybrid Features (BOTH themes):**

- Features with backend logic AND user-facing dashboards
- Analytics: Dark (data pipeline architecture) + Light (analytics dashboard UI)
- Payments: Dark (Stripe integration flow) + Light (checkout screens)
- Admin Tools: Dark (permission system) + Light (admin interface)

### Theme Analysis Tool

Run theme analysis to get automated recommendations:

```bash
python3 docs/design/wireframes/validate-wireframe.py --analyze-themes [spec.md]
```

This outputs JSON classifying each User Story as `light` or `dark` based on keywords.

### Quick Reference

| Theme | Use For                          | Layout                          |
| ----- | -------------------------------- | ------------------------------- |
| Light | Forms, dashboards, user screens  | Desktop + Mobile side-by-side   |
| Dark  | RLS, OAuth, CSRF, CI/CD diagrams | Full-width architecture diagram |

## Color Palettes

### Light Theme

| Element        | Color                            |
| -------------- | -------------------------------- |
| Background     | `#c7ddf5` → `#b8d4f0` (gradient) |
| Panels         | `#e8d4b8` (parchment)            |
| Secondary      | `#dcc8a8`                        |
| Inputs         | `#f5f0e6`                        |
| Borders        | `#b8a080`                        |
| Primary button | `#8b5cf6` (violet)               |
| Text dark      | `#374151`                        |
| Text muted     | `#4b5563`                        |

### Dark Theme

| Element           | Color                            |
| ----------------- | -------------------------------- |
| Background        | `#0f172a` → `#1e293b` (gradient) |
| Panels            | `#334155` (slate)                |
| Borders           | `#475569`                        |
| Text headings     | `#ffffff`                        |
| Text body         | `#94a3b8`                        |
| Flow arrows       | `#8b5cf6` (violet)               |
| Data flow         | `#22c55e` (green)                |
| Error/deny        | `#ef4444` (red)                  |
| Security boundary | `#ef4444` (red dashed)           |

## Shared Badge Colors

Both themes use the same badge colors:

| Badge Type            | Color  | Hex       |
| --------------------- | ------ | --------- |
| US (User Story)       | Cyan   | `#0891b2` |
| FR (Functional Req)   | Blue   | `#2563eb` |
| SC (Success Criteria) | Orange | `#ea580c` |
| Callout circle        | Red    | `#dc2626` |

## Diagram Patterns (Dark Theme)

### Component Box

```xml
<g transform="translate(X, Y)">
  <rect width="200" height="80" rx="8" fill="#334155" stroke="#475569"/>
  <text x="100" y="45" text-anchor="middle" fill="#ffffff" font-size="16" font-weight="bold">Component</text>
</g>
```

### Database Symbol

```xml
<g transform="translate(X, Y)">
  <ellipse cx="60" cy="15" rx="60" ry="15" fill="#334155" stroke="#475569"/>
  <rect x="0" y="15" width="120" height="50" fill="#334155" stroke="#475569"/>
  <ellipse cx="60" cy="65" rx="60" ry="15" fill="#334155" stroke="#475569"/>
  <text x="60" y="45" text-anchor="middle" fill="#ffffff" font-size="14">Database</text>
</g>
```

### Flow Arrow

```xml
<line x1="200" y1="40" x2="300" y2="40" stroke="#8b5cf6" stroke-width="2" marker-end="url(#arrow)"/>
```

### Data Flow (Green)

```xml
<line x1="200" y1="40" x2="300" y2="40" stroke="#22c55e" stroke-width="2" marker-end="url(#arrow-green)"/>
```

### Security Boundary

```xml
<rect x="0" y="0" width="400" height="200" rx="8" fill="none" stroke="#ef4444" stroke-width="2" stroke-dasharray="8,4"/>
<text x="10" y="20" fill="#ef4444" font-size="12" font-weight="bold">SECURITY BOUNDARY</text>
```

### RLS Policy Box

```xml
<g transform="translate(X, Y)">
  <rect width="180" height="60" rx="4" fill="#1e3a5f" stroke="#3b82f6"/>
  <text x="90" y="25" text-anchor="middle" fill="#60a5fa" font-size="12" font-weight="bold">RLS POLICY</text>
  <text x="90" y="45" text-anchor="middle" fill="#94a3b8" font-size="11">tenant_id = auth.uid()</text>
</g>
```

### External Service

```xml
<g transform="translate(X, Y)">
  <rect width="160" height="60" rx="8" fill="#312e81" stroke="#6366f1"/>
  <text x="80" y="35" text-anchor="middle" fill="#a5b4fc" font-size="14">External API</text>
</g>
```

## Layout Differences

| Aspect          | Light Theme                           | Dark Theme                     |
| --------------- | ------------------------------------- | ------------------------------ |
| Content area    | Desktop (1280x720) + Mobile (360x720) | Full-width diagram (1840x700)  |
| Headers/footers | Included via `<use>`                  | None (architecture focus)      |
| Primary focus   | User interface mockups                | System architecture flows      |
| Callouts        | Numbered circles on UI elements       | Numbered circles on components |

## Usage in /wireframe Skill

```bash
# Light theme (UX wireframes)
cat docs/design/wireframes/templates/light-theme.svg

# Dark theme (backend diagrams)
cat docs/design/wireframes/templates/dark-theme.svg
```
