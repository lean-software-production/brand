# Generates character-styles.html: the same two people rendered in three chunky styles.
import os
HERE = os.path.dirname(os.path.abspath(__file__))
INK = "#2a2724"

def person(p):
    """Geometry for one standing person in a 260x380 box, as layered parts (back to front)."""
    parts = []
    L = lambda d, col, w: parts.append(("limb", d, col, w))
    S = lambda d, col: parts.append(("shape", d, col))
    C = lambda cx, cy, r, col: parts.append(("shape", f"M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z", col))
    D = lambda d, w=3.5: parts.append(("line", d, w))
    Dot = lambda cx, cy, r: parts.append(("dot", cx, cy, r))
    # legs + shoes
    L("M112 256 L110 330", p["trousers"], 26)
    L("M148 256 L150 330", p["trousers"], 26)
    S("M88 330 h26 a10 10 0 0 1 0 20 h-26 a10 10 0 0 1 0 -20 Z", INK)
    S("M146 330 h26 a10 10 0 0 1 0 20 h-26 a10 10 0 0 1 0 -20 Z", INK)
    # back (left) arm, hanging
    L("M98 152 C 84 178, 80 204, 82 228", p["top"], 22)
    C(82, 236, 11, p["skin"])
    # torso
    S("M96 140 C 104 132, 156 132, 164 140 L 176 246 C 177 256, 172 262, 162 262 L 98 262 C 88 262, 83 256, 84 246 Z", p["top"])
    D("M114 140 Q130 152 146 140")
    # front (right) arm + prop
    if p["pose"] == "book":
        L("M162 152 C 184 172, 188 196, 170 210", p["top"], 22)
        S("M114 186 L160 176 L204 184 L202 234 L160 228 L116 238 Z", p["book"])
        S("M120 188 L160 180 L198 188 L196 228 L160 222 L122 232 Z", "#ffffff")
        D("M160 180 L160 222", 3)
        D("M130 196 L150 192 M130 206 L150 202 M170 194 L188 197 M170 204 L186 207", 2.5)
        C(160, 226, 10, p["skin"])
    elif p["pose"] == "wave":
        L("M162 150 C 186 142, 198 120, 202 98", p["top"], 22)
        C(203, 88, 12, p["skin"])
        D("M218 70 C 226 78, 226 92, 220 100 M226 62 C 238 74, 238 98, 228 108", 3.5)
    elif p["pose"] == "mug":
        L("M162 152 C 184 172, 184 196, 168 206", p["top"], 22)
        S("M142 186 L174 186 L172 224 L144 224 Z", p.get("mugc", "#F76C37"))
        D("M174 194 C 186 194, 186 214, 173 214", 3.5)
        C(160, 212, 10, p["skin"])
        D("M152 176 C 148 168, 156 164, 152 156 M164 176 C 160 168, 168 164, 164 156", 3)
    else:  # pointing up
        L("M162 150 C 186 134, 196 108, 198 82", p["top"], 22)
        L("M199 70 L203 48", p["skin"], 8)
        C(199, 72, 11, p["skin"])
        D("M186 40 L180 32 M212 36 L218 28 M200 26 L200 16", 3.5)
    # head
    parts.append(("head-start",))
    if p["hair"] == "long":
        S("M86 100 C 78 50, 110 36, 130 38 C 150 36, 182 50, 174 100 L 180 158 C 168 164, 156 158, 154 146 L 106 146 C 104 158, 92 164, 80 158 Z", p["hairc"])
    if p["hair"] == "bun":
        C(130, 44, 17, p["hairc"])
    C(130, 92, 42, p["skin"])
    if p["hair"] == "short":
        S("M88 96 C 82 52, 110 40, 134 42 C 162 44, 178 62, 172 96 C 164 74, 144 68, 126 72 C 108 74, 96 82, 88 96 Z", p["hairc"])
    elif p["hair"] == "long":
        S("M88 92 C 90 58, 112 48, 134 50 C 156 50, 172 64, 172 92 C 160 72, 140 66, 124 70 C 108 72, 96 80, 88 92 Z", p["hairc"])
    elif p["hair"] == "bun":
        S("M88 94 C 84 60, 108 48, 132 50 C 158 50, 176 66, 172 94 C 162 76, 144 70, 128 72 C 110 74, 96 82, 88 94 Z", p["hairc"])
    elif p["hair"] == "bald":
        D("M100 62 C 110 56, 122 54, 132 54", 2.5)
    else:  # curly
        S("M84 104 C 68 94, 72 66, 90 62 C 88 42, 112 32, 126 42 C 138 28, 164 34, 164 52 C 184 54, 190 82, 176 104 C 170 82, 152 72, 130 72 C 108 72, 92 84, 84 104 Z", p["hairc"])
    Dot(116, 98, 4.5); Dot(144, 98, 4.5)
    if p.get("beard"):
        S("M96 110 C 100 134, 116 140, 130 140 C 144 140, 160 134, 164 110 C 156 122, 146 126, 130 126 C 114 126, 104 122, 96 110 Z", p["beard"])
    D("M119 113 Q130 122 141 113")
    parts.append(("blush", 106, 110)); parts.append(("blush", 154, 110))
    if p.get("glasses"):
        D("M106 98 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M134 98 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 M126 97 L134 97", 3)
    if p.get("headphones"):
        L("M90 92 C 86 40, 174 40, 170 92", p["phones"], 7)
        S("M78 80 h14 a6 6 0 0 1 6 6 v18 a6 6 0 0 1 -6 6 h-14 a6 6 0 0 1 -6 -6 v-18 a6 6 0 0 1 6 -6 Z", p["phones"])
        S("M168 80 h14 a6 6 0 0 1 6 6 v18 a6 6 0 0 1 -6 6 h-14 a6 6 0 0 1 -6 -6 v-18 a6 6 0 0 1 6 -6 Z", p["phones"])
    parts.append(("head-end",))
    return parts

def dark(col):
    """Very dark colours (hair, shoes) keep their weight instead of washing out to grey."""
    if not col.startswith("#"): return False
    r, g, b = (int(col[i:i+2], 16) for i in (1, 3, 5))
    return 0.2126*r + 0.7152*g + 0.0722*b < 60

def render(parts, style, head_scale=1.0, paper="var(--paper)"):
    out = []
    for part in parts:
        k = part[0]
        if k == "head-start":
            out.append(f'<g transform="translate(130 110) scale({head_scale}) translate(-130 -110)">'); continue
        if k == "head-end":
            out.append("</g>"); continue
        if k == "shape":
            d, col = part[1], part[2]
            if style == "comic":
                out.append(f'<path d="{d}" fill="{col}" stroke="{INK}" stroke-width="5" stroke-linejoin="round" filter="url(#wob-lite)"/>')
            elif style == "soft":
                out.append(f'<path d="{d}" fill="{col}"/>')
            elif style == "blend":
                out.append(f'<path d="{d}" fill="{paper}"/><path d="{d}" fill="{col}" opacity="{'.88' if dark(col) else '.6'}" transform="translate(2 2)" filter="url(#wash)"/>'
                           f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="5" stroke-linejoin="round" filter="url(#wob-bubble)"/>')
            else:  # storybook
                out.append(f'<path d="{d}" fill="{col}" opacity=".62" transform="translate(4 4)" filter="url(#wash)"/>'
                           f'<path d="{d}" fill="none" stroke="{INK}" stroke-width="4.5" stroke-linejoin="round" filter="url(#wob)"/>')
        elif k == "limb":
            d, col, w = part[1], part[2], part[3]
            if style == "comic":
                out.append(f'<g filter="url(#wob-lite)" fill="none" stroke-linecap="round"><path d="{d}" stroke="{INK}" stroke-width="{w+10}"/><path d="{d}" stroke="{col}" stroke-width="{w}"/></g>')
            elif style == "soft":
                out.append(f'<path d="{d}" fill="none" stroke="{col}" stroke-width="{w+4}" stroke-linecap="round"/>')
            elif style == "blend":
                out.append(f'<g fill="none" stroke-linecap="round"><path d="{d}" stroke="{INK}" stroke-width="{w+10}" filter="url(#wob-bubble)"/><path d="{d}" stroke="{paper}" stroke-width="{w}"/>'
                           f'<path d="{d}" stroke="{col}" stroke-width="{w-2}" opacity=".6" filter="url(#wash)"/></g>')
            else:
                out.append(f'<g fill="none" stroke-linecap="round"><path d="{d}" stroke="{INK}" stroke-width="{w+9}" filter="url(#wob)"/><path d="{d}" stroke="{paper}" stroke-width="{w}"/>'
                           f'<path d="{d}" stroke="{col}" stroke-width="{w-2}" opacity=".72" filter="url(#wash)"/></g>')
        elif k == "line":
            w = part[2] + (1 if style in ("comic", "blend") else 0)
            out.append(f'<path d="{part[1]}" fill="none" stroke="{INK}" stroke-width="{w}" stroke-linecap="round" stroke-linejoin="round"/>')
        elif k == "dot":
            out.append(f'<circle cx="{part[1]}" cy="{part[2]}" r="{part[3] + (1 if style=="soft" else 0)}" fill="{INK}"/>')
        elif k == "blush":
            out.append(f'<ellipse cx="{part[1]}" cy="{part[2]}" rx="8" ry="5" fill="#f28c7a" opacity=".45"/>')
    return "\n".join(out)

learner = dict(pose="book", skin="#f3c9a8", hair="short", hairc="#6b4a2e", top="#4a7d4b", trousers="#36545c",
               book="#1f78a8", headphones=True, phones="#f76c37")
waver = dict(pose="wave", skin="#e8b48f", hair="long", hairc="#3b2a20", top="#039695", trousers="#36545c")
coffee = dict(pose="mug", skin="#7a4b30", hair="bald", hairc="#2b2320", beard="#7a6656", glasses=True, top="#1f78a8",
              trousers="#36545c", mugc="#F76C37")
bun = dict(pose="point", skin="#f0c2a0", hair="bun", hairc="#c0612b", top="#f76c37", trousers="#4a7d4b")
explainer = dict(pose="point", skin="#a8704a", hair="curly", hairc="#2b2320", top="#eea306", trousers="#1f78a8",
                 glasses=True)

def main():
    STYLES = [
        ("comic", "A · Comic ink", 1.0,
         "Thick, even black outline and flat colour fills, like the “meeting you missed” comic. The boldest and most graphic; still readable from the back of the room."),
        ("storybook", "B · Storybook", 1.0,
         "Chunky ink outline with the watercolour wash sitting slightly off the line. The same shapes as A, but softer: closest to the infographics, just heavier than v3."),
        ("soft", "C · Soft shapes", 1.12,
         "No outlines: rounded blocks of flat colour, a slightly bigger head, stubby limbs. A modern, friendly look that sits well next to the wobbly ink panels."),
    ]

    cards = []
    for key, name, hs, desc in STYLES:
        svg = (f'<svg viewBox="30 0 480 370" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="{name}: two example people">'
               f'<g>{render(person(learner), key, hs)}</g>'
               f'<g transform="translate(240 0)">{render(person(explainer), key, hs)}</g></svg>')
        cards.append(f'<section class="card"><h2>{name}</h2><div class="stage">{svg}</div><p>{desc}</p></section>')

    bsvg = (f'<svg viewBox="30 0 480 370" xmlns="http://www.w3.org/2000/svg" role="img" aria-label="A plus B: two example people">'
            f'<g>{render(person(learner), "blend")}</g><g transform="translate(240 0)">{render(person(explainer), "blend")}</g></svg>')
    blend = (f'<section class="card pick"><div class="stage">{bsvg}</div><div><h2>A + B · Clean ink, pastel wash</h2>'
             f'<p>A’s clear, even outline, wobbling like the v1 speech bubble, with B’s soft pastel watercolour inside it. The wash sits just inside the line, so the colour still looks painted but the edges stay crisp.</p>'
             f'<p class="tag">Combined from your feedback</p></div></section>')
    html = open(os.path.join(HERE, "character-styles.tmpl.html")).read().replace("{{CARDS}}", "\n".join(cards)).replace("{{BLEND}}", blend)
    open(os.path.join(HERE, "character-styles.html"), "w").write(html)
    print("ok")


if __name__ == "__main__":
    main()
