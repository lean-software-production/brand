# Brand

**Warm, whimsical, wise.** This is the Sketchbook brand for our slides, website, courses and posts.

- **Warm:** cream paper, soft pastel washes and friendly faces. Welcoming, never corporate.
- **Whimsical:** wobbly ink, marker lettering and lopsided doodles. The hand-drawn feel reminds us that people and collaboration matter.
- **Wise:** one idea at a time, in a clear order, with familiar images and everyday words. Explain jargon briefly when it's needed.

Titles use black marker capitals in Luckiest Guy on a pale-yellow highlighter swash, with burst tick marks; headings and step labels use Patrick Hand SC, and body text uses Patrick Hand. Use the [kit's colours and fonts](kit/README.md#tokens) rather than inventing new ones.

We design for light mode only: ink text on a paper page. The [bb theme](bb-theme/sketchbook/theme.css) stays light even when bb is set to dark mode.

**Accessibility.** Body text needs a contrast of at least 4.5:1 against what's behind it. Ours is 11.4:1 on paper. Put white numerals only on blue and forest (4.9:1), and ink numerals on mustard, coral and teal. White on those fails (2.1, 2.9 and 3.6:1). Mustard, coral and teal are not text colours on paper (2.0, 2.8 and 3.5:1). For text, mix them with ink: at least 45% ink for mustard and coral, and 30% for teal. The kit's `-text` colours already follow these rules. Never let colour carry meaning alone: a progress meter always has its count in words next to it.

Keep drawings easy to read at small sizes. Objects can overlap, but the object in front must hide the outlines behind it. Avoid visible lines crossing through another object; simplify the composition if the overlap gets cluttered.

## Voice and tone

We sound like a friendly, experienced colleague sitting next to you.

- **Warm:** talk to "you", and say "we" for us. Be kind and direct, never cutesy or salesy. Notice the effort, and cheer a small win in a few plain words ("That's your first Rule passing."). Never gush.
- **Whimsical:** the play lives in the pictures and the odd light line, never in instructions. One joke at most, and never at the reader's expense.
- **Wise:** one idea per sentence where you can. Say what to do, then why. Use everyday words. When jargon is needed, explain it in a few words the first time ("a Rule: one behaviour the spec describes"). When something is hard, say so.

**Headlines** are short statements or actions: "Check the work", "One Rule at a time". Don't write questions to tease, stack a colon and subtitle, or promise too much.

| Say | Rather than |
|---|---|
| Let's try the next Rule. | Proceed to the next step. |
| That didn't work yet. Here's what we saw. | Error: validation failed. |
| Three Examples hold now. | Amazing job!!! 🎉 |
| A spec is a written description of what the software should do. | Leverage specs to operationalise requirements. |
| You'll need a GitHub account. | Users must authenticate via GitHub. |

**Words we avoid:** leverage, utilise, synergy, seamless, robust, revolutionary, game-changing; "simply", "just", "easy" and "obviously", which make people feel slow when it's hard; "users" when we mean you; "please note"; unexplained acronyms; more than one exclamation mark. Our drawings do the job of emoji, so we rarely use emoji.

## What's in this repo

- [Brand guidelines deck](index.html): open in a browser and use the arrow keys. Published to GitHub Pages on every push to `main`.
- [Sketchbook kit](kit/): reusable CSS, icons and characters. [Browse the gallery](kit/index.html) or [read how to use it](kit/README.md).
- [bb theme](bb-theme/sketchbook/theme.css): the brand's paper, ink, teal and handwriting for the bb app. Copy `bb-theme/sketchbook/` into the folder `bb theme dir` prints, then run `bb theme set sketchbook`.
- [Decisions still to make](TODO.md).
- [Contributor guide](CONTRIBUTING.md): how to change the kit.

## Use the brand in another project

Copy the [brand skill](skill/lean-software-production-brand/SKILL.md) to `.claude/skills/lean-software-production-brand/SKILL.md` in your project.
