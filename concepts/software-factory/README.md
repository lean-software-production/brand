# Software factory: three homepage hero concepts

Open [the comparison page](index.html). Switch between “In a homepage” and “Just the drawings”, or open an individual SVG. The homepage copy is illustrative, not a proposed website change.

Matt selected the open workshop. [Round two](workshop-variations/index.html) explores three variations on that direction; the first-round assets below are preserved.

1. **The open workshop** — a recognisable cutaway factory. The most literal and immediately legible direction.
2. **The quality carousel** — a circular production cell. The feedback loop becomes the main visual idea.
3. **The factory in your hands** — a miniature factory inside a laptop. Emphasises software engineering and human control.

All three show multiple agents, making and independent checking, a return path, and working software as the outcome. Orchestration and human controls draw on the wider deck. Source: [What is a software factory?, slide 4](https://lean-software-production.github.io/what-is-a-software-factory/#/4).

## Assets

Each concept has a self-contained SVG (1000 × 700 viewBox, embedded Patrick Hand SC lettering) and a 2000 × 1400 PNG. Both have the brand's cream-paper background. Use the SVG on the website; the PNG is useful for quick reviews and slide decks. `concepts.json` includes descriptions and suggested alt text.

These are one-off proposals, not new shared kit pieces. No palette, font, robot design or wobble settings have been changed. The source reuses the kit's renderers and adds opaque foreground silhouettes so machinery cannot show through the robots or cards.

## Rebuild

From the repository root, using Python 3.12 or newer (required by the existing character renderer):

```sh
python3 src/build_factory_heroes.py
```

This also rebuilds the existing kit, without changing its contents. The concept SVGs and manifest are generated; edit `src/build_factory_heroes.py`, not the SVGs. The comparison page is hand-authored HTML.

To export PNGs and smoke-test the page, install Playwright outside the repository and use an installed Google Chrome:

```sh
npm install --prefix /tmp/factory-hero-preview playwright
NODE_PATH=/tmp/factory-hero-preview/node_modules node src/export_factory_heroes.cjs
```

For a different Chromium installation, set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` to its executable path. The exporter checks for missing images and horizontal overflow at desktop, tablet and phone widths, and exercises both preview modes. After geometry changes, visually inspect all three exports as well: a browser smoke test cannot judge layering or composition.

## Fonts

The existing brand fonts are bundled so the preview and SVGs work offline. Patrick Hand and Patrick Hand SC are distributed under the SIL Open Font License; Luckiest Guy under the Apache License 2.0. Their licences are included in `fonts/`. Sources: the Google Fonts CSS API and the [Google Fonts repository](https://github.com/google/fonts).
