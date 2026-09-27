# Animals for the Sketchbook kit, drawn with the same parts as the people in characters.py
# (chunky clean outline + pastel wash). Each sits in a 200×200 box.
INK = "#2a2724"
CREAM = "#FAEED3"

def _circle(cx, cy, r):
    return f"M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z"

def _oval(cx, cy, rx, ry):
    return f"M{cx-rx} {cy} a{rx} {ry} 0 1 0 {2*rx} 0 a{rx} {ry} 0 1 0 {-2*rx} 0 Z"

def cat(fur="#EEA306"):
    # Deliberately lopsided: head tilted, one ear bent, a wink, one paw forward.
    return [
        ("limb", "M138 170 C 176 176, 192 140, 172 118 C 164 110, 168 100, 176 102", fur, 14),
        ("shape", "M58 184 C 46 146, 62 108, 98 104 C 134 108, 150 144, 144 182 Z", fur),
        ("shape", "M82 182 C 80 156, 86 134, 98 132 C 112 136, 118 158, 114 180 Z", CREAM),
        ("shape", _oval(78, 186, 15, 8), fur), ("shape", _oval(122, 181, 11, 7), fur),
        ("head-start", "rotate(-9 100 84)"),
        ("shape", "M70 66 L64 30 L94 52 Z", fur), ("shape", "M126 64 L146 44 L140 36 L108 52 Z", fur),
        ("shape", _oval(100, 84, 36, 32), fur),
        ("line", "M90 56 L93 64 M101 53 L102 63 M111 57 L109 62", 3),
        ("dot", 88, 82, 4.5),
        ("line", "M106 83 Q113 76 120 83", 3.2),
        ("shape", "M97 93 L107 92 L102 99 Z", "#F76C37"),
        ("line", "M93 102 Q98 107 102 102 Q106 106 111 101", 2.8),
        ("line", "M64 90 L84 95 M68 102 L84 100 M136 94 L118 96 M132 104 L118 101", 2.2),
        ("blush", 80, 95), ("blush", 122, 95),
        ("head-end",),
    ]

def dog(fur="#D6631C", ears="#6b4a2e"):
    # Deliberately lopsided: head tilted, one ear flipped up, tongue to one side, a paw raised.
    return [
        ("limb", "M138 170 C 168 164, 180 140, 172 114", fur, 12),
        ("line", "M178 100 L186 90 M184 114 L196 110", 3),
        ("shape", "M58 186 C 50 146, 64 112, 100 110 C 136 112, 152 148, 142 186 Z", fur),
        ("shape", "M84 184 C 82 160, 90 140, 100 138 C 110 140, 116 158, 112 184 Z", CREAM),
        ("limb", "M84 152 L82 182", fur, 16),
        ("shape", _oval(80, 186, 13, 7), fur),
        ("shape", _oval(122, 186, 13, 7), fur),
        ("limb", "M116 148 C 130 146, 140 136, 140 120", fur, 15),
        ("shape", _oval(141, 116, 10, 12), fur),
        ("limb", "M70 120 C 86 132, 110 132, 126 118", "#1F78A8", 8),
        ("shape", _circle(104, 131, 5), "#EEA306"),
        ("head-start", "rotate(12 100 86)"),
        ("shape", _circle(100, 84, 34), fur),
        ("shape", _oval(100, 102, 19, 14), CREAM),
        ("shape", "M70 64 C 54 66, 50 98, 62 112 C 74 110, 78 88, 78 72 Z", ears),
        ("shape", "M126 60 C 136 40, 160 34, 168 42 C 158 50, 146 62, 134 70 Z", ears),
        ("dot", 88, 80, 4.5), ("dot", 113, 79, 5.5),
        ("shape", _oval(100, 95, 7, 5), INK),
        ("line", "M100 100 L100 105 M92 106 Q100 112 108 106", 2.8),
        ("shape", "M102 107 C 102 122, 116 124, 114 106 Z", "#F76C37"),
        ("head-end",),
    ]
