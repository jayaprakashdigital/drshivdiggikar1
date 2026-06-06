# Phase 9 — Performance Report

## Query
- Single `WP_Query` per shortcode render.
- `update_post_term_cache: true` → `get_the_category()` per card is cached.
- `update_post_meta_cache: true` → all `_ra_*` meta is prefetched, no N+1.
- `no_found_rows: true` when load-more is OFF → skips `SQL_CALC_FOUND_ROWS`.

## Assets
- CSS: ~6 KB minified-equivalent (single file, no @import).
- JS: ~1.5 KB minified-equivalent, vanilla jQuery, no extra libs.
- Conditional enqueue — assets only load on pages that contain the
  shortcode or an Elementor widget referencing it.
- Color picker assets are admin-only.

## DOM
- 6 cards = ~120 DOM nodes for the whole section. No iframes, no images
  by default (CSS-driven pastel block + emoji).

## Caching opportunities
- Output is naturally edge-cacheable (no per-request data). For sites
  with object caching, `WP_Query` results are cached automatically.
- AJAX responses can be cached for non-logged-in users by an upstream
  cache; nonce lifetime is 24 h by default.
