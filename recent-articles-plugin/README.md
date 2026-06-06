# Recent Articles — WordPress Plugin

Pixel-perfect recent articles card grid for the Dr. Shiv Diggikar site.
Each card uses a pastel color block with a centered emoji icon (per-post),
category badge, custom reading time, custom excerpt, and a Read CTA.

## Features

- `[recent_articles]` shortcode with sanitized attributes.
- Per-post meta box: icon, background color, badge color, reading time,
  custom excerpt, custom author label.
- AJAX category filter + load-more (jQuery, no extra dependencies).
- Elementor (Free + Pro) compatible — assets auto-detected in widgets.
- Conditional asset loading — only enqueued when the shortcode is present.
- Accessibility: ARIA roles, focus styles, reduced-motion support, semantic HTML.
- Security: nonces, capability checks, sanitized inputs, escaped outputs.
- Performance: single WP_Query, prefetched term & meta caches, no N+1.

## Installation

1. Copy `recent-articles-plugin/` into `wp-content/plugins/`.
2. Activate **Recent Articles** in the WordPress admin.
3. Drop `[recent_articles]` into a page, post, or Elementor Shortcode widget.

## Shortcode

```
[recent_articles]
[recent_articles posts="6"]
[recent_articles posts="9" columns="3" category="nutrition"]
[recent_articles orderby="date" order="DESC"]
[recent_articles featured="yes"]
[recent_articles show_filter="false" load_more="false"]
[recent_articles heading="Latest Articles" label="OUR BLOG"]
```

| Attribute     | Default | Notes                                            |
|---------------|---------|--------------------------------------------------|
| `posts`       | `6`     | 1–50                                             |
| `columns`     | `3`     | 1–4                                              |
| `category`    | `''`    | Comma-separated category slugs                   |
| `show_filter` | `true`  | Show category tab bar                            |
| `load_more`   | `true`  | Show AJAX load-more button                       |
| `orderby`     | `date`  | `date \| title \| rand \| menu_order`            |
| `order`       | `DESC`  | `ASC \| DESC`                                    |
| `featured`    | `no`    | Only show posts with `_ra_featured` meta = `1`   |
| `heading`     | `''`    | Override section heading                         |
| `label`       | `''`    | Override eyebrow label                           |

## Per-post controls

Open any **post** → sidebar meta box **Recent Articles Card**:

- Card Icon (emoji whitelist: 🍼 🌿 💉 🫁 🧠 😴 👶 🫀 🩺 …)
- Card Background Color (color picker + curated pastel palette)
- Category Badge Color (color picker + curated accent palette)
- Reading Time (minutes — 0 auto-calculates)
- Custom Excerpt (≤ 500 chars)
- Custom Author Label (≤ 100 chars)

## Requirements

- WordPress 6.0+
- PHP 8.0+
- jQuery (bundled with WordPress)
