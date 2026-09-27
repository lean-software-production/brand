# Brand

The Sketchbook brand: a hand-drawn style for our slides, website, courses and posts.

- **Guidelines deck:** `index.html`. Open it in a browser and use the arrow keys. It's published to GitHub Pages on every push to `main`.
- **Sketchbook kit:** `kit/`. Ready-to-use CSS, icons and characters. Open `kit/index.html` to see every piece, and read `kit/README.md` to use them.
- **Still to decide:** `TODO.md`.

## Using the brand from another project (agents)

Install the `lean-software-production-brand` skill. It points agents at the brand words and style rules below, and at the list of kit elements in `kit/index.json` (published at https://lean-software-production.github.io/brand/kit/index.json).

```sh
mkdir -p ~/.claude/skills/lean-software-production-brand
curl -fsSL https://lean-software-production.github.io/brand/skill/lean-software-production-brand/SKILL.md -o ~/.claude/skills/lean-software-production-brand/SKILL.md
```

Use `.claude/skills/` inside a project instead to install it for that project only. Agents without skills can be pointed at the same `SKILL.md`.

## Warm, whimsical, wise

- **Warm:** cream paper, soft pastel washes and friendly faces. Welcoming, never corporate.
- **Whimsical:** wobbly ink, marker lettering and friendly doodles. They balance the systems-heavy ideas in our trainings with a reminder that humans and collaboration matter. Nothing is perfectly symmetrical: heads tilt, ears and hands don't match, and faces sit a little off centre, so it looks drawn by a hand, not a machine.
- **Wise:** simplicity and clarity first. One idea at a time, steps in a clear order, simple familiar images. We use everyday words, and when we need jargon we explain it clearly and briefly.

## Style

- **Type:** Luckiest Guy for big titles, Patrick Hand SC for step labels and headings, Patrick Hand for body text.
- **Titles:** black marker capitals on a pale-yellow highlighter swash, with burst tick marks either side.
- **The wobbly line:** every outline, bubble, panel and character wobbles a little:
  `<feTurbulence type="fractalNoise" baseFrequency="0.035" numOctaves="2" seed="3"/><feDisplacementMap in="SourceGraphic" scale="3.5"/>`.
  On chunky ~5px outlines use `baseFrequency="0.04"` and `scale="4.5"`. Always set `filterUnits="userSpaceOnUse"` with a region big enough for the drawing, or straight lines get clipped away.
- **Characters:** a chunky 5px ink outline with the wobble, over a pastel watercolour wash (~60% opacity, offset 2px) on an opaque paper layer. Very dark colours (hair, shoes) stay at ~88% so they don't turn grey.
- **Objects:** thin wobbly ink over an offset watercolour wash.
- **Colours and fonts** are defined once, as tokens: see `kit/README.md`.

## Changing the kit

Everything in `kit/` except `kit/README.md` is generated from `src/`. Rebuild with `python3 src/build_kit.py`. How to add icons, people and other pieces: `src/README.md`.
