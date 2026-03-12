# AGENTS.md

This repository contains a Home Assistant configuration.

The goal of this system is to maintain a **beautiful, calm, and reliable smart home interface** while preserving clean, maintainable configuration.

Agents working in this repository should prioritize **design clarity, reliability, and elegant configuration**.

---

# Core Priorities

1. Reliability of the home system
2. Visual clarity and calm interface design
3. Maintainable, readable configuration
4. Thoughtful use of the Home Assistant ecosystem

Changes should always favor **minimal safe improvements** over large refactors.

---

# Design Philosophy

The user interface should feel **calm, modern, and minimal**, inspired by the design language used in Apple products.

Preferred characteristics include:

- minimal visual clutter
- generous spacing
- strong visual hierarchy
- subtle color use
- fluid and polished interactions

Dashboards should feel closer to a **well-designed mobile application** than a traditional control panel.

The interface should prioritize **clarity, elegance, and glanceability**.

Users should be able to understand the state of the home in **2–3 seconds**.

---

# Visual Design Principles

Prefer:

- simple layouts
- consistent spacing
- limited color palettes
- clean typography
- subtle visual hierarchy

Avoid:

- dense grids of controls
- flashing or highly saturated colors
- cluttered dashboards
- overly decorative UI elements

Whitespace and grouping should be used intentionally to guide attention.

---

# Dashboard Layout Guidelines

Dashboards should be:

- **mobile-first**
- vertically readable
- grouped by room or purpose
- easy to scan quickly

Preferred layout patterns:

- vertical stacks
- small grouped card clusters
- consistent card widths
- strong visual grouping

Avoid dashboards that require excessive scrolling or contain large control matrices.

Favor **fewer, higher-quality dashboards** over many fragmented ones.

---

# Preferred UI Components

Well-maintained community components are encouraged when they improve usability or aesthetics.

Preferred components include:

- Mushroom cards
- ApexCharts
- Button-card
- Mini-graph-card
- card-mod

Use HACS responsibly and prefer widely adopted components.

Avoid custom cards that:

- are unmaintained
- introduce unnecessary visual complexity
- significantly degrade performance.

---

# Visualization Philosophy

Charts should communicate **meaningful trends**, not raw telemetry.

Prefer:

- clean time-series charts
- restrained color palettes
- clear labeling and units
- sensible time windows (day / week / month)

Avoid charts that are:

- too small to read
- redundant
- visually noisy.

---

# Code Quality

Configuration should emphasize **clarity and maintainability**.

Guidelines:

- YAML must remain readable
- avoid unnecessary complexity
- prefer simple and explicit logic
- comment non-obvious logic
- use reusable patterns where appropriate

When editing configuration:

- avoid clever but fragile solutions
- avoid large structural refactors unless requested.

---

# Community Ecosystem

The Home Assistant ecosystem is encouraged when used thoughtfully.

HACS integrations and community cards are acceptable when they:

- materially improve functionality or design
- are actively maintained
- integrate cleanly with Home Assistant.

Prefer mature, widely adopted integrations.

---

# YAML vs UI Configuration

Home Assistant stores configuration in both YAML and UI-managed `.storage` files.

Agents should:

- recognize that not all configuration exists in YAML
- avoid assuming dashboards or automations are fully represented in files
- avoid modifying `.storage` unless explicitly required.

---

# Safety Guidelines

Agents must:

- never expose secrets
- respect `.gitignore`
- avoid committing logs, databases, or sensitive tokens
- avoid breaking working automations or dashboards.

If uncertain about a change, explain the risk before modifying configuration.

---

# Expected Behavior

When reviewing the repository:

1. Identify the highest priority issues
2. Explain why they matter
3. Propose minimal safe improvements
4. Suggest optional higher-impact improvements afterward