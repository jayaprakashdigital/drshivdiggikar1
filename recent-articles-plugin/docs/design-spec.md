# Phase 2 — Design Spec (reverse-engineered from screenshot)

## Layout
- Container max-width: ~1240 px, 24 px horizontal padding.
- Section header: eyebrow label + heading on the left, pill "View All →" button on the right.
- Grid: **3 columns × 2 rows**, gap ~28 px, equal-height cards.
- Card radius: 18 px; soft 2-layer shadow.

## Typography
- Eyebrow label: 12 px, weight 700, uppercase, letter-spacing .18em, color `#B45309` (amber), with a 28 × 3 px bar before it.
- Section heading: serif (Lora-like), ~44 px, weight 700, color `#0B1B3A` (deep navy).
- Card category badge: 10.5 px, 700, uppercase, .12em tracking, colored text on 10 % tint of the same color.
- Read time: 12.5 px, 500, muted gray, clock SVG.
- Card title: serif, 20 px, 700, navy, line-height 1.28.
- Excerpt: 14 px, 1.6 line-height, body gray, 3-line clamp.
- Author name: 13.5 px, 500, navy.
- Read button: 13 px, 500, navy, 1.5 px gray border, rounded-full.

## Card structure

### Header (icon block)
- Height: 170 px desktop, 140 px mobile.
- Flat pastel background, per-post:
  - Peach `#FCEFD5`, Mint `#D5F0E5`, Lavender `#E5DDF8`,
    Pink `#FBD9D8`, Green `#D7F2D7`, Sand `#FBE4C7`.
- Centered emoji icon, ~64 px, with subtle drop-shadow.

### Body
- Padding 22 × 24 px.
- Meta row: badge + clock/read-time.
- Title (serif).
- Excerpt (3 lines).

### Footer
- 1 px divider above.
- Left: 30 px teal `#0E5B5B` circular avatar with white initials (e.g. "SD") + author name.
- Right: rounded pill "Read →" button.

## Responsive
- ≥ 1024 px → 3 columns.
- 640–1023 px → 2 columns; header stacks on small.
- < 640 px → 1 column; icon block 140 px; reduced padding.
