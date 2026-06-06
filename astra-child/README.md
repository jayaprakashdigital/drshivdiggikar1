# Astra Child — Dr. Shivashankar Diggikar

A drop-in Astra child theme that ports the standalone "Newborn Jaundice
Bangalore" HTML article design into the live WordPress single-post template,
without touching Astra parent files or breaking SEO / schema / breadcrumb
plugin support.

## Install

1. Zip this folder (`astra-child/`) or copy it directly into
   `wp-content/themes/astra-child/`.
2. WordPress → **Appearance → Themes** → activate **Astra Child — Dr.
   Shivashankar Diggikar**.
3. Make sure the parent **Astra** theme is also installed (required).

## File layout

```
astra-child/
├── style.css                       # Child theme header
├── functions.php                   # Enqueues + breadcrumb + reading-time helpers
├── single.php                      # Redesigned single-post template
├── sidebar.php                     # Wrapper that adds dsd- hooks for styling
└── assets/
    └── css/
        └── blog-single.css         # All single-post styles (scoped to .single-post)
```

## What stays dynamic

- `the_title()`, `the_content()`, `the_author()`, `get_the_date()`,
  `the_post_thumbnail()`, `the_category()`, `the_tags()`.
- Reading time auto-calculated from the post body (`astra_child_reading_time()`).
- Breadcrumb uses Yoast / Rank Math / SEOPress if active, otherwise renders a
  fallback trail.
- Sidebar uses the existing `sidebar-1` widget area — widgets inherit styling
  automatically.
- `comments_template()`, `astra_primary_content_top/bottom`, `astra_page_layout`,
  `post_class`, and Astra schema attributes are all preserved.

## CSS scope

All rules in `assets/css/blog-single.css` are namespaced under `.single-post`
and use a `dsd-` prefix, so the rest of the site keeps the default Astra look.
The stylesheet is enqueued only when `is_singular('post')` is true.

## Reusable content classes

Drop these classes inside the editor (HTML block) to get the same boxes the
reference HTML uses:

- `.dsd-info-box` (blue tinted) — also matches legacy `.info-box`
- `.dsd-warning-box` (amber) — also matches legacy `.warning-box`
- `.dsd-cta-box` (blue gradient CTA) — also matches legacy `.cta-box`

## Testing checklist

- [ ] Single post displays with hero, breadcrumb, category badge, dynamic
      author + date + reading time.
- [ ] Featured image renders below hero (or hero uses it as background).
- [ ] All `h2`–`h4`, `p`, `ul`, `ol`, `blockquote`, `table`, `img`,
      `figure`, `iframe` inside `the_content()` get the design styling.
- [ ] Sidebar widgets show with widget-head + card styling.
- [ ] Yoast / Rank Math / SEOPress breadcrumbs render when active.
- [ ] Schema markup (`itemprop`, `itemtype`) still present — provided by
      Astra primary content hooks.
- [ ] Comments form + list render and inherit base typography.
- [ ] Author box hides itself when the author has no bio.

## Mobile validation checklist

- [ ] ≤ 900 px: sidebar stacks under content, layout is single-column.
- [ ] ≤ 768 px: container padding reduces to 20 px.
- [ ] ≤ 600 px: author box becomes vertical, CTA padding reduces.
- [ ] ≤ 480 px: hero title scales down, body copy reduces to 15 px.
- [ ] No horizontal scrolling at any of the above widths.
- [ ] Tables become horizontally scrollable on narrow viewports.
