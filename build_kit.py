# Builds the static Sketchbook kit into ./kit from the agreed style (see README.md).
# Run: python3 build_kit.py
import html, json, os, sys
from urllib.parse import quote

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gen_characters as gc

KIT = os.path.join(HERE, "kit")
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
INK = C["ink"]

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
swash = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 100" preserveAspectRatio="none"><defs>'
         + filt("f", 0.02, 7, "-20 -20 440 140") + '</defs>'
         f'<path filter="url(#f)" fill="{C["highlighter"]}" d="M10 16 C 120 4, 280 6, 392 14 L 394 84 C 280 96, 120 94, 6 88 Z"/></svg>')
ticks_l = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 60 100"><defs>' + filt("f", 0.035, 3.5, "-10 -10 80 120") + '</defs>'
           f'<g filter="url(#f)" stroke="{C["ink-title"]}" stroke-width="7" stroke-linecap="round">'
           '<line x1="14" y1="14" x2="46" y2="34"/><line x1="6" y1="52" x2="50" y2="54"/><line x1="14" y1="92" x2="46" y2="74"/></g></svg>')
ticks_r = ticks_l.replace('<g filter', '<g transform="translate(60 0) scale(-1 1)"><g filter').replace('</g></svg>', '</g></g></svg>')
rule = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 400 10" preserveAspectRatio="none">'
        f'<path d="M2 5 C 100 3, 300 7, 398 5" stroke="{C["deep-teal"]}" stroke-width="3" fill="none" stroke-linecap="round" vector-effect="non-scaling-stroke"/></svg>')
end_l = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 92 92"><defs>' + filt("f", 0.02, 6, "-10 -10 112 112") + '</defs>'
         f'<path filter="url(#f)" d="M40 12 L 3 40 L 40 66 L 24 82 L 90 82 L 90 12 Z" fill="#F1DCAE" stroke="{INK}" stroke-width="2.5" stroke-linejoin="round"/></svg>')
end_r = end_l.replace('<path filter', '<g transform="translate(92 0) scale(-1 1)"><path filter').replace('/></svg>', '/></g></svg>')
grain = ('<svg xmlns="http://www.w3.org/2000/svg" width="300" height="300"><filter id="g"><feTurbulence type="fractalNoise" baseFrequency="0.9" numOctaves="2" seed="2"/>'
         '<feColorMatrix values="0 0 0 0 0.45  0 0 0 0 0.38  0 0 0 0 0.28  0 0 0 0.05 0"/></filter><rect width="300" height="300" filter="url(#g)"/></svg>')

# ------------------------------------------------ sketchbook.css
F = TOKENS["font"]
css = f"""/* Sketchbook kit: tokens + reusable chunks. Spec: README.md. Also include sketchbook.js (wobble filters). */
@import url("https://fonts.googleapis.com/css2?family=Luckiest+Guy&family=Patrick+Hand&family=Patrick+Hand+SC&display=swap");

:root {{
{chr(10).join(f"  --sk-{k}: {v};" for k, v in C.items())}
  --sk-font-title: {F["title"]};
  --sk-font-label: {F["label"]};
  --sk-font-body: {F["body"]};
  --sk-line-thin: 3px;
  --sk-line-chunky: 5px;
  --sk-accent: var(--sk-teal);
}}

/* ---------- colour modifiers: add to any chunk that uses an accent ---------- */
.sk-mustard {{ --sk-accent: var(--sk-mustard); }}
.sk-teal    {{ --sk-accent: var(--sk-teal); }}
.sk-forest  {{ --sk-accent: var(--sk-forest); }}
.sk-coral   {{ --sk-accent: var(--sk-coral); }}
.sk-blue    {{ --sk-accent: var(--sk-blue); }}
.sk-rust    {{ --sk-accent: var(--sk-rust); }}
.sk-deep-teal {{ --sk-accent: var(--sk-deep-teal); }}

/* ---------- paper: a 16:9 slide, or any paper-backed block ---------- */
.sk-paper {{
  background: {svg_uri(grain)}, var(--sk-paper);
  color: var(--sk-ink);
  font-family: var(--sk-font-body);
}}
.sk-slide {{
  aspect-ratio: 16 / 9; width: 100%; box-sizing: border-box; overflow: hidden;
  container-type: inline-size; padding: 3cqw 3.5cqw;
  font-size: 1.6cqw;               /* everything inside scales with the slide width */
  border-radius: 6px;
}}

/* ---------- title on a highlighter swash, optional burst ticks ---------- */
.sk-title {{
  font-family: var(--sk-font-title); font-weight: 400; color: var(--sk-ink-title);
  text-transform: uppercase; letter-spacing: .02em; line-height: 1.25;
  font-size: 3.4em; margin: 0; text-align: center;
}}
.sk-title .sk-hl {{
  background: {svg_uri(swash)} center / 100% 100% no-repeat;
  -webkit-box-decoration-break: clone; box-decoration-break: clone;
  padding: .12em .45em 0;
}}
.sk-burst {{ position: relative; display: inline-block; padding: 0 1.2em; }}
.sk-burst::before, .sk-burst::after {{
  content: ""; position: absolute; top: 50%; width: .9em; height: 1.5em; transform: translateY(-50%);
  background: center / contain no-repeat;
}}
.sk-burst::before {{ left: 0; background-image: {svg_uri(ticks_l)}; }}
.sk-burst::after  {{ right: 0; background-image: {svg_uri(ticks_r)}; }}

/* ---------- section heading with a rule either side ---------- */
.sk-section {{
  display: flex; align-items: center; gap: .6em; margin: .6em 0;
  font-family: var(--sk-font-label); font-weight: 400; font-size: 2.2em; color: var(--sk-deep-teal); line-height: 1;
}}
.sk-section::before, .sk-section::after {{
  content: ""; flex: 1; height: .3em; background: {svg_uri(rule)} center / 100% 100% no-repeat;
}}

/* ---------- numbered step badge + label ---------- */
.sk-step {{ display: flex; align-items: center; gap: .45em; }}
.sk-num {{
  position: relative; isolation: isolate; flex: none; display: inline-grid; place-items: center;
  width: 1.9em; height: 1.9em; font-family: var(--sk-font-title); color: #fff; font-size: 1.1em; line-height: 1; padding-top: .12em; box-sizing: border-box;
}}
.sk-num::before {{ content: ""; position: absolute; inset: 0; z-index: -1; border-radius: 50%; background: var(--sk-accent); filter: url(#sk-wobble); }}
.sk-label {{ font-family: var(--sk-font-label); color: var(--sk-accent); font-size: 1.5em; line-height: 1.05; text-transform: uppercase; }}

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
.sk-panel > img, .sk-panel > .sk-icon {{ width: 42%; align-self: center; }}
.sk-panel p {{ margin: 0; font-size: 1.25em; line-height: 1.2; color: var(--sk-body-text); }}
.sk-panel .sk-em {{ color: var(--sk-accent); }}

/* ---------- speech bubble ---------- */
.sk-bubble {{
  position: relative; isolation: isolate; padding: .8em 1.2em; margin-bottom: 1.2em;
  font-family: var(--sk-font-body); font-size: 1.6em; line-height: 1.3; color: var(--sk-body-text);
}}
.sk-bubble::before, .sk-bubble::after {{ content: ""; position: absolute; z-index: -1; background: var(--sk-bubble); filter: url(#sk-wobble); }}
.sk-bubble::before {{ inset: 0; border: 4px solid var(--sk-ink); border-radius: 1.1em; }}
.sk-bubble::after {{
  width: 1.1em; height: 1.1em; left: 2em; bottom: -.62em;
  border-right: 4px solid var(--sk-ink); border-bottom: 4px solid var(--sk-ink); transform: rotate(45deg) skew(8deg, 8deg);
}}
.sk-bubble.sk-tail-right::after {{ left: auto; right: 2em; }}
.sk-bubble .sk-em {{ color: var(--sk-rust); font-weight: 700; }}

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
.sk-ribbon .sk-kicker {{ font-family: var(--sk-font-label); color: var(--sk-rust); }}
.sk-ribbon img {{ height: 1.4em; }}

/* ---------- step row: equal-width panels with arrows between ---------- */
.sk-row {{ display: flex; align-items: stretch; gap: .25em; }}
.sk-row > .sk-panel {{ flex: 1 1 0; min-width: 0; }}

/* ---------- small helpers ---------- */
.sk-arrow {{ width: 1.6em; flex: none; align-self: center; }}
.sk-loop {{ display: block; width: 100%; height: auto; }}
.sk-icon {{ display: block; }}
"""
open(os.path.join(KIT, "sketchbook.css"), "w").write(css)
json.dump(TOKENS, open(os.path.join(KIT, "tokens.json"), "w"), indent=2)

# ------------------------------------------------ icons (standalone SVGs)
ICONS = {
    "books": ('<path d="M22 104 L118 104 L118 128 L22 128 Z"/><path d="M30 80 L112 80 L112 104 L30 104 Z"/><path d="M40 38 L60 36 L66 80 L44 80 Z"/>'
              '<path d="M64 30 L84 30 L86 80 L66 80 Z"/><path d="M90 44 L110 50 L100 80 L86 78 Z"/><path d="M30 116 L110 116 M38 92 L104 92 M50 48 L56 70 M74 40 L76 70"/>', "mustard"),
    "magnifier": ('<path d="M12 30 L90 30 M12 50 L70 50 M12 70 L60 70 M12 90 L50 90 M12 110 L74 110"/><circle cx="78" cy="64" r="34"/>'
                  '<path d="M103 89 L128 116 C 132 121, 126 127, 121 123 L96 96"/><path d="M60 50 C 64 42, 72 38, 80 38"/>', "teal"),
    "page-pencil": ('<path d="M22 14 L84 14 L106 36 L106 128 L22 128 Z"/><path d="M84 14 L84 36 L106 36"/><path d="M36 54 L90 54 M36 72 L90 72 M36 90 L70 90"/>'
                    '<path d="M96 118 L128 64 L138 70 L106 124 L94 130 Z"/><path d="M122 60 L132 66"/>', "forest"),
    "headphones": ('<path d="M26 84 C 22 30, 118 30, 114 84"/><path d="M16 80 L38 80 L38 124 L16 124 C 10 124, 8 118, 8 112 L8 92 C 8 86, 10 80, 16 80 Z"/>'
                   '<path d="M102 80 L124 80 C 130 80, 132 86, 132 92 L132 112 C 132 118, 130 124, 124 124 L102 124 Z"/><path d="M58 88 L58 110 M70 78 L70 120 M82 92 L82 106"/>', "coral"),
    "checklist": ('<path d="M24 22 L116 22 L116 132 L24 132 Z"/><path d="M50 12 L90 12 L90 32 L50 32 Z"/>'
                  '<path d="M38 50 L54 50 L54 66 L38 66 Z M38 78 L54 78 L54 94 L38 94 Z M38 106 L54 106 L54 122 L38 122 Z"/>'
                  '<path d="M64 58 L102 58 M64 86 L102 86 M64 114 L92 114"/><path d="M40 58 L46 64 L60 44 M40 86 L46 92 L60 72"/>', "blue"),
    "car": ('<path d="M8 86 L8 66 C 8 60, 12 58, 18 56 L36 52 L52 30 C 56 26, 60 24, 66 24 L100 24 C 108 24, 112 28, 116 34 L128 54 C 136 56, 140 60, 140 68 L140 86 Z"/>'
            '<path d="M58 34 L68 34 L68 52 L46 52 Z M76 34 L102 34 L112 52 L76 52 Z"/><circle cx="40" cy="88" r="14"/><circle cx="110" cy="88" r="14"/>', "rust"),
    "lightbulb": ('<path d="M70 30 C 40 30, 30 60, 48 80 C 56 90, 56 98, 56 106 L 84 106 C 84 98, 84 90, 92 80 C 110 60, 100 30, 70 30 Z"/>'
                  '<path d="M58 116 L82 116 M62 126 L78 126 M22 56 L8 50 M70 14 L70 -2 M118 56 L132 50"/>', "mustard"),
}
for name, (body, col) in ICONS.items():
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="-6 -10 156 152" role="img" aria-label="{name} doodle">'
           f'<defs>{filt("w", 0.035, 3.5, "-40 -40 240 240")}{WASH}</defs>'
           f'<g fill="{C[col]}" stroke="none" opacity=".55" filter="url(#sk-wash)" transform="translate(5 5)">{body}</g>'
           f'<g fill="none" stroke="{INK}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" filter="url(#w)">{body}</g></svg>')
    open(os.path.join(KIT, "icons", f"{name}.svg"), "w").write(svg)

# ------------------------------------------------ characters (standalone SVGs, A+B style)
CHAR_DEFS = (filt("wob-bubble", 0.04, 4.5, "-50 -50 400 500")
             + WASH.replace('id="sk-wash"', 'id="wash"')
             + filt("wob-lite", 0.03, 1.8, "-50 -50 400 500"))
for name, spec in (("learner", gc.learner), ("explainer", gc.explainer)):
    body = gc.render(gc.person(spec), "blend", paper=C["paper"])
    svg = (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="50 4 186 356" role="img" aria-label="{name} character">'
           f'<defs>{CHAR_DEFS}</defs>{body}</svg>')
    open(os.path.join(KIT, "characters", f"{name}.svg"), "w").write(svg)

# ------------------------------------------------ snippets + gallery
ARROW = ('<svg class="sk-arrow" viewBox="0 0 40 20" aria-hidden="true"><line x1="4" y1="10" x2="30" y2="10" '
         f'stroke="{C["slate"]}" stroke-width="4" stroke-linecap="round" marker-end="url(#sk-head)" filter="url(#sk-wobble-line)"/></svg>')
LOOP = ('<svg class="sk-loop" viewBox="0 0 1000 70" aria-hidden="true"><path d="M960 6 C 950 50, 820 54, 500 54 C 180 54, 50 50, 40 8" '
        f'fill="none" stroke="{C["blue"]}" stroke-width="5" stroke-linecap="round" marker-end="url(#sk-head)" filter="url(#sk-wobble-soft)"/></svg>')

def panel(color, n, label, icon, text, dashed=False):
    return (f'<div class="sk-panel sk-{color}{" sk-dashed" if dashed else ""}">\n'
            f'  <div class="sk-step"><span class="sk-num">{n}</span><span class="sk-label">{label}</span></div>\n'
            f'  <img src="icons/{icon}.svg" alt="">\n  <p>{text}</p>\n</div>')

SNIPPETS = [
    ("Title on highlighter", "Big marker caps on a yellow highlighter swash. Wrap each line's words in <code>.sk-hl</code>; add <code>.sk-burst</code> for the tick marks.",
     '<h1 class="sk-title"><span class="sk-burst"><span class="sk-hl">How to get the agent</span><br><span class="sk-hl">to teach you anything</span></span></h1>'),
    ("Section heading", "Label caps in deep teal with a rule either side.",
     '<h2 class="sk-section">The learning loop</h2>'),
    ("Step panel", "A numbered step in one of the five step colours. Add <code>.sk-dashed</code> to highlight the step you're talking about. Use <code>.sk-em</code> for accent text.",
     panel("teal", 2, "Filter + focus", "magnifier", 'use a lens: <span class="sk-em">“what do I care about?”</span>')),
    ("Speech bubble", "Something a person says or asks. Add <code>.sk-tail-right</code> to move the tail to the right.",
     '<div class="sk-bubble">“I want to learn <span class="sk-em">Chapter 1 of Shape Up</span>, while I’m driving.”</div>'),
    ("Ribbon banner", "An insight or takeaway. The kicker word goes in <code>.sk-kicker</code>, and an icon is optional.",
     '<div class="sk-ribbon"><img src="icons/car.svg" alt=""><span class="sk-kicker">Insight:</span> “I want to learn a book while driving.”</div>'),
    ("Arrows", "A short slate connector between steps, and the blue loop-back arrow that sits under a row of panels.",
     ARROW + '\n' + LOOP),
]

EXAMPLE = f'''<div class="sk-slide sk-paper">
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
    <img src="characters/learner.svg" alt="" style="height:6.2em;margin-top:-1.5em">
  </div>
</div>'''

def swatch(k, v):
    return f'<div class="sw"><i style="background:{v}"></i><b>--sk-{k}</b><span>{v}</span></div>'

cards = "\n".join(
    f'<section class="chunk"><h3>{html.escape(t)}</h3><p class="desc">{d}</p>'
    f'<div class="demo sk-paper">{s}</div><details><summary>Copy the code</summary><pre><code>{html.escape(s)}</code></pre></details></section>'
    for t, d, s in SNIPPETS)
icons = "\n".join(f'<figure><img src="icons/{n}.svg" alt=""><figcaption>icons/{n}.svg</figcaption></figure>' for n in ICONS)
chars = "\n".join(f'<figure class="char"><img src="characters/{n}.svg" alt=""><figcaption>characters/{n}.svg</figcaption></figure>' for n in ("learner", "explainer"))

gallery = f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1">
<title>Sketchbook Kit</title>
<link rel="stylesheet" href="sketchbook.css">
<script src="sketchbook.js" defer></script>
<style>
  :root {{ --g-bg:#efeae0; --g-fg:#2a2a2a; --g-muted:#6b665c; --g-card:#fff; --g-line:#d9d2c3; }}
  @media (prefers-color-scheme: dark) {{ :root:not([data-theme="light"]) {{ --g-bg:#1c1b19; --g-fg:#ece7dc; --g-muted:#a39d90; --g-card:#262521; --g-line:#3a3833; }} }}
  :root[data-theme="dark"] {{ --g-bg:#1c1b19; --g-fg:#ece7dc; --g-muted:#a39d90; --g-card:#262521; --g-line:#3a3833; }}
  * {{ box-sizing: border-box; }}
  body {{ margin:0; background:var(--g-bg); color:var(--g-fg); font:15px/1.5 system-ui,sans-serif; padding:24px 16px 60px; }}
  .wrap {{ max-width:1120px; margin:0 auto; }}
  header h1 {{ font-family:var(--sk-font-title); font-weight:400; font-size:44px; margin:0; color:var(--sk-ink-title); display:inline-block;
               background:var(--sk-highlighter); padding:6px 16px 0; border-radius:4px 14px 6px 12px; }}
  header p {{ color:var(--g-muted); max-width:760px; }}
  h2.g {{ font:700 13px/1 system-ui; letter-spacing:.08em; text-transform:uppercase; color:var(--g-muted); margin:36px 0 12px; }}
  .chunks {{ display:grid; grid-template-columns:repeat(2,1fr); gap:16px; }}
  @media (max-width:820px) {{ .chunks {{ grid-template-columns:1fr; }} }}
  .chunk {{ background:var(--g-card); border:1px solid var(--g-line); border-radius:10px; padding:14px 16px; min-width:0; }}
  .chunk h3 {{ margin:0; font-size:15px; }} .desc {{ margin:4px 0 10px; color:var(--g-muted); font-size:13.5px; }}
  .demo {{ padding:22px 18px; border-radius:8px; font-size:14px; overflow:hidden; }}
  .demo .sk-panel {{ max-width:260px; }}
  details {{ margin-top:10px; }} summary {{ cursor:pointer; font-size:13px; color:var(--g-muted); }}
  pre {{ background:#1f1e1c; color:#ece7dc; padding:10px 12px; border-radius:6px; overflow:auto; font-size:12px; white-space:pre-wrap; word-break:break-word; }}
  .row {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(150px,1fr)); gap:12px; }}
  figure {{ margin:0; background:var(--sk-paper); border-radius:8px; padding:12px; text-align:center; }}
  figure img {{ width:80px; height:80px; }} figure.char img {{ width:auto; height:200px; }}
  figcaption {{ font:12px ui-monospace,monospace; color:#6b665c; margin-top:6px; overflow-wrap:anywhere; }}
  .sw {{ font:12px/1.35 ui-monospace,monospace; }} .sw i {{ display:block; height:34px; border-radius:6px; border:1px solid rgba(0,0,0,.12); margin-bottom:4px; }}
  .sw b {{ display:block; font-weight:600; }} .sw span {{ color:var(--g-muted); }}
  .fonts {{ display:grid; gap:10px; background:var(--sk-paper); color:var(--sk-ink); padding:16px; border-radius:8px; }}
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
<div class="row">{icons}</div>

<h2 class="g">Tokens: colours (CSS variables in sketchbook.css; also tokens.json)</h2>
<div class="row">{"".join(swatch(k, v) for k, v in C.items())}</div>

<h2 class="g">Tokens: type</h2>
<div class="fonts">
  <div style="font-family:var(--sk-font-title);font-size:34px">--SK-FONT-TITLE · LUCKIEST GUY</div>
  <div style="font-family:var(--sk-font-label);font-size:28px;color:var(--sk-deep-teal)">--sk-font-label · Patrick Hand SC</div>
  <div style="font-family:var(--sk-font-body);font-size:24px">--sk-font-body · Patrick Hand: for sentences and captions</div>
</div>
</div></body></html>'''
open(os.path.join(KIT, "index.html"), "w").write(gallery)
print("kit built:", sorted(os.listdir(KIT)))
