# Drawing and changing the kit

How to add icons, people, animals, scenes and layout pieces to the Sketchbook kit. The brand and style rules are in `../README.md`.

## How the drawing works

You draw; the scripts in `src/` apply the brand's look. Each picture is a list of **parts** (SVG paths you write by hand), and the scripts render every part the same way: palette colours, a watercolour wash, wobbly ink. This keeps every picture consistent, so never hand-edit the output in `kit/`.

One command rebuilds everything in `kit/` except `kit/README.md`:

```sh
python3 src/build_kit.py
```

After a change, rebuild, then **look at it**: screenshot `kit/index.html` (e.g. with headless Chromium) and check it before you commit. Commit `src/` and the rebuilt `kit/` together.

**Draw lopsided.** A mirror-image drawing looks machine-made. Tilt the head (wrap it in `("head-start", "rotate(…)")` … `("head-end",)`), make ears, eyes, hands and paws differ, and put the face or the action off centre. See `cat()` and `dog()` in `src/animals.py`. But don't overdo it: one or two touches per drawing, suggested by what the figure is doing, and feet stay on the ground. If every figure has a wobbly head, that looks machine-made too.

## Add an object icon

In `src/icons.py`, add an entry to `ICONS`. It's a list of `(colour, path)` parts in a 140×140 box, back to front:

- `("teal", "M…")`: a watercolour wash in that palette colour, with a wobbly ink outline.
- `(None, "M…")`: an ink line only (details, open strokes).
- `("solid", "M…")`: filled ink (pupils, dots).

Colour names are the palette keys in `TOKENS` in `src/build_kit.py`. Use one colour for simple objects, and up to three when the object has distinct parts. Also add the name to a list in `GROUPS`, or it won't appear in the gallery. It's written to `kit/icons/<name>.svg`.

## Add a person

People are one body with settings (`src/characters.py`):

- **Settings:** `pose` (`book`, `wave`, `mug`, anything else points), `hair` (`short`, `long`, `bun`, `bald`, `curly`), `skin`, `hairc`, `top`, `trousers`, and optional `glasses`, `headphones`/`phones`, `book`, `mugc`.
- **Adding them:** add a settings `dict` next to the others, then add it to `PEOPLE` in `src/build_kit.py`.
- **New poses or hair:** add a branch in `person()`.

Because every person shares one body, they can start to look alike. Before adding many, see the character-variety item in `TODO.md`.

## Add an animal (or any chunky character)

In `src/animals.py`, write a function that returns parts in a 200×200 box:

- `("shape", path, colour)`: a filled shape with a chunky outline.
- `("limb", path, colour, width)`: a thick stroke (tails, legs).
- `("line", path, width)`: an ink detail.
- `("dot", cx, cy, r)`: an eye.
- `("blush", cx, cy)`: a cheek.

Then add a `write_char(...)` call for it in `src/build_kit.py`, and its name to the `chars` list for the gallery. The same parts work for any chunky figure, not just animals.

## Compose a scene

A **scene** is several pictures in one image. `group.svg` in `src/build_kit.py` is the example: render each figure's parts, wrap each in `<g transform="translate(…)">`, and write the whole thing with `write_char`.

## A one-off drawing

If a slide needs something specific that the kit won't reuse, you can still draw it with the same parts and renderers above, so it matches. Don't add it to the kit unless it'll be reused: the kit should stay a small, useful library.

## A new layout piece (CSS)

Layout pieces are the building blocks like panels, bubbles and ribbons, and they live in the `sketchbook.css` section of `src/build_kit.py`. Class names start with `sk-`. Take colours and fonts from the tokens, and never add new colours. Add the new piece to the gallery in the same file, and to the table in `kit/README.md`.
