---
name: lean-software-production-brand
description: Use when making anything that carries the Lean Software Production brand - slides, web pages, posts, course material, docs or images - or when asked to make something "on-brand". Covers the brand's values (warm, whimsical, wise) and its Sketchbook kit of icons, characters, colours, fonts and HTML pieces.
---

# Lean Software Production brand

## 1. Know the brand

Our brand is **warm, whimsical, wise**. Read what each word means, and the style rules, before you make anything:

```sh
curl -fsSL https://raw.githubusercontent.com/lean-software-production/brand/main/README.md
```

## 2. Pick what you need from the kit

```sh
curl -fsSL https://lean-software-production.github.io/brand/kit/index.json
```

A list of every element in the kit. Choose by reading each `about`.

- `icon`, `character`: images, for anything (slides, docs, posts, web pages). Use them as whole files; never edit, recolour or redraw them. `aspect` is width ÷ height.
- `colour`, `font`: the palette and type. Don't use other colours or fonts.
- `role`: what the pieces paint with (page, text, heading, the `-text` colours). Use roles for anything you style yourself.
- `piece`: ready-made HTML (titles, headings, step panels, bubbles, ribbons, arrows, buttons, ticks, meters, a whole slide), for HTML pages and slides only.

To see how everything looks, open https://lean-software-production.github.io/brand/kit/index.html.

## 3. If you're building HTML

Put these in the page `<head>`, then paste in `piece`s and change the words. Start from "Whole slide" for a slide.

```html
<link rel="stylesheet" href="https://lean-software-production.github.io/brand/kit/sketchbook.css">
<script src="https://lean-software-production.github.io/brand/kit/sketchbook.js" defer></script>
```

Always include both: without the script, outlines lose their wobble or disappear.

## 4. When something is missing

Don't draw it yourself or reach for another icon set: it won't match. Use the closest existing element, and tell the user what's missing, so it can be added to the brand repo (https://github.com/lean-software-production/brand).
