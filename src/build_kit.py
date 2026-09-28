# Builds the Sketchbook kit into ../kit from the agreed style (see ../README.md).
# Run: python3 src/build_kit.py
import html, json, os, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import characters as gc

KIT = os.path.join(HERE, "..", "kit")
URL = "https://lean-software-production.github.io/brand/kit/"  # where GitHub Pages publishes kit/
for d in ("", "icons", "characters"):
    os.makedirs(os.path.join(KIT, d), exist_ok=True)

# ---------------------------------------------------------------- tokens
TOKENS = {
    "color": {
        "mustard": "#EEA306", "teal": "#039695", "forest": "#4A7D4B", "coral": "#F76C37", "blue": "#1F78A8",
        "slate": "#36545C", "rust": "#D6631C", "deep-teal": "#094854",
        "highlighter": "#FFEEB8", "paper": "#FCF9F3", "ribbon": "#FAEED3", "bubble": "#EEF4F5",
        "ink": "#2A2724", "ink-title": "#1B1B1B", "body-text": "#3A3631",
    },
    "font": {
        "title": "'Luckiest Guy', 'Patrick Hand SC', cursive",
        "label": "'Patrick Hand SC', 'Patrick Hand', cursive",
        "body": "'Patrick Hand', 'Comic Sans MS', cursive",
    },
    "line": {"thin": "3px", "chunky": "5px"},
    "wobble": {
        "thin":   {"baseFrequency": 0.035, "scale": 3.5, "use": "bubbles, panels, arrows, doodles"},
        "chunky": {"baseFrequency": 0.04,  "scale": 4.5, "use": "character outlines (~5px)"},
        "soft":   {"baseFrequency": 0.02,  "scale": 5.5,   "use": "highlighter swashes, big loop arrows"},
    },
}
C = TOKENS["color"]
# What each colour and font is for. Shown in the gallery and published in index.json.
COLOUR_ABOUT = {
    "mustard": "Step colour 1. Panels, icon washes, warm accents.",
    "teal": "Step colour 2. Panels, icon washes.",
    "forest": "Step colour 3. Panels, icon washes.",
    "coral": "Step colour 4. Panels, icon washes.",
    "blue": "Step colour 5. Panels, icon washes, the loop-back arrow.",
    "slate": "Connector arrows between steps.",
    "rust": "Accent text in speech bubbles, and ribbon kickers.",
    "deep-teal": "Section headings and their rules.",
    "highlighter": "The swash behind big titles.",
    "paper": "The page background.",
    "ribbon": "Ribbon banner fill.",
    "bubble": "Speech bubble fill.",
    "ink": "Outlines and line drawing.",
    "ink-title": "Big title lettering.",
    "body-text": "Sentences and captions.",
}
FONT_ABOUT = {
    "title": ("Luckiest Guy", "Big titles only, always in capitals."),
    "label": ("Patrick Hand SC", "Step labels and section headings."),
    "body": ("Patrick Hand", "Sentences and captions."),
}
assert set(COLOUR_ABOUT) == set(C) and set(FONT_ABOUT) == set(TOKENS["font"]), "every colour and font needs a line in COLOUR_ABOUT / FONT_ABOUT"
INK = C["ink"]

# ------------------------------------------------ colour mixing, as CSS color-mix(in oklab) does it
# Used only where a mix has to be baked into a data-URI image (the ribbon tails). Pages mix
# with color-mix() instead.
def _lin(c): return c / 12.92 if c <= 0.04045 else ((c + 0.055) / 1.055) ** 2.4
def _delin(c): return 12.92 * c if c <= 0.0031308 else 1.055 * c ** (1 / 2.4) - 0.055
def _oklab(hexc):
    r, g, b = (_lin(int(hexc[i:i + 2], 16) / 255) for i in (1, 3, 5))
    l, m, s = ((0.4122214708 * r + 0.5363325363 * g + 0.0514459929 * b) ** (1 / 3),
               (0.2119034982 * r + 0.6806995451 * g + 0.1073969566 * b) ** (1 / 3),
               (0.0883024619 * r + 0.2817188376 * g + 0.6299787005 * b) ** (1 / 3))
    return (0.2104542553 * l + 0.7936177850 * m - 0.0040720468 * s,
            1.9779984951 * l - 2.4285922050 * m + 0.4505937099 * s,
            0.0259040371 * l + 0.7827717662 * m - 0.8086757660 * s)
def _hex(L, a, b):
    l, m, s = ((L + 0.3963377774 * a + 0.2158037573 * b) ** 3, (L - 0.1055613458 * a - 0.0638541728 * b) ** 3,
               (L - 0.0894841775 * a - 1.2914855480 * b) ** 3)
    rgb = (4.0767416621 * l - 3.3077115913 * m + 0.2309699292 * s, -1.2684380046 * l + 2.6097574011 * m - 0.3413193965 * s,
           -0.0041960863 * l - 0.7034186147 * m + 1.7076147010 * s)
    return "#" + "".join(f"{round(min(1, max(0, _delin(v))) * 255):02X}" for v in rgb)
def mix(c1, share, c2):
    """color-mix(in oklab, c1 <share>, c2), share as 0..1."""
    return _hex(*(x * share + y * (1 - share) for x, y in zip(_oklab(c1), _oklab(c2))))

# ------------------------------------------------ roles: what the pieces paint with
# Each role is a CSS value that points at palette colours or mixes them; there are no new
# colours. The brand is light mode only (README.md): a paper page with ink text.
ROLES = {
    "page": ("var(--sk-paper)", "The page behind everything."),
    "text": ("var(--sk-body-text)", "Sentences and captions."),
    "title-text": ("var(--sk-ink-title)", "Big title lettering and its burst ticks."),
    "line": ("var(--sk-ink)", "Outlines of bubbles and secondary buttons."),
    "heading": ("var(--sk-deep-teal)", "Section headings and their rules, primary buttons."),
    "on-heading": ("var(--sk-paper)", "Text on a primary button."),
    "connector": ("var(--sk-slate)", "Connector arrows between steps."),
    "loop": ("var(--sk-blue)", "The loop-back arrow."),
    "bubble-fill": ("var(--sk-bubble)", "Speech bubble fill."),
    "swash": ("var(--sk-highlighter)", "What the highlighter swash reads as: a solid colour for tints and contrast checks."),
    "track": ("color-mix(in oklab, var(--sk-ink) 12%, var(--sk-paper))", "The empty part of a progress meter."),
    # Palette colours as text: mixed with ink until they reach 4.5:1 on paper.
    "mustard-text": ("color-mix(in oklch, var(--sk-mustard) 55%, var(--sk-ink))", "Mustard that reads as text."),
    "teal-text": ("color-mix(in oklch, var(--sk-teal) 70%, var(--sk-ink))", "Teal that reads as text."),
    "forest-text": ("color-mix(in oklch, var(--sk-forest) 85%, var(--sk-ink))", "Forest that reads as text. Ticks."),
    "coral-text": ("color-mix(in oklch, var(--sk-coral) 55%, var(--sk-ink))", "Coral that reads as text."),
    "blue-text": ("color-mix(in oklch, var(--sk-blue) 85%, var(--sk-ink))", "Blue that reads as text."),
    "rust-text": ("color-mix(in oklch, var(--sk-rust) 70%, var(--sk-ink))", "Rust that reads as text: bubble accents, ribbon kickers."),
    "deep-teal-text": ("var(--sk-deep-teal)", "Deep teal that reads as text."),
}

def svg_uri(svg):
    return 'url("data:image/svg+xml,' + quote(svg, safe="") + '")'

def filt(fid, freq, scale, region="-20 -20 2000 2000", blur=None):
    x, y, w, h = region.split()
    extra = f'<feGaussianBlur stdDeviation="{blur}"/>' if blur else ""
    return (f'<filter id="{fid}" filterUnits="userSpaceOnUse" x="{x}" y="{y}" width="{w}" height="{h}">'
            f'<feTurbulence type="fractalNoise" baseFrequency="{freq}" numOctaves="2" seed="3"/>'
            f'<feDisplacementMap in="SourceGraphic" scale="{scale}"/>{extra}</filter>')

WASH = ('<filter id="sk-wash" filterUnits="userSpaceOnUse" x="-50" y="-50" width="2000" height="2000">'
        '<feTurbulence type="fractalNoise" baseFrequency="0.06" numOctaves="3" seed="11" result="n"/>'
        '<feDisplacementMap in="SourceGraphic" in2="n" scale="8" result="d"/><feGaussianBlur in="d" stdDeviation="1.2"/></filter>')

# ------------------------------------------------ page-level filter defs (for CSS chunks)
# CSS chunks use filter:url(#sk-...) on pseudo-elements; sketchbook.js injects these once per page.
PAGE_DEFS = ('<svg id="sk-defs" width="0" height="0" style="position:absolute" aria-hidden="true"><defs>'
             '<filter id="sk-wobble" x="-5%" y="-5%" width="110%" height="110%"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.5"/></filter>'
             '<filter id="sk-wobble-soft" x="-5%" y="-10%" width="110%" height="120%"><feTurbulence type="fractalNoise" baseFrequency="0.02" numOctaves="2" seed="8"/><feDisplacementMap in="SourceGraphic" scale="5.5"/></filter>'
             '<filter id="sk-wobble-line" filterUnits="userSpaceOnUse" x="-100" y="-100" width="3000" height="3000"><feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.5"/></filter>'
             '<marker id="sk-head" viewBox="0 0 10 10" refX="7" refY="5" markerWidth="5" markerHeight="5" orient="auto-start-reverse"><path d="M1 1 L8 5 L1 9" fill="none" stroke="context-stroke" stroke-width="2.2" stroke-linecap="round" stroke-linejoin="round"/></marker>'
             '</defs></svg>')
open(os.path.join(KIT, "sketchbook.js"), "w").write(
    "// Sketchbook kit: injects the shared wobble filters once per page. Include with <script src=\"sketchbook.js\" defer></script>\n"
    "(function(){\n  var defs = " + json.dumps(PAGE_DEFS) + ";\n"
    "  function go(){ if(!document.getElementById('sk-defs')) document.body.insertAdjacentHTML('afterbegin', defs); }\n"
    "  if (document.body) go(); else document.addEventListener('DOMContentLoaded', go);\n})();\n")

# ------------------------------------------------ small data-URI images used by the CSS
# Single-colour shapes are masks: the page paints them with a role colour (background-color).
# Only two images keep their colours inside: the highlighter swash and the ribbon tails
# (two colours each).
swash = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" preserveAspectRatio="none"><defs>'
         + filt("f", 0.02, 7, "-20 -20 440 140") + '</defs>'
         f'<path filter="url(#f)" fill="{C["highlighter"]}" d="M10 16 C 120 4, 280 6, 392 14 L 394 84 C 280 96, 120 94, 6 88 Z"/></svg>')
ticks_l = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 100"><defs>' + filt("f", 0.035, 3.5, "-10 -10 80 120") + '</defs>'
           '<g filter="url(#f)" stroke="#000" stroke-width="7" stroke-linecap="round">'
           '<line x1="14" y1="14" x2="46" y2="34"/><line x1="6" y1="52" x2="50" y2="54"/><line x1="14" y1="92" x2="46" y2="74"/></g></svg>')
ticks_r = ticks_l.replace('<g filter', '<g transform="translate(60 0) scale(-1 1)"><g filter').replace('</g></svg>', '</g></g></svg>')
rule = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 10" preserveAspectRatio="none">'
        '<path d="M2 5 C 100 3, 300 7, 398 5" stroke="#000" stroke-width="3" fill="none" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')
# A hand-drawn tick: a short stroke down, then a long curving one up and to the right.
tick = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs>' + filt("f", 0.035, 3.5, "-10 -10 120 120") + '</defs>'
        '<path filter="url(#f)" d="M12 58 C 22 61, 31 70, 39 84 C 50 58, 66 34, 89 13" fill="none" stroke="#000" '
        'stroke-width="14" stroke-linecap="round" stroke-linejoin="round"/></svg>')
# Ribbon tails: the ribbon's cream with a little mustard and ink, so the fold reads as its underside.
TAIL = mix(mix(C["ribbon"], .8, C["mustard"]), .97, INK)
end_l = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 92 92"><defs>' + filt("f", 0.02, 6, "-10 -10 112 112") + '</defs>'
         f'<path filter="url(#f)" d="M40 12 L 3 40 L 40 66 L 24 82 L 90 82 L 90 12 Z" fill="{TAIL}" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/></svg>')
end_r = end_l.replace('<path filter', '<g transform="translate(92 0) scale(-1 1)"><path filter').replace('/></svg>', '/></g></svg>')
grain = ('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2"/>'
         '<feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.05 0"/></filter><rect width="300" height="300" filter="url(#g)"/></svg>')

def mask(uri, rest):
    return f"-webkit-mask: {uri} {rest}; mask: {uri} {rest};"

# ------------------------------------------------ sketchbook.css
F = TOKENS["font"]
roles = "\n".join(f"  --sk-{k}: {v};" for k, (v, _) in ROLES.items())
# (colour, numeral colour on its badge). White numerals only where they reach 4.5:1.
ACCENTS = [("mustard", "var(--sk-ink-title)"), ("teal", "var(--sk-ink-title)"), ("forest", "#fff"), ("coral", "var(--sk-ink-title)"),
           ("blue", "#fff"), ("rust", "var(--sk-ink-title)"), ("deep-teal", "#fff")]
modifiers = "\n".join(f".sk-{c} {{ --sk-accent: var(--sk-{c}); --sk-accent-text: var(--sk-{c}-text); --sk-on-accent: {on}; }}" for c, on in ACCENTS)
css = f"""/* Sketchbook kit: tokens + reusable chunks. Spec: README.md. Also include sketchbook.js (wobble filters). */
@import url("https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Patrick+Hand&family=Patrick+Hand+SC&display=swap");

/* Palette and fonts. The roles below point at them. */
:root {{
{chr(10).join(f"  --sk-{k}: {v};" for k, v in C.items())}
  --sk-font-title: {F["title"]};
  --sk-font-label: {F["label"]};
  --sk-font-body: {F["body"]};
  --sk-line-thin: 3px;
  --sk-line-chunky: 5px;
}}

/* Roles: what the pieces paint with. */
:root {{
{roles}
  --sk-accent: var(--sk-teal); --sk-accent-text: var(--sk-teal-text); --sk-on-accent: var(--sk-ink-title);
}}

/* ---------- colour modifiers: add to any chunk that uses an accent ----------
   Each sets the accent (outlines, badges, washes), a version of it that reads as text,
   and the numeral colour for a badge filled with it. */
{modifiers}

/* ---------- paper: a 16:9 slide, or any paper-backed block ---------- */
.sk-paper {{
  background: {svg_uri(grain)}, var(--sk-page);
  color: var(--sk-text);
  font-family: var(--sk-font-body);
}}
.sk-slide {{
  aspect-ratio: 16 / 9; width: 100%; box-sizing: border-box; overflow: hidden;
  container-type: inline-size; border-radius: 6px;
}}
/* put everything inside .sk-slide-body: it scales with the slide's width, not the window's */
.sk-slide-body {{
  height: 100%; box-sizing: border-box; padding: 3cqw 3.5cqw;
  font-size: 1.6cqw; display: flex; flex-direction: column;
}}

/* ---------- title on a highlighter swash, optional burst ticks ---------- */
.sk-title {{
  font-family: var(--sk-font-title); font-weight: 400; color: var(--sk-title-text);
  text-transform: uppercase; letter-spacing: .02em; line-height: 1.25;
  font-size: 3.4em; margin: 0; text-align: center;
}}
.sk-burst {{ position: relative; display: inline-block; padding: 0 1.2em; }}
.sk-burst::before, .sk-burst::after {{
  content: ""; position: absolute; top: 50%; width: .9em; height: 1.5em; transform: translateY(-50%);
  background-color: var(--sk-title-text);
}}
.sk-burst::before {{ left: 0; {mask(svg_uri(ticks_l), "center / contain no-repeat")} }}
.sk-burst::after  {{ right: 0; {mask(svg_uri(ticks_r), "center / contain no-repeat")} }}

/* ---------- highlighter swash: in a title, on a phrase, or on a whole row ---------- */
.sk-hl {{
  background: {svg_uri(swash)} center / 100% 100% no-repeat;
  -webkit-box-decoration-break: clone; box-decoration-break: clone;
  padding: .08em .4em 0; margin: 0 -.25em;
}}
.sk-title .sk-hl {{ padding: .12em .45em 0; margin: 0; }}
/* .sk-sweep: the swash sweeps in from the left, once. Still for people who ask for less motion. */
.sk-hl.sk-sweep {{ background-position: left center; animation: sk-sweep .9s cubic-bezier(.3, .7, .4, 1) .3s both; }}
@keyframes sk-sweep {{ from {{ background-size: 0% 100%; }} to {{ background-size: 100% 100%; }} }}
@media (prefers-reduced-motion: reduce) {{ .sk-hl.sk-sweep {{ animation: none; }} }}

/* ---------- section heading with a rule either side ---------- */
.sk-section {{
  display: flex; align-items: center; gap: .6em; margin: .6em 0;
  font-family: var(--sk-font-label); font-weight: 400; font-size: 2.2em; color: var(--sk-heading); line-height: 1;
}}
.sk-section::before, .sk-section::after {{
  content: ""; flex: 1; height: .3em; background-color: var(--sk-heading);
  {mask(svg_uri(rule), "center / 100% 100% no-repeat")}
}}

/* ---------- numbered step badge + label ---------- */
.sk-step {{ display: flex; align-items: center; gap: .45em; }}
.sk-num {{
  position: relative; isolation: isolate; flex: none; display: inline-grid; place-items: center;
  width: 1.9em; height: 1.9em; font-family: var(--sk-font-title); color: var(--sk-on-accent); font-size: 1.1em; line-height: 1; padding-top: .12em; box-sizing: border-box;
}}
.sk-num::before {{ content: ""; position: absolute; inset: 0; z-index: -1; border-radius: 50%; background: var(--sk-accent); filter: url(#sk-wobble); }}
.sk-label {{ font-family: var(--sk-font-label); color: var(--sk-accent-text); font-size: 1.5em; line-height: 1.05; text-transform: uppercase; }}

/* ---------- panel: wobbly outline in the accent colour ---------- */
.sk-panel {{
  position: relative; isolation: isolate; padding: 1em 1.1em 1.2em;
  display: flex; flex-direction: column; gap: .8em;
}}
.sk-panel::before {{
  content: ""; position: absolute; inset: 0; z-index: -1; border-radius: .9em;
  border: var(--sk-line-thin) solid var(--sk-accent); filter: url(#sk-wobble-soft);
}}
.sk-panel.sk-dashed::before {{ border-style: dashed; }}
/* .sk-wash: a pale wash of the accent mixed with the page */
.sk-panel.sk-wash::before {{ background: color-mix(in oklab, var(--sk-accent) 9%, var(--sk-page)); }}
.sk-panel > img, .sk-panel > .sk-icon {{ width: 42%; align-self: center; }}
.sk-panel p {{ margin: 0; font-size: 1.25em; line-height: 1.2; color: var(--sk-text); }}
.sk-panel .sk-em {{ color: var(--sk-accent-text); }}

/* ---------- tick: a hand-drawn tick, sized and coloured like text ---------- */
.sk-tick {{
  display: inline-block; width: 1em; height: 1em; vertical-align: -.12em; flex: none;
  color: var(--sk-forest-text); background-color: currentColor;
  {mask(svg_uri(tick), "center / contain no-repeat")}
}}

/* ---------- buttons: primary (filled) and secondary (outlined) ---------- */
.sk-btn {{
  position: relative; isolation: isolate; display: inline-flex; align-items: center; gap: .4em;
  border: 0; background: none; padding: .45em 1.15em .38em; margin: 0; cursor: pointer; text-decoration: none;
  font-family: var(--sk-font-label); font-size: 1.2em; line-height: 1.1; color: var(--sk-on-heading);
}}
.sk-btn::before {{
  content: ""; position: absolute; inset: 0; z-index: -1; border-radius: .6em;
  background: var(--sk-heading); filter: url(#sk-wobble-soft);
}}
.sk-btn:hover::before {{ background: color-mix(in oklab, var(--sk-heading) 85%, var(--sk-text)); }}
.sk-btn.sk-secondary {{ color: var(--sk-text); }}
.sk-btn.sk-secondary::before {{ background: transparent; border: 2.5px solid var(--sk-line); }}
.sk-btn.sk-secondary:hover::before {{ background: color-mix(in oklab, var(--sk-line) 8%, transparent); }}
.sk-btn + .sk-btn {{ margin-left: .6em; }}
.sk-btn:focus-visible {{ outline: 2.5px dashed var(--sk-heading); outline-offset: 4px; }}

/* ---------- progress meter: set --sk-value (0%–100%); the fill takes the accent ---------- */
.sk-meter {{ position: relative; isolation: isolate; display: block; height: .6em; min-width: 4em; }}
.sk-meter::before, .sk-meter::after {{ content: ""; position: absolute; inset: 0; z-index: -1; border-radius: 1em; filter: url(#sk-wobble-line); }}
.sk-meter::before {{ background: var(--sk-track); }}
.sk-meter::after {{ right: auto; width: var(--sk-value, 0%); background: var(--sk-accent); }}

/* ---------- speech bubble ---------- */
.sk-bubble {{
  position: relative; isolation: isolate; padding: .8em 1.2em; margin-bottom: 1.2em;
  font-family: var(--sk-font-body); font-size: 1.6em; line-height: 1.3; color: var(--sk-text);
}}
.sk-bubble::before, .sk-bubble::after {{ content: ""; position: absolute; z-index: -1; background: var(--sk-bubble-fill); filter: url(#sk-wobble); }}
.sk-bubble::before {{ inset: 0; border: 4px solid var(--sk-line); border-radius: 1.1em; }}
.sk-bubble::after {{
  width: 1.1em; height: 1.1em; left: 2em; bottom: -.62em;
  border-right: 4px solid var(--sk-line); border-bottom: 4px solid var(--sk-line); transform: rotate(45deg) skew(8deg, 8deg);
}}
.sk-bubble.sk-tail-right::after {{ left: auto; right: 2em; }}
.sk-bubble .sk-em {{ color: var(--sk-rust-text); font-weight: 700; }}

/* ---------- ribbon banner ---------- */
.sk-ribbon {{
  position: relative; isolation: isolate; display: inline-flex; align-items: center; gap: .5em;
  padding: .45em 1.4em .35em; margin: 0 2.4em;
  font-family: var(--sk-font-body); font-size: 1.6em; color: var(--sk-body-text);
}}
.sk-ribbon::before {{
  content: ""; position: absolute; inset: 0; z-index: -1;
  background: var(--sk-ribbon); border: 2.5px solid var(--sk-ink); filter: url(#sk-wobble-soft);
}}
.sk-ribbon::after {{
  content: ""; position: absolute; inset: .45em -2.2em -.45em; z-index: -2;
  background: {svg_uri(end_l)} left center / auto 100% no-repeat, {svg_uri(end_r)} right center / auto 100% no-repeat;
}}
.sk-ribbon .sk-kicker {{ font-family: var(--sk-font-label); color: var(--sk-rust-text); }}
.sk-ribbon img {{ height: 1.4em; }}

/* ---------- step row: equal-width panels with arrows between ---------- */
.sk-row {{ display: flex; align-items: stretch; gap: .25em; }}
.sk-row > .sk-panel {{ flex: 1 1 0; min-width: 0; }}

/* ---------- small helpers ---------- */
.sk-arrow {{ width: 1.6em; flex: none; align-self: center; }}
.sk-arrow :is(line, path) {{ stroke: var(--sk-connector); }}
.sk-loop {{ display: block; width: 100%; height: auto; }}
.sk-loop path {{ stroke: var(--sk-loop); }}
.sk-icon {{ display: block; }}
"""
open(os.path.join(KIT, "sketchbook.css"), "w").write(css)
json.dump({**TOKENS, "role": {k: {"css": v, "use": u} for k, (v, u) in ROLES.items()}},
          open(os.path.join(KIT, "tokens.json"), "w"), indent=2)

# ------------------------------------------------ icons (standalone SVGs)
import icons as icon_defs
ICONS = icon_defs.ICONS
missing = set(ICONS) - set(icon_defs.ABOUT)
assert not missing, f"add a line to ABOUT in icons.py for: {sorted(missing)}"
for name, parts in ICONS.items():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 156 156" role="img" aria-label="{name} doodle">'
           f'<defs>{filt("w", 0.035, 3.5, "-40 -40 240 240")}{WASH}</defs>'
           + icon_defs.render(parts, C, INK) + '</svg>')
    open(os.path.join(KIT, "icons", f"{name}.svg"), "w").write(svg)

# ------------------------------------------------ characters (standalone SVGs, A+B style)
CHAR_DEFS = (filt("wob-bubble", 0.04, 4.5, "-50 -50 400 500")
             + WASH.replace('id="sk-wash"', 'id="wash"')
             + filt("wob-lite", 0.03, 1.8, "-50 -50 400 500"))
import animals
PEOPLE = {"learner": gc.learner, "explainer": gc.explainer, "waver": gc.waver, "coffee": gc.coffee, "pointer": gc.bun}
def blend(parts): return gc.render(parts, paper=C["paper"])
CHAR_BOXES = {}
def write_char(name, viewbox, body, label):
    CHAR_BOXES[name] = viewbox
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="{viewbox}" role="img" aria-label="{label}">'
           f'<defs>{CHAR_DEFS}</defs>{body}</svg>')
    open(os.path.join(KIT, "characters", f"{name}.svg"), "w").write(svg)
for name, spec in PEOPLE.items():
    write_char(name, "50 4 196 356", blend(gc.person(spec)), f"{name} character")
write_char("cat", "40 20 170 190", blend(animals.cat()), "cat")
write_char("dog", "40 20 170 190", blend(animals.dog()), "dog")
# a group: four people side by side (the waver mirrored to wave outward), dog at their feet
group = (f'<g transform="translate(260 0) scale(-1 1)">{blend(gc.person(gc.waver))}</g>'
         f'<g transform="translate(125 0)">{blend(gc.person(gc.learner))}</g>'
         f'<g transform="translate(250 0)">{blend(gc.person(gc.coffee))}</g>'
         f'<g transform="translate(375 0)">{blend(gc.person(gc.bun))}</g>'
         f'<g transform="translate(-30 212) scale(.78)">{blend(animals.dog())}</g>')
write_char("group", "0 4 610 360", group, "a group of four people and a dog")

# One line per character: who they are and when to use them. Published in kit/index.json.
CHAR_ABOUT = {
    "learner": "A person reading a book with headphones on. Studying, learning, taking something in.",
    "explainer": "A person pointing up with an idea. Explaining, teaching, a tip or insight.",
    "waver": "A person waving. Hello, welcome, getting someone's attention, goodbye.",
    "coffee": "A person holding a mug of coffee. Relaxed, a break, informal chat.",
    "pointer": "A person pointing up with an idea. An alternative to the explainer.",
    "group": "Four people and a dog side by side. A team, a community, working together.",
    "cat": "A sitting cat, winking. Playful aside, a light moment.",
    "dog": "A sitting dog with its head tilted. Curiosity, a question, loyalty.",
}

# ------------------------------------------------ snippets + gallery
ARROW = ('<svg class="sk-arrow" viewBox="0 0 40 20" aria-hidden="true"><line x1="4" y1="10" x2="30" y2="10" '
         'stroke-width="4" stroke-linecap="round" marker-end="url(#sk-head)" filter="url(#sk-wobble-line)"/></svg>')
LOOP = ('<svg class="sk-loop" viewBox="0 0 1000 70" aria-hidden="true"><path d="M960 6 C 950 50, 820 54, 500 54 C 180 54, 50 50, 40 8" '
        'fill="none" stroke-width="5" stroke-linecap="round" marker-end="url(#sk-head)" filter="url(#sk-wobble-soft)"/></svg>')

def panel(color, n, label, icon, text, dashed=False, wash=False):
    return (f'<div class="sk-panel sk-{color}{" sk-dashed" if dashed else ""}{" sk-wash" if wash else ""}">\n'
            f'  <div class="sk-step"><span class="sk-num">{n}</span><span class="sk-label">{label}</span></div>\n'
            f'  <img src="icons/{icon}.svg" alt="">\n  <p>{text}</p>\n</div>')

SNIPPETS = [
    ("Title on highlighter", "Big marker caps on a yellow highlighter swash. Wrap each line's words in <code>.sk-hl</code>; add <code>.sk-burst</code> for the tick marks.",
     '<h1 class="sk-title"><span class="sk-burst"><span class="sk-hl">How to get the agent</span><br><span class="sk-hl">to teach you anything</span></span></h1>'),
    ("Section heading", "Label caps in deep teal with a rule either side.",
     '<h2 class="sk-section">The learning loop</h2>'),
    ("Step panel", "A numbered step in one of the five main colours. Add <code>.sk-dashed</code> for a dotted outline, to highlight the step you're talking about. Use <code>.sk-em</code> for accent text.",
     '<div class="sk-row">\n' + panel("teal", 2, "Filter + focus", "magnifier", 'use a lens: <span class="sk-em">“what do I care about?”</span>') + '\n'
     + panel("forest", 3, "Create new source", "page-pencil", "pull out just the parts that matter", dashed=True) + '\n</div>'),
    ("Speech bubble", "Something a person says or asks. Add <code>.sk-tail-right</code> to move the tail to the right.",
     '<div class="sk-bubble">“I want to learn <span class="sk-em">Chapter 1 of Shape Up</span>, while I’m driving.”</div>'),
    ("Ribbon banner", "An insight or takeaway. The kicker word goes in <code>.sk-kicker</code>, and an icon is optional.",
     '<div class="sk-ribbon"><img src="icons/car.svg" alt=""><span class="sk-kicker">Insight:</span> “I want to learn a book while driving.”</div>'),
    ("Arrows", "A short slate connector between steps, and the blue loop-back arrow that sits under a row of panels. Their colours come from the CSS.",
     ARROW + '\n' + LOOP),
    ("Panel wash", "Add <code>.sk-wash</code> to a panel for a pale wash of its accent colour mixed with the page, about 9%. Use it to set a card apart from the page.",
     '<div class="sk-row">\n' + panel("mustard", 1, "Add sources", "books", "books, manuals, transcripts, code", wash=True) + '\n'
     + panel("teal", 2, "Filter + focus", "magnifier", 'use a lens: <span class="sk-em">“what do I care about?”</span>', wash=True) + '\n</div>'),
    ("Highlighter anywhere", "<code>.sk-hl</code> works outside a title too: on a phrase, or on a whole row to mark the one you're on. Add <code>.sk-sweep</code> to sweep it in once, for a moment worth marking; it stays still for people who ask for less motion.",
     '<p style="font-size:1.4em;margin:0 0 .6em">Next is <span class="sk-hl">the lesson leads your coach thread</span>.</p>\n'
     '<div style="font-size:1.4em">\n  <div>The course outline shows where you are</div>\n  <div class="sk-hl sk-sweep">You can ask your coach anything</div>\n  <div>A side question goes in a side chat</div>\n</div>'),
    ("Tick", "A hand-drawn tick for something done or passing. It takes the size of the text around it, and the forest text colour; set <code>color</code> to change it. Give it a label when it stands alone.",
     '<p style="font-size:1.4em;margin:0"><span class="sk-tick" role="img" aria-label="done"></span> Three Examples hold.</p>\n'
     '<p style="font-size:2.6em;margin:0"><span class="sk-tick" role="img" aria-label="passing"></span></p>'),
    ("Buttons", "<code>.sk-btn</code> is the one main action on a screen: deep teal with paper lettering. Add <code>.sk-secondary</code> for the others: an ink outline.",
     '<button class="sk-btn" type="button">Start the course →</button>\n<button class="sk-btn sk-secondary" type="button">Use a different project</button>'),
    ("Progress meter", "A wobbly bar. Set <code>--sk-value</code> from 0% to 100%; the fill takes the accent, so a colour modifier changes it. Put the count in words next to it.",
     '<div style="display:flex;align-items:center;gap:.8em;font-size:1.3em">\n'
     '  <div class="sk-meter" role="progressbar" aria-label="Examples that hold" aria-valuemin="0" aria-valuemax="10" aria-valuenow="3" style="--sk-value:30%;width:10em"></div>\n'
     '  <span>3 of 10 Examples hold</span>\n</div>\n'
     '<div class="sk-meter sk-mustard" role="progressbar" aria-label="Lessons done" aria-valuemin="0" aria-valuemax="9" aria-valuenow="6" style="--sk-value:66%;width:10em;margin-top:1em"></div>'),
]

EXAMPLE = f'''<div class="sk-slide sk-paper"><div class="sk-slide-body">
  <h1 class="sk-title" style="font-size:2.7em"><span class="sk-burst"><span class="sk-hl">How to get the agent</span><br><span class="sk-hl">to teach you anything</span></span></h1>
  <h2 class="sk-section" style="font-size:1.7em;margin:.4em 0 .5em">The learning loop</h2>
  <div class="sk-row" style="font-size:.78em">
    {panel("mustard", 1, "Add sources", "books", "books, manuals, transcripts, code")}
    {ARROW}
    {panel("teal", 2, "Filter + focus", "magnifier", 'use a lens: <span class="sk-em">“what do I care about?”</span>')}
    {ARROW}
    {panel("forest", 3, "Create new source", "page-pencil", "pull out just the parts that matter", dashed=True)}
    {ARROW}
    {panel("coral", 4, "Create a projection", "headphones", "audio summary, infographic, quiz")}
    {ARROW}
    {panel("blue", 5, "Validate + iterate", "checklist", "teach back, quiz me, spaced repetition")}
  </div>
  <div style="margin:0 7% 0 7%">{LOOP}</div>
  <div style="display:flex;align-items:center;justify-content:center;gap:1.5em;margin-top:-.6em">
    <div class="sk-ribbon" style="font-size:1.3em"><img src="icons/car.svg" alt=""><span class="sk-kicker">Insight:</span> “I want to learn a book while driving.”</div>
    <img src="characters/learner.svg" alt="" style="height:6.2em;margin-top:.6em">
  </div>
</div></div>'''

def swatch(k, v):
    return f'<div class="sw"><i style="background:{v}"></i><b>--sk-{k}</b><span>{v}</span><em>{html.escape(COLOUR_ABOUT[k])}</em></div>'
def role_swatch(k, value, use):
    return (f'<div class="sw"><i style="background:var(--sk-{k})"></i><b>--sk-{k}</b>'
            f'<span>{html.escape(value)}</span><em>{html.escape(use)}</em></div>')
def figure(path, about, cls=""):
    return f'<figure{cls}><img src="{path}" alt=""><figcaption>{html.escape(about)}<code>{path}</code></figcaption></figure>'

cards = "\n".join(
    f'<section class="chunk"><h3>{html.escape(t)}</h3><p class="desc">{d}</p>'
    f'<div class="demo sk-paper">{s}</div><details><summary>Copy the code</summary><pre><code>{html.escape(s)}</code></pre></details></section>'
    for t, d, s in SNIPPETS)
fonts = "".join(f'<div><div style="font-family:var(--sk-font-{k});font-size:28px">{name}</div>{html.escape(use)}<code>--sk-font-{k}</code></div>'
                for k, (name, use) in FONT_ABOUT.items())
icons = "\n".join(f'<h3 class="grp">{g}</h3><div class="row">' + "".join(figure(f"icons/{n}.svg", icon_defs.ABOUT[n]) for n in names) + '</div>'
                  for g, names in icon_defs.GROUPS.items())
chars = "\n".join(figure(f"characters/{n}.svg", CHAR_ABOUT[n], ' class="char"') for n in CHAR_BOXES)

gallery = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sketchbook Kit</title>
<link rel="stylesheet" href="sketchbook.css">
<script src="sketchbook.js" defer></script>
<style>
  :root {{ --g-bg:#efeae0; --g-fg:#2a2a2a; --g-muted:#6b665c; --g-card:#fff; --g-line:#d9d2c3; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--g-bg); color:var(--g-fg); font:15px/1.5 system-ui,sans-serif; padding:24px 16px 60px; }}
  .wrap {{ max-width:1120px; margin:0 auto; }}
  header h1 {{ font-family:var(--sk-font-title); font-weight:400; font-size:44px; margin:0; color:var(--sk-title-text); display:inline-block;
               background:var(--sk-swash); padding:6px 16px 0; border-radius:4px 14px 6px 12px; }}
  header p {{ color:var(--g-muted); max-width:760px; }}
  h2.g {{ font:700 13px/1 system-ui; letter-spacing:.08em; text-transform:uppercase; color:var(--g-muted); margin:36px 0 12px; }}
  .chunks {{ display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }}
  @media (max-width:820px) {{ .chunks {{ grid-template-columns:1fr; }} }}
  .chunk {{ background:var(--g-card); border:1px solid var(--g-line); border-radius:10px; padding:14px 16px; min-width:0; }}
  .chunk h3 {{ margin:0; font-size:15px; }} .desc {{ margin:4px 0 10px; color:var(--g-muted); font-size:13.5px; }}
  .demo {{ padding:22px 18px; border-radius:8px; font-size:14px; overflow:hidden; }}
  .demo .sk-panel {{ max-width:260px; }}
  .demo .sk-row .sk-panel {{ max-width:none; }}
  details {{ margin-top:10px; }} summary {{ cursor:pointer; font-size:13px; color:var(--g-muted); }}
  pre {{ background:#1f1e1c; color:#ece7dc; padding:10px 12px; border-radius:6px; overflow:auto; font-size:12px; white-space:pre-wrap; word-break:break-word; }}
  .row {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px; }}
  figure {{ margin:0; background:var(--sk-page); border-radius:8px; padding:14px 12px 12px; text-align:center; }}
  figure img {{ width:80px; height:80px; }} figure.char img {{ width:auto; height:200px; max-width:100%; object-fit:contain; }}
  figcaption {{ font:12.5px/1.35 system-ui,sans-serif; color:var(--sk-text); margin-top:8px; text-align:left; }}
  figcaption code, .fonts code {{ display:block; font:11px ui-monospace,monospace; color:color-mix(in oklab, var(--sk-text) 75%, var(--sk-page)); margin-top:4px; overflow-wrap:anywhere; }}
  .sw em {{ display:block; font:12px/1.35 system-ui,sans-serif; color:var(--g-fg); margin-top:2px; }}
  .sw {{ font:12px/1.35 ui-monospace,monospace; }} .sw i {{ display:block; height:34px; border-radius:6px; border:1px solid rgba(0,0,0,.12); margin-bottom:4px; }}
  .sw b {{ display:block; font-weight:600; }} .sw span {{ color:var(--g-muted); overflow-wrap:anywhere; }}
  .roles .sw span {{ font-size:10.5px; display:block; }}
  h3.grp {{ font:600 13px/1 system-ui; margin:18px 0 8px; color:var(--g-muted); }}
  .fonts {{ display:grid; gap:10px; background:var(--sk-page); color:var(--sk-text); padding:16px; border-radius:8px; }}
</style></head>
<body><div class="wrap">
<header><h1>SKETCHBOOK KIT</h1>
<p>Reusable pieces for slides and static web content in the style of the “learn anything” lightning-lesson slides. Every piece is plain HTML, CSS or SVG.
Add <code>sketchbook.css</code> and <code>sketchbook.js</code> to a page, then paste in any chunk. Drop the icons and characters in as images anywhere.</p></header>

<h2 class="g">Example: a whole slide built only from kit pieces</h2>
{EXAMPLE}
<details><summary>Copy the code</summary><pre><code>{html.escape(EXAMPLE)}</code></pre></details>

<h2 class="g">Chunks</h2>
<div class="chunks">{cards}</div>

<h2 class="g">Characters</h2>
<div class="row">{chars}</div>

<h2 class="g">Doodle icons</h2>
<p class="desc">One colour for simple objects; up to three when the object has distinct parts. Always from the palette.</p>
{icons}

<h2 class="g">Tokens: colours (CSS variables in sketchbook.css; also tokens.json)</h2>
<div class="row">{"".join(swatch(k, v) for k, v in C.items())}</div>

<h2 class="g">Tokens: roles (what the pieces paint with)</h2>
<p class="desc">Use these rather than the palette when you build something new.</p>
<div class="row roles">{"".join(role_swatch(k, *v) for k, v in ROLES.items())}</div>

<h2 class="g">Tokens: type</h2>
<div class="fonts">{fonts}</div>
</div></body></html>'''
open(os.path.join(KIT, "index.html"), "w").write(gallery)

# ------------------------------------------------ index.json: the kit, for agents
import re
def aspect(viewbox):
    w, h = viewbox.split()[2:]
    return round(float(w) / float(h), 3)
def plain(text):
    return html.unescape(re.sub(r"<[^>]+>", "", text))
icon_tags = {n: g for g, names in icon_defs.GROUPS.items() for n in names}
def hosted(snippet):
    return re.sub(r'src="(icons|characters)/', lambda m: f'src="{URL}{m.group(1)}/', snippet)
index = (
    [{"kind": "icon", "name": n, "about": icon_defs.ABOUT[n], "tags": [icon_tags.get(n, "other")],
      "aspect": 1.0, "url": f"{URL}icons/{n}.svg"} for n in ICONS]
    + [{"kind": "character", "name": n, "about": CHAR_ABOUT[n], "aspect": aspect(CHAR_BOXES[n]),
        "url": f"{URL}characters/{n}.svg"} for n in CHAR_BOXES]
    + [{"kind": "piece", "name": t, "about": plain(d), "html": hosted(snip)} for t, d, snip in SNIPPETS]
    + [{"kind": "piece", "name": "Whole slide", "about": "A complete 16:9 slide built only from kit pieces. Start from this.", "html": hosted(EXAMPLE)}]
    + [{"kind": "colour", "name": k, "hex": v, "css": f"var(--sk-{k})", "about": COLOUR_ABOUT[k]} for k, v in C.items()]
    + [{"kind": "role", "name": k, "css": f"var(--sk-{k})", "value": v, "about": u} for k, (v, u) in ROLES.items()]
    + [{"kind": "font", "name": name, "css": f"var(--sk-font-{k})", "about": use} for k, (name, use) in FONT_ABOUT.items()]
)
missing = set(CHAR_BOXES) - set(CHAR_ABOUT)
assert not missing, f"add a line to CHAR_ABOUT in build_kit.py for: {sorted(missing)}"
json.dump(index, open(os.path.join(KIT, "index.json"), "w"), indent=2, ensure_ascii=False)
print("kit built:", sorted(os.listdir(KIT)))
