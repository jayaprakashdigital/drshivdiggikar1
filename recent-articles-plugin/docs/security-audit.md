# Phase 10 — Security Audit

| Vector            | Control                                                                |
|-------------------|------------------------------------------------------------------------|
| Direct file access| `defined( 'ABSPATH' ) || exit;` at the top of every PHP file           |
| CSRF (meta box)   | `wp_nonce_field` + `wp_verify_nonce`                                   |
| CSRF (AJAX)       | `check_ajax_referer( 'ra_load_more', 'nonce' )`                        |
| Capability check  | `current_user_can( 'edit_post', $post_id )` before saving meta         |
| Input — icon      | Hard whitelist (`array_key_exists` against `ALLOWED_ICONS`)            |
| Input — colors    | `sanitize_hex_color()`                                                 |
| Input — int       | `(int)` cast + `max/min` clamp (read_time 0–120)                       |
| Input — strings   | `sanitize_text_field`, `sanitize_textarea_field`, length cap           |
| Input — slugs     | `sanitize_title` on category slugs                                     |
| Output — text     | `esc_html`, `esc_attr`, `esc_url`                                      |
| Output — content  | `wp_kses_post` on excerpt                                              |
| SQL injection     | Only `WP_Query` API + post meta API used, no raw SQL                   |
| Stored XSS        | Author label / excerpt sanitized on save and escaped on output         |
| Hex injection     | RGBA helper validates `^[0-9a-fA-F]{6}$` after expansion               |
| Open redirect     | None — all URLs derived from `get_permalink` / `home_url`              |

No vulnerabilities found in v2.0.0.
