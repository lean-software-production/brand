# Brand

The Sketchbook brand: a hand-drawn style for our slides, website, courses and posts.

- **Guidelines deck:** `index.html`. Open it in a browser and use the arrow keys. It's published to GitHub Pages on every push to `main`.
- **Sketchbook kit:** `kit/`. Ready-to-use CSS, icons and characters. Open `kit/index.html` to see every piece, and read `kit/README.md` to use them.
- **Still to decide:** `TODO.md`.

## Warm, whimsical, wise

- **Warm:** cream paper, soft pastel washes and friendly faces. Welcoming, never corporate.
- **Whimsical:** wobbly ink, marker lettering and friendly doodles. They balance the systems-heavy ideas in our trainings with a reminder that humans and collaboration matter.
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

Everything in `kit/` except `kit/README.md` is generated. Edit the files in `src/` and rebuild:

```sh
python3 src/build_kit.py
```

- `src/build_kit.py`: tokens, CSS, the wobble filters and the kit gallery page.
- `src/icons.py`: object doodles.
- `src/characters.py`: people.
- `src/animals.py`: animals.
