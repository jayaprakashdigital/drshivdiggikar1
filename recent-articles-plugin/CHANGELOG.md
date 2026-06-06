# Changelog

## 2.0.0 — 2026-06-06

### Added
- Per-post meta box: card icon (emoji), background color, badge color,
  reading time, custom excerpt, custom author label.
- Curated pastel + accent color palettes (color picker integration).
- Heading / label shortcode overrides.
- `featured="yes"` shortcode attribute (queries `_ra_featured` meta).
- Activation hook with PHP version guard.

### Changed
- Card design rebuilt to match the LATEST POSTS / Recent Articles
  reference screenshot: pastel icon block instead of featured image,
  per-card accent badge, refined typography (Lora + Inter), shadows
  and spacing tuned for parity.
- Asset enqueue split into `register` + `maybe_enqueue` priorities
  so other plugins can dequeue/override before output.
- AJAX handler now passes the card index for deterministic palette
  fallbacks and respects `featured`.

### Security
- Strict whitelist for the emoji icon field.
- Hex sanitization for color fields via `sanitize_hex_color`.
- Length caps on excerpt (500) and author label (100).
- All inputs nonce-verified and capability-checked.

### Performance
- `update_post_term_cache` + `update_post_meta_cache` true to avoid N+1.
- `no_found_rows` flips with `load_more` to skip COUNT when not needed.

## 1.0.0
- Initial release.
