---
name: sketchbook
description: Use when making slides, web pages, posts, course material or diagrams in our brand (the Sketchbook style - warm, whimsical, wise), or when asked to "make it on-brand". Finds the brand's ready-made icons, characters and HTML pieces from its published index.
---

# Sketchbook brand

Our brand is **warm, whimsical, wise**: cream paper, wobbly ink, pastel watercolour, marker titles, one idea at a time, in everyday words.

## 1. Set up the page

```html
<link rel="stylesheet" href="https://lean-software-production.github.io/brand/kit/sketchbook.css">
<script src="https://lean-software-production.github.io/brand/kit/sketchbook.js" defer></script>
```

Always include both: without the script, outlines lose their wobble or disappear.

## 2. Pick pieces from the index

```sh
curl -fsSL https://lean-software-production.github.io/brand/kit/index.json
```

A list of every element in the kit. Choose by reading each `about`.

- `piece`: ready-made HTML (titles, headings, step panels, bubbles, ribbons, arrows, a whole slide). Paste it in and change the words. Start from "Whole slide" for a slide.
- `icon`, `character`: images. Use them as whole files (`<img src="url">`); never edit, recolour or redraw them. `aspect` is width ÷ height.
- `colour`, `font`: the palette and type, as CSS variables. Don't use other colours or fonts.

To see how it all looks, open https://lean-software-production.github.io/brand/kit/index.html.

## 3. When something is missing

Don't draw it yourself or reach for another icon set: it won't match. Use the closest existing piece, and tell the user what's missing, so it can be added to the brand repo (https://github.com/lean-software-production/brand).
