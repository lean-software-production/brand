# Contributing

## Changing the kit

Read [the drawing and kit guide](src/README.md) before drawing anything or changing the [kit](kit/). Edit the source in `src/`: everything in `kit/` except `kit/README.md` is generated. Rebuild with `python3 src/build_kit.py`, inspect the result, and commit the source and generated files together.

Keep outlines gently wobbly and drawings slightly asymmetrical. The shared SVG filter uses `feTurbulence` with `type="fractalNoise"`, `baseFrequency="0.035"`, `numOctaves="2"`, and `seed="3"`, followed by `feDisplacementMap` with `in="SourceGraphic"` and `scale="3.5"`. Chunky ~5px outlines use `baseFrequency="0.04"` and `scale="4.5"`. Set `filterUnits="userSpaceOnUse"` with enough room so straight lines don't get clipped.

Characters use a chunky 5px ink outline over a pastel watercolour wash at about 60% opacity, offset by 2px on opaque paper. Very dark colours stay around 88% opacity so they don't turn grey. Objects use thinner wobbly ink over an offset wash. Take colours and fonts from the [kit tokens](kit/README.md#tokens).
