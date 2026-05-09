#!/usr/bin/env python3
"""
Custom assembler for the Fantasy Bakery cinematic proposal (v3).

v3 changes (May 2026):
- Hero uses two-beat title (white + gold spans) per panel-taglines.md
- Atmospheric panels render .panel-tag (not .stage-label chip)
- Top-left overlay class with scrim
- Chapter III renders bucketed feature scope (not a flat deliverables list)
- Chapter IV renders inline campaign-example cards before deliverables
- Chapter V renders bifurcated_pricing (Website + WhatsApp split for both setup
  and monthly), not the legacy single-pricing_block
"""

import json
import re
from datetime import date, timedelta
from pathlib import Path

PROJ = Path(__file__).resolve().parent
SKILL = Path("/Users/agency-build/.claude/skills/waterfall-website")
TEMPLATE = SKILL / "assets" / "templates" / "proposal-v4.html"

brief = json.loads((PROJ / "brief.json").read_text())
template = TEMPLATE.read_text()
override_css = (PROJ / "palette-override.css").read_text()

# 1) Extract <head> chrome from v4 template
m = re.search(r"^(.*?</style>\s*</head>)", template, re.DOTALL)
if not m:
    raise SystemExit("ERROR: could not find </style></head> in template")
head_block = m.group(1)

# 2) Customize head
page_title = brief.get("page_title", "Proposal")
head_block = re.sub(r"<title>[^<]+</title>", f"<title>{page_title}</title>", head_block, count=1)
head_block = re.sub(r"<!-- PostHog.*?</script>", "", head_block, count=1, flags=re.DOTALL)

today = date.today().isoformat()
expiry = (date.today() + timedelta(days=14)).isoformat()
head_block = re.sub(r'name="data-published" content="[^"]+"', f'name="data-published" content="{today}"', head_block)
head_block = re.sub(r'name="data-valid-until" content="[^"]+"', f'name="data-valid-until" content="{expiry}"', head_block)

# 3) Append palette override
head_block = head_block.replace(
    "</style>",
    "</style>\n<style>\n/* === Fantasy Bakery palette override === */\n" + override_css + "\n</style>",
    1,
)


def render_hero(panel: dict) -> str:
    """Hero: minimal per skill rule - one-line eyebrow + one two-beat headline.
    No CTA, no signer card, no body copy - the floating WhatsApp button does conversion."""
    h = brief.get("hero", {})
    eyebrow = h.get("eyebrow", "")
    tw = h.get("tagline_white", "")
    tg = h.get("tagline_gold", "")
    inner = (
        f'<div class="eyebrow">{eyebrow}</div>'
        f'<h1 class="hero-h1">{tw}<span class="hero-h1-soft">{tg}</span></h1>'
    )
    idx = panel["id"]
    slug = panel["slug"]
    return (
        f'<section class="block" data-block="{idx}" id="panel-{idx}">'
        f'<div class="video-panel">'
        f'<video autoplay loop muted playsinline preload="auto">'
        f'<source src="assets/mobile-A/panel-{idx}-{slug}-mobile-A.mp4" media="(max-aspect-ratio: 1/1)" type="video/mp4">'
        f'<source src="assets/panel-{idx}-{slug}-loop.mp4" type="video/mp4">'
        f'</video>'
        f'<div class="video-overlay top-left">{inner}</div>'
        f'</div></section>'
    )


# ---- Inline HTML animations (CSS lives in palette-override.css) ----

PIPELINE_HTML = '''<div class="fb-pipe" role="img" aria-label="Order to doorstep flow: order placed, central kitchen, fridge node, delivery partner, doorstep">
  <svg viewBox="0 0 760 90" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <line class="fb-pipe-track" x1="60" y1="45" x2="700" y2="45" />
    <circle class="fb-pipe-halo fb-pipe-halo-1" cx="60" cy="45" r="10" />
    <circle class="fb-pipe-halo fb-pipe-halo-2" cx="220" cy="45" r="10" />
    <circle class="fb-pipe-halo fb-pipe-halo-3" cx="380" cy="45" r="10" />
    <circle class="fb-pipe-halo fb-pipe-halo-4" cx="540" cy="45" r="10" />
    <circle class="fb-pipe-halo fb-pipe-halo-5" cx="700" cy="45" r="10" />
    <circle class="fb-pipe-node" cx="60" cy="45" r="7" />
    <circle class="fb-pipe-node" cx="220" cy="45" r="7" />
    <circle class="fb-pipe-node" cx="380" cy="45" r="7" />
    <circle class="fb-pipe-node" cx="540" cy="45" r="7" />
    <circle class="fb-pipe-node" cx="700" cy="45" r="7" />
    <circle class="fb-pipe-dot" r="5" />
  </svg>
  <div class="fb-pipe-labels">
    <span>Order placed</span>
    <span>Central kitchen</span>
    <span>Fridge node</span>
    <span>Delivery partner</span>
    <span>Doorstep</span>
  </div>
</div>'''

CHAT_HTML = '''<div class="fb-chat" role="img" aria-label="WhatsApp marketing example: inbound question, system typing, broadcast send with confirmation">
  <div class="fb-chat-row left"><div class="fb-chat-bubble fb-chat-in">Cake for Sunday?</div></div>
  <div class="fb-chat-row left"><div class="fb-chat-typing"><span></span><span></span><span></span></div></div>
  <div class="fb-chat-row right"><div class="fb-chat-bubble fb-chat-out">Birthday Week Unicorn collection is open. Reply with the date and the flavour, and we will hold the slot.<div class="fb-chat-attach"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><path d="M14 2H6a2 2 0 00-2 2v16a2 2 0 002 2h12a2 2 0 002-2V8z"/><path d="M14 2v6h6"/></svg>Unicorn-cake.jpg</div></div></div>
  <div class="fb-chat-confirm"><svg width="14" height="14" viewBox="0 0 24 24" style="vertical-align:middle;margin-right:6px;" aria-hidden="true"><polyline class="fb-chat-check" points="4,12 10,18 20,7" fill="none" stroke="currentColor" stroke-width="2.4" stroke-linecap="round" stroke-linejoin="round" /></svg>Sent &middot; 247 customers</div>
</div>'''

COST_HTML = '''<div class="fb-cost" role="img" aria-label="Cost squeeze chart: rent rises from 50,000 to 90,000 rupees per month while cake price stays flat at 500 rupees">
  <svg viewBox="0 0 720 280" xmlns="http://www.w3.org/2000/svg" aria-hidden="true">
    <defs>
      <linearGradient id="fb-cost-fill" x1="0" y1="0" x2="0" y2="1">
        <stop offset="0%" stop-color="#F7B6CD" stop-opacity="0.45"/>
        <stop offset="100%" stop-color="#F7B6CD" stop-opacity="0.05"/>
      </linearGradient>
    </defs>
    <line class="fb-cost-axis" x1="60" y1="240" x2="690" y2="240" />
    <line class="fb-cost-axis" x1="60" y1="40" x2="60" y2="240" />
    <text class="fb-cost-tick" x="60" y="262" text-anchor="middle">Today</text>
    <text class="fb-cost-tick" x="375" y="262" text-anchor="middle">+18 months</text>
    <text class="fb-cost-tick" x="690" y="262" text-anchor="middle">+36 months</text>
    <text class="fb-cost-y" x="50" y="80" text-anchor="end">₹90K</text>
    <text class="fb-cost-y" x="50" y="148" text-anchor="end">₹70K</text>
    <text class="fb-cost-y" x="50" y="216" text-anchor="end">₹50K</text>
    <path class="fb-cost-gap" d="M 60 148 L 690 80 L 690 226 L 60 226 Z" fill="url(#fb-cost-fill)" />
    <path class="fb-cost-rent" d="M 60 148 L 690 80" />
    <text class="fb-cost-label fb-cost-label-rent" x="680" y="62" text-anchor="end">Rent per outlet</text>
    <path class="fb-cost-cake" d="M 60 226 L 690 226" />
    <text class="fb-cost-label fb-cost-label-cake" x="680" y="218" text-anchor="end">Cake price ceiling ~₹500</text>
    <circle class="fb-cost-pulse" cx="375" cy="114" r="6" />
  </svg>
  <div class="fb-cost-caption">The two lines do not meet again. <em>The squeeze is structural, not seasonal.</em></div>
</div>'''

ARCH_HTML = '''<div class="fb-arch" role="img" aria-label="System architecture: customer PWA on top, central kitchen and fridge network and delivery layer in the middle, AI content and admin operations on the right, all connected">
  <div class="fb-arch-grid">
    <div class="fb-arch-node fb-arch-customer">
      <div class="fb-arch-icon">&#127968;</div>
      <div class="fb-arch-label">Customer PWA</div>
      <div class="fb-arch-sub">orders 4 hours ahead</div>
    </div>
    <div class="fb-arch-conn fb-arch-conn-1"></div>
    <div class="fb-arch-core">
      <div class="fb-arch-node fb-arch-kitchen">
        <div class="fb-arch-icon">&#127869;&#65039;</div>
        <div class="fb-arch-label">Central kitchen</div>
        <div class="fb-arch-sub">made after order</div>
      </div>
      <div class="fb-arch-conn fb-arch-conn-2"></div>
      <div class="fb-arch-node fb-arch-fridges">
        <div class="fb-arch-icon">&#10070;&#10070;&#10070;</div>
        <div class="fb-arch-label">Fridge network</div>
        <div class="fb-arch-sub">25-40 nodes across Pune</div>
      </div>
      <div class="fb-arch-conn fb-arch-conn-3"></div>
      <div class="fb-arch-node fb-arch-delivery">
        <div class="fb-arch-icon">&#128692;</div>
        <div class="fb-arch-label">Delivery</div>
        <div class="fb-arch-sub">scheduled rounds</div>
      </div>
    </div>
    <div class="fb-arch-conn fb-arch-conn-4"></div>
    <div class="fb-arch-side">
      <div class="fb-arch-node fb-arch-ai">
        <div class="fb-arch-icon">&#10024;</div>
        <div class="fb-arch-label">AI content</div>
        <div class="fb-arch-sub">photos, captions, festivals</div>
      </div>
      <div class="fb-arch-node fb-arch-admin">
        <div class="fb-arch-icon">&#128202;</div>
        <div class="fb-arch-label">Admin + analytics</div>
        <div class="fb-arch-sub">orders, P&amp;L, freshness logs</div>
      </div>
    </div>
  </div>
</div>'''

IP_HTML = '''<div class="fb-ip">
  <div class="fb-ip-grid">
    <div class="fb-ip-col">
      <div class="fb-ip-icon">&#127874;</div>
      <div class="fb-ip-label">Your data</div>
      <div class="fb-ip-summary">Customer records, orders, conversations, and analytics. <strong>Belongs entirely to Fantasy.</strong> Full export on demand.</div>
    </div>
    <div class="fb-ip-col">
      <div class="fb-ip-icon">&#9881;&#65039;</div>
      <div class="fb-ip-label">Our platform</div>
      <div class="fb-ip-summary">Source code, system prompts, AI instructions, templates, infrastructure. <strong>Licensed to Fantasy.</strong> Tranquil Veda retains IP.</div>
    </div>
    <div class="fb-ip-col">
      <div class="fb-ip-icon">&#128268;</div>
      <div class="fb-ip-label">Third-party services</div>
      <div class="fb-ip-summary">Razorpay, Meta WhatsApp, OpenAI, hosting. <strong>Operate under their own terms.</strong> Liability capped at 3 months of fees.</div>
    </div>
  </div>
</div>'''


def render_animation(name: str) -> str:
    if name == "fb-pipe":
        return PIPELINE_HTML
    if name == "fb-chat":
        return CHAT_HTML
    if name == "fb-cost":
        return COST_HTML
    if name == "fb-arch":
        return ARCH_HTML
    if name == "fb-ip":
        return IP_HTML
    return ""


def render_atmos_panel(panel: dict) -> str:
    idx = panel["id"]
    slug = panel["slug"]
    tag = panel.get("tagline") or {}
    if tag and (tag.get("white") or tag.get("gold")):
        white = tag.get("white", "")
        gold = tag.get("gold", "")
        inner = f'<div class="panel-tag">{white}<span class="em">{gold}</span></div>'
    else:
        # Fallback to stage label if tagline missing
        inner = f'<div class="stage-label">Stage {idx}</div>'
    return (
        f'<section class="block" data-block="{idx}" id="panel-{idx}">'
        f'<div class="video-panel atmos">'
        f'<video autoplay loop muted playsinline preload="auto">'
        f'<source src="assets/mobile-A/panel-{idx}-{slug}-mobile-A.mp4" media="(max-aspect-ratio: 1/1)" type="video/mp4">'
        f'<source src="assets/panel-{idx}-{slug}-loop.mp4" type="video/mp4">'
        f'</video>'
        f'<div class="video-overlay top-left">{inner}</div>'
        f'</div></section>'
    )


def render_closer_panel(panel: dict) -> str:
    idx = panel["id"]
    slug = panel["slug"]
    c = brief.get("closer", {})
    headline_white = c.get("headline_white", c.get("headline", ""))
    headline_gold = c.get("headline_gold", "")
    head_html = f'<h2>{headline_white}'
    if headline_gold:
        head_html += f'<br/><span class="hero-h1-soft">{headline_gold}</span>'
    head_html += '</h2>'

    footer = brief.get("footer", {})
    footer_html = ""
    if footer:
        footer_html = (
            '<div class="footer-meta">'
            f'{footer.get("company_line", "")}<br/>'
            f'{footer.get("links_html", "")}<br/>'
            f'Prepared {today} &middot; Valid until {expiry}'
            "</div>"
        )
    inner = (
        f'{head_html}'
        f'<p class="lede">{c.get("lede", "")}</p>'
        f'<a class="cta" href="{c.get("cta_link", "#")}">{c.get("cta_text", "")} <span class="arrow">&#8594;</span></a>'
        f"{footer_html}"
    )
    return (
        f'<section class="block" data-block="{idx}" id="panel-{idx}">'
        f'<div class="video-panel">'
        f'<video autoplay loop muted playsinline preload="auto">'
        f'<source src="assets/mobile-A/panel-{idx}-{slug}-mobile-A.mp4" media="(max-aspect-ratio: 1/1)" type="video/mp4">'
        f'<source src="assets/panel-{idx}-{slug}-loop.mp4" type="video/mp4">'
        f'</video>'
        f'<div class="video-overlay bottom">{inner}</div>'
        f'</div></section>'
    )


def render_panel(panel: dict) -> str:
    role = panel.get("role", "atmos")
    if role == "hero":
        return render_hero(panel)
    if role == "closer":
        return render_closer_panel(panel)
    return render_atmos_panel(panel)


def render_feature_buckets(buckets: list) -> str:
    total = sum(len(b.get("items", [])) for b in buckets)
    out = [f'<div class="feature-buckets-meta"><span class="feature-buckets-total">{total}</span> features across <span class="feature-buckets-cat-count">{len(buckets)}</span> categories</div>']
    out.append('<div class="feature-buckets">')
    for b in buckets:
        items_count = len(b.get("items", []))
        icon = b.get("icon", "&bull;")
        out.append('<div class="feature-bucket">')
        out.append('<div class="feature-bucket-header">')
        out.append(f'<div class="feature-bucket-icon">{icon}</div>')
        out.append(f'<div class="feature-bucket-name">{b.get("name", "")}</div>')
        out.append(f'<div class="feature-bucket-count">{items_count}</div>')
        out.append("</div>")
        items = "".join(f"<li>{x}</li>" for x in b.get("items", []))
        out.append(f"<ul>{items}</ul>")
        out.append("</div>")
    out.append("</div>")
    return "".join(out)


def render_campaign_examples(examples: list) -> str:
    if not examples:
        return ""
    out = ['<div class="campaign-grid">']
    for ex in examples:
        out.append('<div class="campaign-example">')
        out.append(f'<div class="campaign-title">{ex.get("title", "")}</div>')
        out.append(f'<div class="campaign-angle">{ex.get("angle", "")}</div>')
        out.append(f'<p class="campaign-broadcast">{ex.get("broadcast", "")}</p>')
        out.append("</div>")
    out.append("</div>")
    return "".join(out)


def render_bifurcated_pricing(bp: dict) -> str:
    setup = bp.get("setup", {})
    monthly = bp.get("monthly", {})
    out = []

    # Setup section
    if setup.get("components"):
        out.append('<div class="bifurcated-setup">')
        for c in setup["components"]:
            out.append('<div class="setup-half">')
            out.append(f'<div class="setup-half-label">{c.get("label", "")}</div>')
            out.append(f'<div class="setup-half-amount">{c.get("amount", "")}</div>')
            out.append(f'<div class="setup-half-note">{c.get("note", "")}</div>')
            out.append("</div>")
        out.append("</div>")
    if setup.get("total") or setup.get("payment_terms"):
        out.append('<div class="setup-total-line">')
        if setup.get("total"):
            out.append(f'Total one-time setup: <strong>{setup["total"]}</strong>')
        if setup.get("payment_terms"):
            out.append(f' &middot; {setup["payment_terms"]}')
        out.append('</div>')

    # Monthly section
    if monthly.get("components"):
        out.append('<div class="bifurcated-monthly">')
        for c in monthly["components"]:
            out.append('<div class="monthly-half">')
            out.append(f'<div class="monthly-half-label">{c.get("label", "")}</div>')
            out.append(f'<div class="monthly-half-amount">{c.get("amount", "")}<span class="per">/month</span></div>')
            items = "".join(f"<li>{x}</li>" for x in c.get("items", []))
            out.append(f"<ul>{items}</ul>")
            out.append("</div>")
        out.append("</div>")
    if monthly.get("total"):
        out.append('<div class="monthly-total-line">')
        out.append(f'Total monthly: <strong>{monthly["total"]}/month</strong>')
        if monthly.get("payment_terms"):
            out.append(f' &middot; {monthly["payment_terms"]}')
        out.append('</div>')
    if monthly.get("cta_text"):
        out.append('<div class="monthly-cta-row">')
        out.append(f'<a class="cta" href="{monthly.get("cta_link", "#")}">{monthly["cta_text"]} <span class="arrow">&#8594;</span></a>')
        out.append('</div>')
    if monthly.get("terms_fine"):
        out.append(f'<div class="terms-fine">{monthly["terms_fine"]}</div>')

    return "".join(out)


def render_chapter(chapter: dict) -> str:
    body = chapter.get("body_html", "")
    extras = []

    if chapter.get("feature_buckets"):
        extras.append(render_feature_buckets(chapter["feature_buckets"]))

    if chapter.get("campaign_examples"):
        extras.append(render_campaign_examples(chapter["campaign_examples"]))

    if chapter.get("deliverables"):
        items = "".join(f"<li>{x}</li>" for x in chapter["deliverables"])
        extras.append(f'<ul class="deliverables">{items}</ul>')

    if chapter.get("bifurcated_pricing"):
        extras.append(render_bifurcated_pricing(chapter["bifurcated_pricing"]))

    if chapter.get("animation"):
        extras.append(render_animation(chapter["animation"]))

    if chapter.get("body_after_animation_html"):
        extras.append(chapter["body_after_animation_html"])

    extra_html = "".join(extras)
    anchor = f' id="{chapter["anchor"]}"' if chapter.get("anchor") else ""
    return (
        f'<section class="chapter"{anchor}>'
        f'<div class="chapter-inner">'
        f'<div class="chapter-num">{chapter.get("num", "")}</div>'
        f'<div class="chapter-title">{chapter.get("title", "")}</div>'
        f'<div class="chapter-glyph">- &#11045; -</div>'
        f'<div class="chapter-body">{body}{extra_html}</div>'
        "</div></section>"
    )


# Build body
panels = brief.get("panels", [])
chapters = brief.get("chapters", [])
hero = next((p for p in panels if p.get("role") == "hero"), panels[0] if panels else None)
closer = next((p for p in panels if p.get("role") == "closer"), panels[-1] if panels else None)
mid = [p for p in panels if p.get("role") not in ("hero", "closer")]

blocks = []
if hero:
    blocks.append(render_panel(hero))
for i, ch in enumerate(chapters):
    blocks.append(render_chapter(ch))
    if i < len(mid):
        blocks.append(render_panel(mid[i]))
if closer:
    blocks.append(render_panel(closer))

body_html = "\n\n".join(blocks)

# Floating WhatsApp + minimal expiry script
wa_link = brief.get("whatsapp_link", "https://wa.me/919673758777")
wa_label = brief.get("whatsapp_label", "WhatsApp Shruti")
floating = f'''
<a class="wa-float" href="{wa_link}" aria-label="{wa_label}">
  <svg viewBox="0 0 24 24" fill="currentColor" width="22" height="22"><path d="M17.472 14.382c-.297-.149-1.758-.867-2.03-.967-.272-.099-.47-.149-.669.15-.198.297-.768.967-.941 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.52.149-.174.198-.298.298-.497.099-.198.05-.371-.025-.52-.075-.149-.669-1.612-.916-2.207-.242-.579-.487-.5-.669-.51l-.57-.01c-.198 0-.52.074-.792.372-.272.297-1.04 1.016-1.04 2.479 0 1.462 1.065 2.875 1.213 3.074.149.198 2.096 3.2 5.077 4.487.709.306 1.262.489 1.694.626.712.226 1.36.194 1.871.118.571-.085 1.758-.719 2.006-1.413.248-.694.248-1.289.173-1.413-.074-.124-.272-.198-.57-.347zM12.05 21.785h-.005a9.87 9.87 0 01-5.031-1.378l-.361-.214-3.741.982.998-3.648-.235-.374a9.86 9.86 0 01-1.51-5.26c.001-5.45 4.436-9.884 9.888-9.884a9.825 9.825 0 016.994 2.898 9.821 9.821 0 012.893 6.994c-.003 5.45-4.437 9.884-9.889 9.884zm8.413-18.297A11.815 11.815 0 0012.05 0C5.495 0 .16 5.335.157 11.892c0 2.096.547 4.142 1.588 5.945L.057 24l6.305-1.654a11.882 11.882 0 005.683 1.448h.005c6.554 0 11.89-5.335 11.893-11.893a11.821 11.821 0 00-3.48-8.413z"/></svg>
  {wa_label}
</a>

<script>
  (function() {{
    var pubEl = document.querySelector('meta[name="data-published"]');
    if (!pubEl) return;
    var pub = new Date(pubEl.getAttribute('content'));
    var expiry = new Date(pub.getTime() + 30 * 24 * 60 * 60 * 1000);
    if (new Date() > expiry) {{
      var d = document.createElement('div');
      d.className = 'expired';
      d.innerHTML = '<h2>This proposal has expired</h2><p>This proposal was prepared on ' + pub.toDateString() + ' and has reached its 30-day archival window. Please reach out to Shruti for a refreshed version.</p><a href="{wa_link}">WhatsApp Shruti</a>';
      document.body.appendChild(d);
    }}
  }})();
</script>
'''

html = head_block + "\n<body>\n" + body_html + "\n" + floating + "\n</body>\n</html>"
(PROJ / "index.html").write_text(html)
print(f"OK: assembled index.html ({len(html)} bytes, {len(panels)} panels + {len(chapters)} chapters)")
