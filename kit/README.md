# Sketchbook kit

Reusable pieces for slides and static web content, in the cartoony style of the "learn anything" lightning-lesson slides. Everything is plain HTML, CSS and SVG, with no framework and no build step. Open `index.html` to see every piece with copy-and-paste code.

Built by `../build_kit.py`. Edit that file, not the output, then re-run `python3 build_kit.py`. The brand words and the style decisions behind the kit are in `../README.md`.

## Use it on a page

```html
<link rel="stylesheet" href="sketchbook.css">
<script src="sketchbook.js" defer></script>   <!-- adds the wobbly-line filters once per page -->
```

Without `sketchbook.js`, outlines, badges and bubbles lose their wobble (Chrome) or disappear (Firefox). Always include it.

## The pieces

| Piece | Markup |
|---|---|
| 16:9 slide on paper | `<div class="sk-slide sk-paper">…</div>`. Everything inside scales with the slide width. `sk-paper` alone gives any block the paper background. |
| Title on highlighter | `<h1 class="sk-title"><span class="sk-burst"><span class="sk-hl">Line one</span><br><span class="sk-hl">Line two</span></span></h1>`. `sk-burst` (the tick marks) is optional. |
| Section heading | `<h2 class="sk-section">The learning loop</h2>` |
| Step panel | `<div class="sk-panel sk-teal">` + `<div class="sk-step"><span class="sk-num">2</span><span class="sk-label">Filter + focus</span></div>` + `<img src="icons/magnifier.svg" alt="">` + `<p>…</p>`. Add `sk-dashed` to highlight one step. |
| Step row | `<div class="sk-row">` panels with `<svg class="sk-arrow">` between them (copy from `index.html`). Panels share the width equally. |
| Loop-back arrow | `<svg class="sk-loop">` (copy from `index.html`). Put it under a step row. |
| Speech bubble | `<div class="sk-bubble">“…”</div>`. Add `sk-tail-right` to move the tail. |
| Ribbon banner | `<div class="sk-ribbon"><img src="icons/car.svg" alt=""><span class="sk-kicker">Insight:</span> …</div>` |
| Accent text | `<span class="sk-em">…</span>` inside a panel (step colour) or bubble (rust). |

**Colour modifiers:** `sk-mustard`, `sk-teal`, `sk-forest`, `sk-coral`, `sk-blue`, `sk-rust`, `sk-deep-teal`. The five-step sequence is always mustard → teal → forest → coral → blue.

## Images (use anywhere: slides, web, Google Slides, docs)

- `icons/`: books, magnifier, page-pencil, headphones, checklist, car, lightbulb. Thin wobbly ink over a watercolour wash.
- `characters/`: learner (headphones + book) and explainer (pointing). Chunky clean outline with a pastel wash.

Each SVG is self-contained, with its own effects, so it works as a plain `<img>`.

## Tokens

CSS variables in `sketchbook.css` (`var(--sk-mustard)`, `var(--sk-font-title)` and so on), also in `tokens.json`.

- **Colours:** mustard #EEA306, teal #039695, forest #4A7D4B, coral #F76C37, blue #1F78A8, slate #36545C (connector arrows), rust #D6631C, deep-teal #094854 (headings), highlighter #FFEEB8, paper #FCF9F3, ribbon #FAEED3, bubble #EEF4F5, ink #2A2724.
- **Fonts:** `--sk-font-title` Luckiest Guy (big titles, always capitals), `--sk-font-label` Patrick Hand SC (step labels, headings), `--sk-font-body` Patrick Hand (sentences).

## Rules of thumb

- One idea per slide: a title, then at most one row of panels or one bubble and one ribbon.
- Characters are supporting cast. Keep them small and at the edge, doing something, never the centrepiece.
- Pictures of things (books, headphones) beat pictures of people for explaining a step.
- Don't invent new colours. If you need more than five steps, reuse the sequence.
- Every outline wobbles, but only a little. Don't turn the wobble up.
