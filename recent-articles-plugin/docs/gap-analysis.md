# Phase 3 — Gap Analysis

| # | Current v1.0.0                              | Target screenshot                       | Action                              |
|---|---------------------------------------------|-----------------------------------------|-------------------------------------|
| 1 | Featured image (16:9)                       | Flat pastel block + centered emoji      | Replace markup + add per-post meta  |
| 2 | Sans heading (system stack)                 | Serif heading (Lora) navy `#0B1B3A`     | Update CSS font stacks              |
| 3 | Blue badge fixed                            | Per-post colored badge (amber/teal/…)   | Per-post badge color + CSS var      |
| 4 | Default WP avatar                           | Solid teal `#0E5B5B` circle, white "SD" | Initials-only avatar by default     |
| 5 | Read button: filled accent                  | Subtle outlined pill                    | Outline pill style                  |
| 6 | View All in pill at header right            | Same                                    | Keep                                |
| 7 | Eyebrow label width:100% above heading      | Inline with heading, bar to the left    | Restructure header markup           |
| 8 | Reading time auto-only                      | Often custom (5–10 min)                 | Add `_ra_read_time` meta            |
| 9 | Excerpt auto-only                           | Often custom hand-written               | Add `_ra_excerpt` meta              |
|10 | No author label override                    | "Dr. Shiv Diggikar" everywhere          | Add `_ra_author_label` meta         |

## Code improvements
- Activation guard for PHP 8.0+.
- Split asset register vs. enqueue.
- Strict input sanitation in AJAX handler.
- Correct `no_found_rows` logic.
- Warm term + meta caches in main query.
