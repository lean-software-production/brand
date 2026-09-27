# Sketchbook brand style — agreed decisions (2026-09-27)

Reference: the "How to learn anything w/ an Agent" lightning-lesson slides and the two
infographics in the "LL1: HOW TO LEARN ANYTHING" frame on the canvas.

## What's in this folder
- `index.html`: the brand guidelines deck (reveal.js). Published to GitHub Pages by `.github/workflows/pages.yml` on every push to `main`. Open it locally in a browser, and use the arrow keys to move between slides.
- `kit/`: the Sketchbook kit, with reusable pieces for slides and web pages. Open `kit/index.html` to see them, and read `kit/README.md` for how to use them.
- `reference/` (not published): the original slides and infographics this style was taken from.
- `build_kit.py`, `gen_characters.py`: generate the kit. Edit these, not the output.
- `slide-example*.html`, `character-styles.html`: the prototypes we iterated on to get here.

## Brand in three words
**Warm, whimsical, wise.**
- **Warm:** cream paper, soft pastel washes and friendly faces make everything we put out, from slides and the website to courses and posts, feel welcoming, never corporate.
- **Whimsical:** wobbly ink, marker lettering and friendly doodles balance the mechanical, systems-heavy ideas in our trainings with a playfulness that reminds everyone that humans and collaboration matter.
- **Wise:** simplicity and clarity first, with one idea at a time, steps in a clear order and simple, familiar images, so even hard topics are easy to understand. We use words normal people would use whenever we can. When we introduce jargon, we explain it clearly and concisely.

## Approved
- **Typography** — Luckiest Guy (big titles), Patrick Hand SC (step labels, headings), Patrick Hand (body).
- **Title treatment** — black marker caps on a pale-yellow highlighter swash (#FFEEB8), with burst tick marks either side.
- **Wobbly hand-drawn line** — the v1 speech-bubble wobble is THE line style. Use it on outlines, bubbles, panels and characters:
  `<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.5"/>`
  On chunky outlines (characters, ~5px strokes) use `baseFrequency="0.04"` and `scale="4.5"`: enough to show on the thick line but still smooth (scale 7 was too wobbly, 3.5 invisible).
  Always set `filterUnits="userSpaceOnUse"` with a region big enough for the drawing. Otherwise straight lines get clipped to nothing.
- **Characters: "A + B"** — a chunky, clear ink outline (5px, #2A2724) with the wobble above, filled with a pastel watercolour wash (fill at ~60% opacity, offset 2px, displacement + blur filter). Put an opaque paper layer under each wash. Very dark colours (hair, shoes) stay at ~88% so they don't turn grey. The generator is `gen_characters.py` (render mode `"blend"`).
- **Object doodles** (v2) — thin wobbly ink over an offset watercolour wash.
- **Layout pieces** (v2) — a section heading with rules on either side, outlined panels in the step colours (the highlighted step is dashed), a blue loop-back arrow, and a ribbon banner.

## Palette (sampled from the slides)
Mustard #EEA306 · Teal #039695 · Forest #4A7D4B · Coral #F76C37 · Blue #1F78A8 · Slate arrow #36545C ·
Rust #D6631C · Deep teal #094854 · Highlighter #FFEEB8 · Paper #FCF9F3 · Ribbon #FAEED3 · Ink #1B1B1B / #2A2724

## Rejected
- v1 big flat cartoon person (clip-art feel).
- v3 thin-pencil person: too hand-drawn, wanted chunkier.
