#!/usr/bin/env python3
"""
BATCH Elementor Template Generator for Blog Articles
Pixel-perfect CSS isolation + full page preservation
For: 5 blog articles (Poppins + Blue/Gold/Navy color system)
"""
import json
import re
import random
import os
import glob

def uid():
    return format(random.randint(0x1000000, 0xFFFFFFF), '07x')

# CSS_WITH_ISOLATION - Same for all article pages
CSS_WITH_ISOLATION = """
/* Pixel-Perfect CSS Isolation - Blog Articles (Poppins + Blue/Gold/Navy) */
:root {
  --blue: #2b57bd !important;
  --blue-dark: #045cb4 !important;
  --blue-light: #F0F5FA !important;
  --navy: #1e293b !important;
  --text: #334155 !important;
  --muted: #64748b !important;
  --border: #e2e8f0 !important;
  --gold: #f7b500 !important;
  --white: #fff !important;
  --bg: #F8FAFC !important;
  --serif: Georgia, serif !important;
  --sans: 'Poppins', sans-serif !important;
  --radius: 10px !important;
  --shadow: 0 4px 20px rgba(27, 46, 95, .08) !important;
  --container: 1240px !important;
  --ease: cubic-bezier(.4, 0, .2, 1) !important;
}

*,*::before,*::after {
  box-sizing: border-box !important;
  margin: 0 !important;
  padding: 0 !important;
}

html {
  font-size: 16px !important;
  scroll-behavior: smooth !important;
}

body {
  font-family: var(--sans) !important;
  color: var(--text) !important;
  background: var(--white) !important;
  line-height: 1.7 !important;
  -webkit-font-smoothing: antialiased !important;
}

a {
  color: var(--blue) !important;
  text-decoration: none !important;
}

a:hover {
  color: var(--blue-dark) !important;
}

img {
  max-width: 100% !important;
  display: block !important;
}

ul,ol {
  padding-left: 1.5rem !important;
}

/* Container */
.container {
  max-width: var(--container) !important;
  margin: 0 auto !important;
  padding: 0 28px !important;
}

/* Header */
.site-header {
  background: var(--white) !important;
  border-bottom: 1px solid var(--border) !important;
  position: sticky !important;
  top: 0 !important;
  z-index: 100 !important;
  box-shadow: 0 2px 8px rgba(0, 0, 0, .05) !important;
}

.header-inner {
  display: flex !important;
  align-items: center !important;
  justify-content: space-between !important;
  height: 70px !important;
}

.logo {
  display: flex !important;
  align-items: center !important;
  gap: 11px !important;
}

.logo-mark {
  width: 42px !important;
  height: 42px !important;
  background: var(--blue) !important;
  border-radius: 9px !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #fff !important;
  font-size: 20px !important;
  flex-shrink: 0 !important;
}

.logo-name {
  font-size: 15px !important;
  font-weight: 700 !important;
  color: var(--navy) !important;
  line-height: 1.15 !important;
}

.logo-sub {
  font-size: 10px !important;
  color: var(--muted) !important;
  font-weight: 500 !important;
  letter-spacing: .04em !important;
}

.header-cta {
  display: flex !important;
  align-items: center !important;
  gap: 12px !important;
}

.btn {
  display: inline-flex !important;
  align-items: center !important;
  gap: 7px !important;
  padding: 10px 22px !important;
  border-radius: 99px !important;
  font-size: 14px !important;
  font-weight: 600 !important;
  font-family: var(--sans) !important;
  border: none !important;
  cursor: pointer !important;
  transition: all .2s var(--ease) !important;
}

.btn-primary {
  background: var(--blue) !important;
  color: #fff !important;
  box-shadow: 0 4px 14px rgba(43, 87, 189, .3) !important;
}

.btn-primary:hover {
  background: var(--blue-dark) !important;
  transform: translateY(-1px) !important;
  color: #fff !important;
}

.btn-outline {
  background: transparent !important;
  border: 2px solid var(--blue) !important;
  color: var(--blue) !important;
}

.btn-outline:hover {
  background: var(--blue) !important;
  color: #fff !important;
}

/* Breadcrumb */
.breadcrumb {
  padding: 14px 0 !important;
  font-size: 13px !important;
  color: var(--muted) !important;
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
}

.breadcrumb a {
  color: var(--muted) !important;
}

.breadcrumb a:hover {
  color: var(--blue) !important;
}

.breadcrumb span {
  color: var(--text) !important;
}

/* Article Hero */
.article-hero {
  background: linear-gradient(135deg, var(--navy) 0%, #1a3a7a 60%, #1a5b9a 100%) !important;
  padding: 52px 0 60px !important;
  position: relative !important;
  overflow: hidden !important;
}

.article-hero::after {
  content: '' !important;
  position: absolute !important;
  bottom: -1px !important;
  left: 0 !important;
  right: 0 !important;
  height: 50px !important;
  background: var(--white) !important;
  clip-path: ellipse(55% 100% at 50% 100%) !important;
}

.article-hero::before {
  content: '' !important;
  position: absolute !important;
  inset: 0 !important;
  background: radial-gradient(ellipse at 80% 20%, rgba(43, 87, 189, .25), transparent 55%) !important;
}

.hero-inner {
  position: relative !important;
  z-index: 1 !important;
  max-width: 860px !important;
}

.category-badge {
  display: inline-flex !important;
  align-items: center !important;
  gap: 7px !important;
  background: rgba(255, 255, 255, .12) !important;
  border: 1px solid rgba(255, 255, 255, .25) !important;
  border-radius: 99px !important;
  padding: 5px 15px !important;
  font-size: 11px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .1em !important;
  color: rgba(255, 255, 255, .9) !important;
  margin-bottom: 18px !important;
}

.article-title {
  font-size: clamp(26px, 4vw, 44px) !important;
  font-weight: 700 !important;
  line-height: 1.2 !important;
  color: #fff !important;
  margin-bottom: 18px !important;
  letter-spacing: -.01em !important;
}

.article-meta {
  display: flex !important;
  flex-wrap: wrap !important;
  align-items: center !important;
  gap: 16px !important;
  margin-bottom: 0 !important;
}

.meta-item {
  display: flex !important;
  align-items: center !important;
  gap: 6px !important;
  font-size: 13px !important;
  color: rgba(255, 255, 255, .7) !important;
  font-weight: 500 !important;
}

.meta-dot {
  width: 4px !important;
  height: 4px !important;
  border-radius: 50% !important;
  background: rgba(255, 255, 255, .35) !important;
}

/* Layout */
.content-wrap {
  display: grid !important;
  grid-template-columns: minmax(0, 1fr) 300px !important;
  gap: 44px !important;
  padding: 52px 0 80px !important;
  align-items: start !important;
}

.article-body {
  min-width: 0 !important;
}

.sidebar {
  position: sticky !important;
  top: 90px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 22px !important;
}

/* Article Body */
.article-body h2 {
  font-size: clamp(19px, 2.5vw, 25px) !important;
  font-weight: 700 !important;
  color: var(--navy) !important;
  margin: 40px 0 14px !important;
  line-height: 1.25 !important;
  padding-bottom: 10px !important;
  border-bottom: 2px solid var(--blue-light) !important;
}

.article-body h3 {
  font-size: 18px !important;
  font-weight: 600 !important;
  color: var(--navy) !important;
  margin: 30px 0 11px !important;
}

.article-body p {
  margin-bottom: 18px !important;
  font-size: 16px !important;
  line-height: 1.8 !important;
  color: var(--text) !important;
}

.article-body ul,
.article-body ol {
  margin-bottom: 18px !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 7px !important;
}

.article-body li {
  font-size: 15.5px !important;
  line-height: 1.7 !important;
  color: var(--text) !important;
}

.article-body strong {
  color: var(--navy) !important;
  font-weight: 600 !important;
}

.article-body blockquote {
  margin: 28px 0 !important;
  padding: 20px 24px !important;
  background: var(--blue-light) !important;
  border-left: 4px solid var(--blue) !important;
  border-radius: 0 var(--radius) var(--radius) 0 !important;
  font-size: 15.5px !important;
  line-height: 1.7 !important;
  color: var(--navy) !important;
  font-style: italic !important;
}

/* Info box */
.info-box {
  background: var(--blue-light) !important;
  border: 1px solid #c7d9f7 !important;
  border-radius: var(--radius) !important;
  padding: 20px 22px !important;
  margin: 28px 0 !important;
}

.info-box-title {
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .07em !important;
  color: var(--blue) !important;
  margin-bottom: 10px !important;
  display: flex !important;
  align-items: center !important;
  gap: 7px !important;
}

.warning-box {
  background: #fff8ed !important;
  border: 1px solid #f7d98a !important;
  border-radius: var(--radius) !important;
  padding: 20px 22px !important;
  margin: 28px 0 !important;
}

.warning-box-title {
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .07em !important;
  color: #b45309 !important;
  margin-bottom: 10px !important;
  display: flex !important;
  align-items: center !important;
  gap: 7px !important;
}

/* Table */
.table-wrap {
  overflow-x: auto !important;
  margin: 28px 0 !important;
}

table {
  width: 100% !important;
  border-collapse: collapse !important;
  font-size: 14px !important;
}

th {
  background: var(--navy) !important;
  color: #fff !important;
  padding: 11px 14px !important;
  text-align: left !important;
  font-weight: 600 !important;
  font-size: 13px !important;
}

td {
  padding: 10px 14px !important;
  border-bottom: 1px solid var(--border) !important;
  color: var(--text) !important;
}

tr:nth-child(even) td {
  background: var(--bg) !important;
}

/* CTA Box */
.cta-box {
  background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 100%) !important;
  border-radius: 14px !important;
  padding: 28px !important;
  color: #fff !important;
  margin: 40px 0 !important;
}

.cta-box h3 {
  font-size: 18px !important;
  font-weight: 700 !important;
  margin-bottom: 10px !important;
  color: #fff !important;
}

.cta-box p {
  font-size: 14.5px !important;
  line-height: 1.65 !important;
  color: rgba(255, 255, 255, .85) !important;
  margin-bottom: 20px !important;
}

.cta-box .btn-white {
  background: #fff !important;
  color: var(--blue) !important;
  font-weight: 700 !important;
}

.cta-box .btn-white:hover {
  background: #f0f5ff !important;
  color: var(--blue-dark) !important;
}

.cta-meta {
  display: flex !important;
  gap: 18px !important;
  flex-wrap: wrap !important;
  margin-top: 14px !important;
}

.cta-meta span {
  font-size: 13px !important;
  color: rgba(255, 255, 255, .75) !important;
  display: flex !important;
  align-items: center !important;
  gap: 5px !important;
}

/* Author box */
.author-box {
  background: var(--bg) !important;
  border: 1px solid var(--border) !important;
  border-radius: 14px !important;
  padding: 24px !important;
  display: flex !important;
  gap: 20px !important;
  align-items: flex-start !important;
  margin-top: 44px !important;
}

.author-avatar {
  width: 64px !important;
  height: 64px !important;
  border-radius: 50% !important;
  background: linear-gradient(135deg, var(--blue), #1a5b9a) !important;
  display: flex !important;
  align-items: center !important;
  justify-content: center !important;
  color: #fff !important;
  font-size: 22px !important;
  flex-shrink: 0 !important;
}

.author-name {
  font-size: 16px !important;
  font-weight: 700 !important;
  color: var(--navy) !important;
  margin-bottom: 3px !important;
}

.author-creds {
  font-size: 12px !important;
  color: var(--blue) !important;
  font-weight: 600 !important;
  margin-bottom: 9px !important;
  letter-spacing: .02em !important;
}

.author-bio {
  font-size: 13.5px !important;
  line-height: 1.65 !important;
  color: var(--text) !important;
}

/* Sidebar widgets */
.widget {
  background: var(--white) !important;
  border: 1px solid var(--border) !important;
  border-radius: var(--radius) !important;
  overflow: hidden !important;
}

.widget-head {
  background: var(--navy) !important;
  color: #fff !important;
  padding: 13px 18px !important;
  font-size: 13px !important;
  font-weight: 700 !important;
  text-transform: uppercase !important;
  letter-spacing: .07em !important;
}

.widget-body {
  padding: 18px !important;
}

.widget-body p {
  font-size: 13.5px !important;
  color: var(--text) !important;
  line-height: 1.65 !important;
  margin-bottom: 12px !important;
}

.quick-facts {
  list-style: none !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 9px !important;
}

.quick-facts li {
  display: flex !important;
  gap: 9px !important;
  font-size: 13px !important;
  color: var(--text) !important;
  line-height: 1.5 !important;
}

.quick-facts li::before {
  content: '✓' !important;
  color: var(--blue) !important;
  font-weight: 700 !important;
  flex-shrink: 0 !important;
}

.related-list {
  list-style: none !important;
  padding: 0 !important;
  display: flex !important;
  flex-direction: column !important;
  gap: 0 !important;
}

.related-list a {
  display: block !important;
  padding: 11px 0 !important;
  font-size: 13px !important;
  color: var(--text) !important;
  border-bottom: 1px solid var(--border) !important;
  line-height: 1.45 !important;
  transition: color .2s !important;
}

.related-list a:hover {
  color: var(--blue) !important;
}

.related-list li:last-child a {
  border-bottom: none !important;
}

.contact-widget {
  background: var(--navy) !important;
}

.contact-widget .widget-body {
  color: #fff !important;
  text-align: center !important;
}

.contact-widget .widget-body p {
  color: rgba(255, 255, 255, .8) !important;
}

.contact-num {
  font-size: 20px !important;
  font-weight: 700 !important;
  color: var(--gold) !important;
  letter-spacing: .02em !important;
  margin: 8px 0 !important;
}

.contact-hours {
  font-size: 12px !important;
  color: rgba(255, 255, 255, .6) !important;
  margin-bottom: 16px !important;
  line-height: 1.6 !important;
}

/* Footer */
.site-footer {
  background: var(--navy) !important;
  color: rgba(255, 255, 255, .6) !important;
  text-align: center !important;
  padding: 22px !important;
  font-size: 13px !important;
}

.site-footer a {
  color: rgba(255, 255, 255, .6) !important;
}

/* Responsive */
@media (max-width: 900px) {
  .content-wrap {
    grid-template-columns: 1fr !important;
  }
  .sidebar {
    position: static !important;
  }
}

@media (max-width: 600px) {
  .container {
    padding: 0 16px !important;
  }
  .header-cta .btn-outline {
    display: none !important;
  }
  .article-hero {
    padding: 38px 0 48px !important;
  }
  .cta-box {
    padding: 22px !important;
  }
  .author-box {
    flex-direction: column !important;
  }
}
"""

def process_article(html_file):
    """Process a single article HTML file and generate Elementor JSON"""

    with open(html_file, 'r', encoding='utf-8') as f:
        html_content = f.read()

    # Get article title from filename for output naming
    base_name = os.path.basename(html_file).replace('.html', '')

    # Extract the full body content (everything between <body> and </body>)
    body_match = re.search(r'<body>(.*?)</body>', html_content, re.DOTALL)
    if not body_match:
        print(f"❌ Could not extract body from {html_file}")
        return False

    full_article_html = body_match.group(1).strip()

    # Inject CSS at the beginning
    full_with_css = f'<style id="article-styles" data-scope="pixel-perfect">{CSS_WITH_ISOLATION}</style>\n{full_article_html}'

    def make_section(bg_color, html_widget_content, padding_top="0", padding_bottom="0"):
        return {
            "id": uid(),
            "elType": "section",
            "isInner": False,
            "settings": {
                "stretch_section": "section-stretched",
                "layout": "full_width",
                "content_width": {"unit": "px", "size": 1240, "sizes": []},
                "gap": "no",
                "padding": {
                    "unit": "px",
                    "top": padding_top,
                    "right": "0",
                    "bottom": padding_bottom,
                    "left": "0",
                    "isLinked": False
                },
                "background_background": "classic",
                "background_color": bg_color if bg_color else "transparent",
                "background_overlay": "no"
            },
            "elements": [{
                "id": uid(),
                "elType": "column",
                "isInner": False,
                "settings": {
                    "_column_size": 100,
                    "_inline_size": None,
                    "padding": {"unit": "px", "top": "0", "right": "0", "bottom": "0", "left": "0", "isLinked": True}
                },
                "elements": [{
                    "id": uid(),
                    "elType": "widget",
                    "widgetType": "html",
                    "settings": {
                        "html": html_widget_content
                    }
                }]
            }]
        }

    # Build template
    template = {
        "version": "0.4",
        "title": f"Blog Article – {base_name.replace('-', ' ').title()} (Pixel-Perfect)",
        "type": "page",
        "content": [
            make_section("transparent", full_with_css, "0", "0"),
        ],
        "page_settings": {
            "custom_css": "/* Pixel-Perfect Override */\n.elementor-widget-html { overflow: visible !important; }"
        }
    }

    # Write output
    output_file = os.path.join(os.path.dirname(html_file), f"elementor-{base_name}.json")
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(template, f, ensure_ascii=False, indent=2)

    size_kb = len(json.dumps(template, ensure_ascii=False)) / 1024
    print(f"✅ {base_name}: {size_kb:.1f} KB")
    return True

# Process all article HTML files
html_files = sorted(glob.glob("/home/claude/repo/blog-articles/article-*.html"))
success_count = 0

print("🚀 Processing 5 blog articles...\n")
for html_file in html_files:
    if process_article(html_file):
        success_count += 1

print(f"\n✨ Successfully converted {success_count}/5 articles")
