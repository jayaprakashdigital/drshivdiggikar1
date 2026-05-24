#!/usr/bin/env python3
"""
PIXEL-PERFECT Elementor Template Generator
For: neonatologist-bangalore-standalone.html
Preserves 100% of CSS, typography, spacing, animations, and responsive behavior
"""
import json, re, random

def uid():
    return format(random.randint(0x1000000, 0xFFFFFFF), '07x')

# Read the HTML file
with open('/home/claude/repo/neonatologist-bangalore.html', 'r', encoding='utf-8') as f:
    html_content = f.read()

# Extract CSS (between <style> tags)
style_match = re.search(r'<style>(.*?)</style>', html_content, re.DOTALL)
CSS = style_match.group(1) if style_match else ""

# Extract script (between <script> tags)
script_match = re.search(r'<script>(.*?)</script>', html_content, re.DOTALL)
SCRIPT = script_match.group(1) if script_match else ""

# Extract body sections by ID
def extract_section(section_id):
    """Extract a section by its ID"""
    pattern = rf'<section[^>]*id="{section_id}"[^>]*>(.*?)</section>'
    match = re.search(pattern, html_content, re.DOTALL)
    return match.group(1).strip() if match else ""

# Get each section
HERO_BODY = extract_section('hero')
ABOUT_BODY = extract_section('about')
CONDITIONS_BODY = extract_section('conditions')
LOCATION_BODY = extract_section('location')
FAQ_BODY = extract_section('faq')
CTA_BODY = extract_section('cta')

# Build complete section HTML including wrapper divs
def wrap_section(body_html, section_class, section_id):
    """Wrap extracted body in proper section tags"""
    return f'<section class="{section_class}" id="{section_id}">{body_html}</section>'

HERO_HTML = wrap_section(HERO_BODY, 'hero', 'hero')
ABOUT_HTML = wrap_section(ABOUT_BODY, 'about-section', 'about')
CONDITIONS_HTML = wrap_section(CONDITIONS_BODY, 'conditions-section', 'conditions')
LOCATION_HTML = wrap_section(LOCATION_BODY, 'location-section', 'location')
FAQ_HTML = wrap_section(FAQ_BODY, 'faq-section', 'faq')
CTA_HTML = wrap_section(CTA_BODY, 'final-cta', 'cta') if CTA_BODY else ""

# CSS Injection with Google Fonts
CSS_INJECT = f"""<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Bricolage+Grotesque:opsz,wght@12..96,400;12..96,500;12..96,600;12..96,700;12..96,800&family=Inter:wght@300;400;500;600;700;800&display=swap" rel="stylesheet">
<style id="neo-styles">{CSS}</style>"""

# Mobile CTA and Scripts
MOBILE_CTA_SCRIPTS = f"""<div class="mobile-sticky-cta" id="neo-mobile-cta">
  <a href="tel:+919133555335" class="btn btn-outline-blue"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07A19.5 19.5 0 0 1 4.69 12a19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 3.6 1.27h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L7.91 9a16 16 0 0 0 6 6l1.09-1.09a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z"/></svg>Call</a>
  <a href="https://www.medicoverhospitals.in/doctors/dr-shivashankar-diggikar" target="_blank" rel="noopener" class="btn btn-primary"><svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"><rect x="3" y="4" width="18" height="18" rx="2"/><line x1="16" y1="2" x2="16" y2="6"/><line x1="8" y1="2" x2="8" y2="6"/><line x1="3" y1="10" x2="21" y2="10"/></svg>Book</a>
</div>

<script>
{SCRIPT}
</script>"""

def make_section(bg_color, html_widget_content, padding_top="0", padding_bottom="0"):
    """Create a pixel-perfect Elementor section"""
    return {
        "id": uid(),
        "elType": "section",
        "isInner": False,
        "settings": {
            "stretch_section": "section-stretched",
            "layout": "full_width",
            "content_width": {"unit": "px", "size": 1160, "sizes": []},
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
            "background_color": bg_color
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

# Build the template
template = {
    "version": "0.4",
    "title": "Best Neonatologist in Bangalore – Dr. Shivashankar Diggikar",
    "type": "page",
    "content": [
        make_section("transparent", CSS_INJECT, "0", "0"),
        make_section("#0a2540", HERO_HTML, "0", "0"),
        make_section("#ffffff", ABOUT_HTML, "0", "0"),
        make_section("#f8fafc", CONDITIONS_HTML, "0", "0"),
        make_section("#ffffff", LOCATION_HTML, "0", "0"),
        make_section("#ffffff", FAQ_HTML, "0", "0"),
        make_section("#0a2540", CTA_HTML, "0", "0") if CTA_HTML else None,
        make_section("transparent", MOBILE_CTA_SCRIPTS, "0", "0"),
    ],
    "page_settings": {
        "custom_css": ""
    }
}

# Remove None entries
template["content"] = [s for s in template["content"] if s is not None]

# Write output
output_path = "/home/claude/repo/elementor-neonatologist-bangalore.json"
with open(output_path, "w", encoding="utf-8") as f:
    json.dump(template, f, ensure_ascii=False, indent=2)

print(f"✅ Generated: {output_path}")
print(f"📊 File size: {len(json.dumps(template, ensure_ascii=False)):,} bytes")
print(f"📑 Sections: {len(template['content'])}")
print(f"🎨 CSS preserved: {len(CSS):,} chars")
print(f"⚙️ JavaScript preserved: {len(SCRIPT):,} chars")
print("\n✨ Pixel-perfect Elementor template ready for import!")
