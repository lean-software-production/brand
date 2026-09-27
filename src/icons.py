# Doodle icons for the Sketchbook kit. Each icon is a list of parts in a 140×140 box:
#   (colour, path)          -> watercolour wash in that palette colour + wobbly ink outline
#   (None, path)            -> ink outline only (details, open lines)
#   ("solid", path)         -> filled ink (pupils, dots)
# Colour rule: one colour for simple objects; up to three when the object has distinct parts.
import math

def gear(cx, cy, r_out, r_in, teeth):
    pts = []
    for i in range(teeth * 4):
        a = 2 * math.pi * i / (teeth * 4)
        r = r_out if i % 4 in (1, 2) else r_in
        pts.append(f"{cx + r * math.cos(a):.1f} {cy + r * math.sin(a):.1f}")
    return "M" + " L".join(pts) + " Z"

ICONS = {
    # ---- the three brand words
    "mug": [  # warm
        ("coral", "M30 50 L100 50 L96 120 C 95 128, 90 132, 82 132 L48 132 C 40 132, 35 128, 34 120 Z"),
        (None, "M100 64 C 126 62, 128 100, 98 104 M99 76 C 112 76, 112 92, 98 92"),
        ("mustard", "M65 86 C 58 74, 44 84, 65 104 C 86 84, 72 74, 65 86 Z"),
        (None, "M52 38 C 44 28, 60 20, 52 8 M70 38 C 62 28, 78 20, 70 8 M88 38 C 80 28, 96 20, 88 8"),
    ],
    "kite": [  # whimsical
        ("mustard", "M70 4 L70 44 L34 44 Z"), ("coral", "M70 4 L106 44 L70 44 Z"),
        ("teal", "M34 44 L70 44 L70 100 Z"), ("blue", "M70 44 L106 44 L70 100 Z"),
        (None, "M70 100 C 56 108, 86 116, 70 124 C 58 130, 78 136, 66 142"),
        ("coral", "M62 110 L72 106 L70 116 Z"), ("mustard", "M64 128 L74 124 L72 134 Z"),
    ],
    "owl": [  # wise
        ("rust", "M70 22 C 30 22, 26 60, 30 90 C 34 120, 52 134, 70 134 C 88 134, 106 120, 110 90 C 114 60, 110 22, 70 22 Z"),
        (None, "M40 36 L32 12 L56 26 M100 36 L108 12 L84 26"),
        ("highlighter", "M39 62 a15 15 0 1 0 30 0 a15 15 0 1 0 -30 0 Z M71 62 a15 15 0 1 0 30 0 a15 15 0 1 0 -30 0 Z"),
        ("solid", "M49 63 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z M81 63 a5 5 0 1 0 10 0 a5 5 0 1 0 -10 0 Z"),
        ("mustard", "M63 80 L77 80 L70 92 Z"),
        (None, "M56 106 L60 112 L64 106 M68 106 L72 112 L76 106 M80 106 L84 112 L88 106 M34 72 C 24 92, 32 112, 46 118 M106 72 C 116 92, 108 112, 94 118"),
    ],
    # ---- redrawn older icons, now with more than one colour
    "books": [
        ("forest", "M22 104 L118 104 L118 128 L22 128 Z"), ("teal", "M30 80 L112 80 L112 104 L30 104 Z"),
        ("mustard", "M40 38 L60 36 L66 80 L44 80 Z"), ("coral", "M64 30 L84 30 L86 80 L66 80 Z"), ("blue", "M90 44 L110 50 L100 80 L86 78 Z"),
        (None, "M30 116 L110 116 M38 92 L104 92 M50 48 L56 70 M74 40 L76 70"),
    ],
    "car": [
        ("rust", "M8 86 L8 66 C 8 60, 12 58, 18 56 L36 52 L52 30 C 56 26, 60 24, 66 24 L100 24 C 108 24, 112 28, 116 34 L128 54 C 136 56, 140 60, 140 68 L140 86 Z"),
        ("blue", "M58 34 L68 34 L68 52 L46 52 Z M76 34 L102 34 L112 52 L76 52 Z"),
        ("slate", "M26 88 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 Z M96 88 a14 14 0 1 0 28 0 a14 14 0 1 0 -28 0 Z"),
    ],
    "lightbulb": [
        ("mustard", "M70 30 C 40 30, 30 60, 48 80 C 56 90, 56 98, 56 106 L 84 106 C 84 98, 84 90, 92 80 C 110 60, 100 30, 70 30 Z"),
        ("slate", "M56 108 L84 108 L82 124 L58 124 Z"),
        (None, "M58 116 L82 116 M22 56 L8 50 M70 14 L70 -2 M118 56 L132 50"),
    ],
    "checklist": [
        ("blue", "M24 22 L116 22 L116 132 L24 132 Z"), ("slate", "M50 12 L90 12 L90 32 L50 32 Z"),
        (None, "M38 50 L54 50 L54 66 L38 66 Z M38 78 L54 78 L54 94 L38 94 Z M38 106 L54 106 L54 122 L38 122 Z M64 58 L102 58 M64 86 L102 86 M64 114 L92 114"),
        ("forest", "M40 58 L46 64 L60 44 M40 86 L46 92 L60 72"),
    ],
    "headphones": [
        (None, "M26 84 C 22 30, 118 30, 114 84"),
        ("coral", "M16 80 L38 80 L38 124 L16 124 C 10 124, 8 118, 8 112 L8 92 C 8 86, 10 80, 16 80 Z M102 80 L124 80 C 130 80, 132 86, 132 92 L132 112 C 132 118, 130 124, 124 124 L102 124 Z"),
        (None, "M58 88 L58 110 M70 78 L70 120 M82 92 L82 106"),
    ],
    "magnifier": [
        (None, "M12 30 L90 30 M12 50 L70 50 M12 70 L60 70 M12 90 L50 90 M12 110 L74 110"),
        ("teal", "M44 64 a34 34 0 1 0 68 0 a34 34 0 1 0 -68 0 Z"),
        ("slate", "M103 89 L128 116 C 132 121, 126 127, 121 123 L96 96 Z"),
        (None, "M60 50 C 64 42, 72 38, 80 38"),
    ],
    "page-pencil": [
        ("paper", "M22 14 L84 14 L106 36 L106 128 L22 128 Z"),
        (None, "M84 14 L84 36 L106 36 M36 54 L90 54 M36 72 L90 72 M36 90 L70 90"),
        ("mustard", "M96 118 L128 64 L138 70 L106 124 L94 130 Z"), ("coral", "M122 60 L128 50 C 130 46, 136 46, 140 50 L138 70 Z"),
    ],
    # ---- new everyday objects
    "gear": [
        ("slate", gear(62, 64, 46, 36, 9) + " M46 64 a16 16 0 1 0 32 0 a16 16 0 1 0 -32 0 Z"),
        ("mustard", gear(112, 112, 24, 18, 7) + " M104 112 a8 8 0 1 0 16 0 a8 8 0 1 0 -16 0 Z"),
    ],
    "robot": [
        ("coral", "M64 16 a6 6 0 1 0 12 0 a6 6 0 1 0 -12 0 Z"), (None, "M70 22 L70 38"),
        ("blue", "M38 38 L102 38 C 108 38, 110 42, 110 48 L110 88 C 110 94, 108 98, 102 98 L38 98 C 32 98, 30 94, 30 88 L30 48 C 30 42, 32 38, 38 38 Z"),
        ("slate", "M20 56 L30 56 L30 80 L20 80 Z M110 56 L120 56 L120 80 L110 80 Z"),
        ("highlighter", "M44 64 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 Z M76 64 a10 10 0 1 0 20 0 a10 10 0 1 0 -20 0 Z"),
        ("solid", "M50 64 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z M82 64 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z"),
        (None, "M54 84 C 62 90, 78 90, 86 84"),
        ("teal", "M46 104 L94 104 L94 136 L46 136 Z"), (None, "M58 116 L82 116 M58 126 L74 126"),
    ],
    "sprout": [
        ("forest", "M70 58 C 50 58, 36 44, 38 28 C 58 28, 70 42, 70 58 Z M70 48 C 88 48, 104 34, 102 18 C 82 18, 70 32, 70 48 Z"),
        (None, "M70 84 C 70 66, 70 56, 70 44"),
        ("rust", "M34 82 L106 82 L106 96 L34 96 Z M40 96 L100 96 L92 134 L48 134 Z"),
    ],
    "puzzle": [
        ("coral", "M16 40 L60 40 L60 62 C 76 56, 76 88, 60 82 L60 120 L16 120 Z"),
        ("teal", "M68 40 L124 40 L124 120 L68 120 L68 88 C 84 94, 84 50, 68 56 Z"),
    ],
    "laptop": [
        ("slate", "M28 26 L112 26 L112 92 L28 92 Z M16 96 L124 96 L114 112 L26 112 Z"),
        ("teal", "M36 34 L104 34 L104 84 L36 84 Z"),
        (None, "M46 48 L66 48 M46 60 L82 60 M52 72 L64 72 M60 104 L80 104"),
    ],
    "chat": [
        ("mustard", "M14 30 C 14 18, 22 14, 34 14 L80 14 C 92 14, 98 20, 98 32 L98 52 C 98 62, 92 66, 80 66 L46 66 L28 82 L32 66 C 20 66, 14 60, 14 52 Z"),
        ("solid", "M34 40 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z M52 40 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z M70 40 a4 4 0 1 0 8 0 a4 4 0 1 0 -8 0 Z"),
        ("blue", "M52 86 C 52 78, 58 74, 68 74 L114 74 C 124 74, 130 80, 130 90 L130 106 C 130 116, 124 120, 114 120 L108 120 L114 138 L94 120 L68 120 C 58 120, 52 114, 52 106 Z"),
        (None, "M68 92 L112 92 M68 104 L98 104"),
    ],
    "compass": [
        ("mustard", "M20 74 a50 50 0 1 0 100 0 a50 50 0 1 0 -100 0 Z M64 24 L76 24 L76 12 L64 12 Z"),
        ("paper", "M30 74 a40 40 0 1 0 80 0 a40 40 0 1 0 -80 0 Z"),
        ("coral", "M70 40 L80 74 L60 74 Z"), ("slate", "M60 74 L80 74 L70 108 Z"),
        (None, "M70 36 L70 42 M70 106 L70 112 M34 74 L40 74 M100 74 L106 74"),
    ],
    "sticky-note": [
        ("mustard", "M24 24 L116 24 L116 96 L92 120 L24 120 Z"),
        (None, "M116 96 L92 96 L92 120 M38 48 L96 48 M38 64 L90 64 M38 80 L72 80"),
    ],
}

# One line per icon: what it shows and what it's good for. Published in kit/index.json so agents can pick icons.
ABOUT = {
    "mug": "A steaming mug with a heart. Warmth, welcome, a break, a chat over coffee. Stands for 'warm'.",
    "kite": "A colourful kite. Play, curiosity, freedom, trying things out. Stands for 'whimsical'.",
    "owl": "An owl. Knowledge, good judgement, a wise guide. Stands for 'wise'.",
    "books": "A stack of books. Sources, reading, research, a body of knowledge.",
    "page-pencil": "A page with a pencil. Writing, notes, drafting, creating something new.",
    "magnifier": "A magnifying glass. Looking closely, searching, focusing, filtering.",
    "lightbulb": "A lightbulb. An idea, an insight, a moment of understanding.",
    "checklist": "A checklist with ticks. Steps done, validation, testing, a plan.",
    "headphones": "Headphones. Listening, audio, podcasts, learning on the go.",
    "chat": "Two speech bubbles. Conversation, feedback, asking questions.",
    "puzzle": "Two puzzle pieces fitting together. Collaboration, integration, parts of a solution.",
    "sticky-note": "A sticky note. Ideas on a wall, workshops, capturing a thought.",
    "compass": "A compass. Direction, strategy, finding your way, goals.",
    "laptop": "A laptop. Computers, coding, working online.",
    "robot": "A friendly robot. AI, agents, automation.",
    "gear": "Gears. Systems, processes, how things work, machinery.",
    "sprout": "A sprout. Growth, learning, starting small, progress.",
    "car": "A car. Travel, a journey, learning on the move, speed.",
}

GROUPS = {
    "Brand words": ["mug", "kite", "owl"],
    "Learning": ["books", "page-pencil", "magnifier", "lightbulb", "checklist", "headphones"],
    "Working together": ["chat", "puzzle", "sticky-note", "compass"],
    "Tech & systems": ["laptop", "robot", "gear", "sprout", "car"],
}

def render(parts, colours, ink, wobble="url(#w)", wash="url(#sk-wash)"):
    washes, inks = [], []
    for col, d in parts:
        if col == "solid":
            inks.append(f'<path d="{d}" fill="{ink}" stroke="none"/>')
            continue
        if col:
            washes.append(f'<path d="{d}" fill="{colours[col]}"/>')
        inks.append(f'<path d="{d}"/>')
    return (f'<g stroke="none" opacity=".6" filter="{wash}" transform="translate(4 4)">{"".join(washes)}</g>'
            f'<g fill="none" stroke="{ink}" stroke-width="2.6" stroke-linecap="round" stroke-linejoin="round" filter="{wobble}">{"".join(p for p in inks if "fill=" not in p)}</g>'
            f'<g filter="{wobble}">{"".join(p for p in inks if "fill=" in p)}</g>')
