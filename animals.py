# Animals for the Sketchbook kit, drawn with the same parts as the people in gen_characters.py
# (chunky clean outline + pastel wash). Each sits in a 200×200 box.
INK = "#2a2724"
CREAM = "#FAEED3"

def _circle(cx, cy, r):
    return f"M{cx-r} {cy} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z"

def _oval(cx, cy, rx, ry):
    return f"M{cx-rx} {cy} a{rx} {ry} 0 1 0 {2*rx} 0 a{rx} {ry} 0 1 0 {-2*rx} 0 Z"

def cat(fur="#EEA306"):
    return [
        ("limb", "M136 172 C 178 172, 186 130, 164 112", fur, 14),
        ("shape", "M60 182 C 52 142, 64 106, 100 102 C 136 106, 148 142, 140 182 Z", fur),
        ("shape", "M84 180 C 80 152, 88 130, 100 128 C 112 130, 120 152, 116 180 Z", CREAM),
        ("shape", _oval(82, 182, 13, 8), fur), ("shape", _oval(118, 182, 13, 8), fur),
        ("shape", "M72 66 L68 34 L94 52 Z", fur), ("shape", "M128 66 L132 34 L106 52 Z", fur),
        ("shape", _circle(100, 82, 34), fur),
        ("line", "M92 54 L94 62 M100 52 L100 60 M108 54 L106 62", 3),
        ("dot", 88, 82, 4.5), ("dot", 112, 82, 4.5),
        ("shape", "M95 92 L105 92 L100 98 Z", "#F76C37"),
        ("line", "M91 101 Q96 106 100 101 Q104 106 109 101", 2.8),
        ("line", "M66 92 L84 95 M66 101 L84 100 M134 92 L116 95 M134 101 L116 100", 2.2),
        ("blush", 80, 94), ("blush", 120, 94),
    ]

def dog(fur="#D6631C", ears="#6b4a2e"):
    return [
        ("limb", "M138 170 C 166 162, 176 142, 170 118", fur, 12),
        ("line", "M176 104 L184 96 M182 116 L192 112", 3),
        ("shape", "M58 186 C 50 146, 64 112, 100 110 C 136 112, 150 146, 142 186 Z", fur),
        ("shape", "M86 184 C 82 158, 90 138, 100 136 C 110 138, 118 158, 114 184 Z", CREAM),
        ("limb", "M84 152 L82 182", fur, 16), ("limb", "M116 152 L118 182", fur, 16),
        ("shape", _oval(80, 186, 13, 7), fur), ("shape", _oval(120, 186, 13, 7), fur),
        ("shape", _circle(100, 84, 34), fur),
        ("shape", _oval(100, 102, 19, 14), CREAM),
        ("shape", "M70 64 C 54 66, 50 98, 62 112 C 74 110, 78 88, 78 72 Z", ears),
        ("shape", "M130 64 C 146 66, 150 98, 138 112 C 126 110, 122 88, 122 72 Z", ears),
        ("dot", 88, 80, 4.5), ("dot", 112, 80, 4.5),
        ("shape", _oval(100, 95, 7, 5), INK),
        ("line", "M100 100 L100 105 M92 106 Q100 112 108 106", 2.8),
        ("shape", "M96 109 C 96 118, 104 118, 104 109 Z", "#F76C37"),
        ("limb", "M72 118 C 88 128, 112 128, 128 118", "#1F78A8", 8),
        ("shape", _circle(100, 128, 5), "#EEA306"),
    ]
