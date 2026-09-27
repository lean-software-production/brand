---
name: sketchbook
description: Use when making slides, web pages, posts, course material or diagrams in our brand (the Sketchbook style - warm, whimsical, wise), or when asked to "make it on-brand". Finds the brand's ready-made icons, characters and HTML pieces from its published index.
---

# Sketchbook brand

Our brand is **warm, whimsical, wise**: cream paper, wobbly ink, pastel watercolour, marker titles, one idea at a time, in everyday words.

## 1. Read the index

```sh
curl -fsSL https://lean-software-production.github.io/brand/kit/index.json
```

It lists everything the kit offers:
- `setup`: the two lines to put in the page `<head>`.
- `images`: every icon and character, with a one-line `about`, `tags`, `aspect` (width ÷ height) and `url`.
- `pieces`: ready-made HTML (titles, headings, step panels, bubbles, ribbons, arrows, a whole slide) with notes on how to use them.
- `rules`: follow them.
- `tokens`: colours and fonts, if you need them outside the CSS.

## 2. Build with it

- Add the `setup` lines, then paste in `pieces` and change the words. Start from "Whole slide" for a slide.
- Image paths inside `html` are relative: prefix them with `base_url`, or download the files next to your page.
- Use images as whole files (`<img src="…">`). Pick them by reading `about`. Never edit, recolour or redraw them.
- Only use palette colours, and the `colour_modifiers` classes on panels.
- If you're not sure how something should look, open `gallery` in a browser.

## 3. When something is missing

Don't draw it yourself or reach for another icon set: it won't match. Use the closest existing piece, and tell the user what's missing, so it can be added to the brand repo (https://github.com/lean-software-production/brand).
