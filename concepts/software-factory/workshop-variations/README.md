# Open workshop: three variations

Round two follows Matt's selection of the open-workshop concept. [Compare the variations](index.html), either as drawings or beside the same sample homepage copy used in round one.

1. **The airy workshop:** two broad roof bays, fewer labels and a pendant light. The closest refinement of the selected direction.
2. **The control loft:** a two-storey cutaway, with human direction upstairs and the make/check line below.
3. **The corner workshop:** a three-quarter view with a visible roof and side wall, retaining the open front.

All retain multiple agents, independent checking, a visible feedback loop and human controls. The existing palette, fonts, characters and wobble settings are unchanged. These remain one-off proposals outside the shared kit.

Each drawing has a self-contained SVG with embedded lettering and a 2000 × 1400 PNG. The cream-paper background is intentional. Descriptions and alt text are in `concepts.json`; the original concepts remain untouched in the parent directory.

## Rebuild

From the repository root, with Python 3.12 or newer:

```sh
python3 src/build_workshop_variations.py
```

The script reuses the drawing helpers from `src/build_factory_heroes.py` and rebuilds the kit as an import side effect. It does not regenerate or replace the first-round drawings.

For PNGs and the desktop/tablet/mobile browser checks:

```sh
npm install --prefix /tmp/factory-hero-preview playwright
NODE_PATH=/tmp/factory-hero-preview/node_modules node src/export_factory_heroes.cjs concepts/software-factory/workshop-variations
```

The exporter uses an installed Google Chrome; set `PLAYWRIGHT_CHROMIUM_EXECUTABLE` for another Chromium installation. It blocks external HTTP requests during the page checks, so the preview is also checked offline. Visually inspect the exported PNGs after geometry changes.

The fonts and their licences are reused from `../fonts/`. Source drawings live in `src/build_workshop_variations.py`; do not hand-edit the generated SVGs or manifest.
