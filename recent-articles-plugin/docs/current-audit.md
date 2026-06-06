# Phase 1 — Audit of v1.0.0 (uploaded zip)

| Area              | Score |
|-------------------|-------|
| Architecture      | 7/10  |
| Security          | 7/10  |
| Performance       | 7/10  |
| Maintainability   | 7/10  |
| UX / Design fit   | 4/10  |

## Strengths
- Clean class split (Shortcode / Assets / Ajax) with strict types.
- Nonce on AJAX; basic sanitization of shortcode attributes.
- Conditional asset loading with Elementor awareness.

## Problems
1. **Design mismatch** — uses featured images + 16:9 aspect block, the
   target uses a flat pastel block with a single centered emoji icon.
2. **No per-post controls** — colors, icons, reading time, excerpt are
   not editable per post.
3. `wp_localize_script` runs inside the same hook that decides whether
   to enqueue, so the localized config never reaches the page if the
   "page has shortcode" detection runs before `the_post` is set.
4. AJAX trusts `$_POST['orderby']` directly into an array search without
   unslash / sanitize (low risk but lint-warning).
5. `no_found_rows` set to `! load_more` — flipped logic; load-more needs
   `max_num_pages`, so it must be `false` when load-more is enabled.
6. Section header markup wraps the heading and "View All" in the same
   flex row as the eyebrow label using `width: 100%` on the label, which
   collapses on narrow Elementor containers.
7. No PHP version guard on activation.
8. Missing `update_post_term_cache` / `update_post_meta_cache` warm-up
   on the main query → N+1 risk for `get_the_category` per card.

## Fixes applied in v2.0.0
- New `class-meta-box.php` with whitelisted emoji, color pickers,
  reading time, excerpt, author label, all nonce + capability gated.
- Shortcode rewritten to render pastel icon block + per-card CSS vars.
- Asset registration split from enqueue; localization runs once at
  registration time so it's always present when the script is enqueued.
- Strict input sanitation in `class-ajax.php` (`wp_unslash`, hard
  whitelists, integer clamping).
- `no_found_rows` logic corrected.
- Query caches warmed.
- Activation guard for PHP 8.0+.
