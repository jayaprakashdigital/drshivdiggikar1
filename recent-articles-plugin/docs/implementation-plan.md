# Phase 5 — Implementation Plan

## Files created
- `recent-articles.php` — bootstrap, constants, autoload, activation guard.
- `includes/class-meta-box.php` — per-post controls (icon, colors, RT, excerpt, author).
- `includes/class-shortcode.php` — shortcode, query builder, card renderer.
- `includes/class-assets.php` — register + conditional enqueue.
- `includes/class-ajax.php` — `ra_load_more` handler.
- `assets/css/frontend.css` — public styles matching the design.
- `assets/css/admin.css` — meta-box layout.
- `assets/js/frontend.js` — filter + load-more.
- `assets/js/admin.js` — color-picker bootstrap.
- `assets/images/placeholder.svg` — neutral fallback.
- `README.md`, `CHANGELOG.md`, `docs/*`.

## Risks
- Emoji rendering varies by OS — mitigated by `Apple Color Emoji, Segoe UI Emoji, Noto Color Emoji` stack.
- Lora/Inter not bundled — themes that already load them get the design;
  default platforms fall back to Georgia / system sans, retaining hierarchy.
- Color contrast on light pastels — content sits below the block on white.

## Dependencies
- WordPress 6.0+, PHP 8.0+, jQuery (bundled), `wp-color-picker`.

## Migration
- No DB migration. New meta keys are read-only-fallback (empty → palette index).
