"""Three one-off homepage illustrations, using the existing Sketchbook renderers.

Run with Python 3.12+: python3 src/build_factory_heroes.py
Importing build_kit also rebuilds the kit. These concepts deliberately live outside
kit/: they are proposals, not additions to the shared vocabulary.
"""
from pathlib import Path
import base64
import html
import json

import build_kit as brand
import characters
import icons

OUT = Path(__file__).resolve().parents[1] / "concepts" / "software-factory"
C = brand.C
INK = brand.INK


def group(body, x=0, y=0, scale=1, rotate=0):
    return f'<g transform="translate({x} {y}) scale({scale}) rotate({rotate})">{body}</g>'


def parts(items, x=0, y=0, scale=1, rotate=0):
    return group(icons.render(items, C, INK), x, y, scale, rotate)


def shape(d, color="paper"):
    # Use the same wobbled silhouette for the opaque cover and front outline.
    return parts([("front", d), (color, d)])


def line(d):
    return parts([(None, d)])


def wash(d, color="teal", opacity=.12):
    return f'<path d="{d}" fill="{C[color]}" opacity="{opacity}" filter="url(#sk-wash)"/>'


def circle(x, y, r):
    return f'M{x-r} {y} a{r} {r} 0 1 0 {2*r} 0 a{r} {r} 0 1 0 {-2*r} 0 Z'


def rect(x, y, w, h, r=8):
    return f'M{x+r} {y} H{x+w-r} Q{x+w} {y} {x+w} {y+r} V{y+h-r} Q{x+w} {y+h} {x+w-r} {y+h} H{x+r} Q{x} {y+h} {x} {y+h-r} V{y+r} Q{x} {y} {x+r} {y} Z'


def text(s, x, y, size=23, color="ink", anchor="middle"):
    return f'<text x="{x}" y="{y}" font-family="Patrick Hand SC" font-size="{size}" fill="{C[color]}" text-anchor="{anchor}">{html.escape(s)}</text>'


def arrow(d, end, color="blue", width=4):
    # Hand-drawn open arrowhead, rather than a geometric SVG marker.
    return f'<g fill="none" stroke="{C[color]}" stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round" filter="url(#w)"><path d="{d}"/><path d="{end}"/></g>'


def icon(name, x, y, s=1, rotate=0):
    # Standalone kit icons assume empty paper behind them. In a scene, each
    # coloured silhouette needs its own cover or conveyor lines show through.
    layered = []
    for color, d in icons.ICONS[name]:
        if color and color not in ('solid', 'front'):
            layered.append(('front', d))
        layered.append((color, d))
    return parts(layered, x, y, s, rotate)


def card(x, y, scale=1, kind="code", rotate=0):
    d = 'M4 4 L105 1 L108 79 L2 82 Z'
    body = shape(d, 'highlighter' if kind == 'idea' else 'paper')
    body += line('M5 20 L105 18')
    body += parts([('solid', circle(13, 12, 2)), ('solid', circle(22, 12, 2)), ('solid', circle(31, 11, 2))])
    if kind == 'idea':
        body += icon('lightbulb', 33, 22, .38)
    elif kind == 'done':
        body += shape('M13 30 H42 V68 H13 Z', 'teal')
        body += line('M52 32 L94 31 M52 43 L80 43 M52 68 L65 68')
        body += arrow('M69 58 L77 66 L96 47', '', 'forest', 4)
    else:
        body += line('M37 35 L22 49 L36 61 M72 34 L88 47 L75 60 M63 31 L52 66')
    return group(body, x, y, scale, rotate)


def robot(x, y, s=1, role="make"):
    # Familiar kit robot, with task-specific arms. The original face, antenna,
    # eye discs and body colours are unchanged.
    body = line('M43 116 Q20 109 13 130 M96 114 Q116 109 126 129')
    body += icon('robot', 0, 0)
    if role == 'make':
        body += card(4, 124, .86)
        body += shape(circle(19, 132, 7), 'slate')
        body += shape(circle(91, 134, 7), 'slate')
    else:
        body += card(2, 130, .68)
        # Opaque lens hides the arm and card beneath it.
        body += shape('M105 111 L126 135 L119 141 L98 119 Z', 'slate')
        body += shape(circle(91, 101, 22), 'bubble')
        body += arrow('M78 100 L88 109 L103 90', '', 'forest', 3)
        body += line('M78 88 Q82 83 90 82')
    return group(body, x, y, s)


def panel(x, y, s=1, label=True):
    body = shape(rect(0, 0, 148, 86), 'highlighter')
    body += shape(rect(11, 11, 76, 36, 3), 'bubble')
    body += line('M20 34 L31 34 L39 22 L49 36 L59 26 L78 26')
    body += shape(circle(115, 29, 16), 'paper')
    body += line('M115 29 L122 19')
    for xx, col in ((23, 'forest'), (47, 'mustard'), (71, 'coral')):
        body += shape(circle(xx, 63, 5), col)
    body += line('M103 55 V72 M116 55 V72 M110 55 V72 M123 55 V72')
    if label:
        body += text('ORCHESTRATOR', 74, -12, 20, 'deep-teal')
    return group(body, x, y, s)


def operator(x, y, s=.58, coffee=False):
    spec = characters.coffee if coffee else characters.explainer
    return group(characters.render(characters.person(spec), paper=C['paper']), x, y, s)


def spark(x, y, s=1):
    return group(line('M0 0 L-7 -12 M10 -3 L12 -19 M20 1 L30 -9'), x, y, s)


def ground():
    return wash('M75 557 C145 529 857 527 939 557 C997 596 825 615 495 608 C227 613 40 597 75 557 Z', 'mustard', .10)


def workshop():
    """A welcoming cutaway: the factory is visible, not a mysterious black box."""
    b = ground()
    # Factory shell and sawtooth skylights; intentionally unequal roof bays.
    b += shape('M210 226 L210 179 L377 104 L377 177 L548 103 L548 179 L720 114 L720 191 L864 190 L864 537 L210 537 Z', 'paper')
    b += shape('M201 231 L201 179 L378 98 L378 176 L548 97 L548 178 L720 108 L720 188 L872 186 L872 232 Z', 'teal')
    for d in ('M244 171 L354 121 L354 172 Z', 'M414 170 L526 120 L526 172 Z', 'M585 171 L698 127 L698 173 Z'):
        b += shape(d, 'bubble')
    b += line('M317 139 L317 173 M486 138 L486 172 M657 145 L657 173')
    # Open front: no rear outlines through the equipment.
    b += wash('M228 250 L846 248 L844 521 L226 522 Z', 'mustard', .07)
    b += line('M226 243 L226 527 M847 243 L847 526')
    b += shape('M191 527 L880 527 L901 546 L179 549 Z', 'slate')
    # Dispatch cables terminate at each machine, behind the equipment.
    b += line('M479 303 L448 303 L448 321 L384 321 L384 331 M596 303 L607 303 L607 318 L679 318 L679 326')
    b += panel(479, 263, .79)
    # Conveyor is opaque; rollers sit inside its front face.
    b += shape('M167 434 Q141 434 141 453 Q141 474 167 474 L911 474 Q932 474 932 453 Q932 434 911 434 Z', 'slate')
    b += line('M166 442 L910 442')
    for x in range(167, 921, 31):
        b += shape(circle(x, 457, 7), 'paper')
    b += line('M269 475 L260 524 M800 475 L811 525')
    b += robot(320, 294, .91, 'make')
    b += robot(616, 289, .91, 'check')
    b += text('MAKE', 382, 283, 25, 'deep-teal')
    b += text('CHECK', 682, 278, 25, 'deep-teal')
    b += card(172, 356, .89, 'idea', -7)
    b += card(487, 357, .80, 'code', 3)
    b += card(793, 347, 1.05, 'done', -4)
    b += arrow('M276 408 Q292 405 309 406', 'M300 397 L310 406 L300 414', 'slate', 3)
    b += arrow('M736 410 L770 410', 'M759 401 L771 410 L759 419', 'forest', 3)
    # A separate return rail makes the validator-to-doer feedback explicit.
    b += arrow('M685 478 C684 510 632 512 536 512 C451 512 381 514 380 479', 'M370 491 L380 478 L389 491', 'blue', 4)
    b += text('REFINE & TRY AGAIN', 536, 498, 22, 'blue')
    b += text('IDEA IN', 160, 341, 23, 'deep-teal')
    b += text('WORKING SOFTWARE', 825, 583, 22, 'forest')
    b += spark(892, 340, .8)
    # Human with a real control surface, not supervising every individual card.
    b += operator(4, 329, .59)
    b += shape('M134 454 L217 454 L226 535 L125 535 Z', 'teal')
    b += panel(126, 417, .67, False)
    b += text('YOU SET THE DIRECTION', 168, 591, 23, 'deep-teal')
    b += line('M164 568 Q154 556 151 547')
    b += icon('sprout', 879, 481, .55)
    return b


def carousel():
    """A compact production cell: the conveyor itself is the learning loop."""
    b = ground()
    # Foundation and legs give the loop a physical, tabletop presence.
    b += line('M281 500 L270 563 M771 500 L784 562 M414 536 L410 583')
    b += shape('M246 302 C316 203 665 207 791 295 C940 398 831 554 573 567 C340 579 155 500 179 392 Q190 340 246 302 Z', 'slate')
    b += shape('M244 280 C328 181 668 192 795 282 C935 380 829 532 576 548 C341 562 161 482 180 374 Q189 324 244 280 Z', 'teal')
    b += shape('M337 316 C405 268 601 265 692 315 C782 366 724 455 565 465 C412 476 296 430 299 379 Q301 342 337 316 Z', 'paper')
    # Visible front conveyor rollers, deliberately irregularly spaced.
    for x,y in ((221,455),(260,487),(308,512),(363,529),(423,543),(486,550),(548,551),(612,549),(675,539),(735,521),(785,497),(822,466)):
        b += shape(circle(x,y,6), 'paper')
    # Direction on the belt, including the prominent returning foreground path.
    b += arrow('M738 421 C715 493 490 528 338 469', 'M350 462 L336 469 L342 484', 'blue', 5)
    b += arrow('M230 405 Q214 355 255 319', 'M244 320 L257 317 L254 330', 'slate', 3)
    b += arrow('M464 239 Q550 234 603 254', 'M595 244 L605 255 L590 259', 'slate', 3)
    # Maker station, with a tiny sawtooth canopy: unmistakably a factory cell.
    b += shape('M269 196 L269 172 L328 143 L328 168 L388 142 L388 170 L443 171 L445 198 Z', 'mustard')
    b += line('M280 198 V314 M432 198 V314')
    b += robot(289, 186, 1.02, 'make')
    b += text('MAKE', 353, 129, 27, 'deep-teal')
    # Checker looks directly at the work travelling round the loop.
    b += shape('M644 266 L644 242 L700 213 L700 239 L758 215 L758 241 L811 242 L813 266 Z', 'teal')
    b += line('M652 268 V389 M804 268 V389')
    b += robot(654, 259, .99, 'check')
    b += text('CHECK', 723, 199, 27, 'deep-teal')
    # A short release spur branches only after validation.
    b += shape('M816 362 L950 358 L953 393 L813 400 Z', 'slate')
    for x in (836,862,889,919,944):
        b += shape(circle(x,383,5), 'paper')
    b += card(849, 283, .89, 'done', -4)
    b += arrow('M821 349 L842 347', 'M833 340 L844 347 L835 355', 'forest', 3)
    b += spark(935, 284, .75)
    b += text('READY', 902, 265, 23, 'forest')
    b += card(473, 210, .68, 'code', 8)
    b += card(200, 346, .76, 'idea', -13)
    b += text('IDEA IN', 174, 301, 23, 'deep-teal')
    # Central orchestration hub: routes a line, with dials visible to the human.
    b += line('M488 382 L427 349 M579 369 L639 361')
    b += shape('M467 376 L573 375 L584 451 L456 452 Z', 'teal')
    b += panel(452, 344, .88)
    b += text('FEEDBACK, NOT FINGERS CROSSED', 528, 609, 25, 'deep-teal')
    # A failed check returns a marked card; it is not a one-way assembly line.
    b += card(472, 475, .65, 'code', -9)
    b += shape(circle(541, 479, 12), 'highlighter')
    b += line('M537 473 L544 481 M544 473 L537 481')
    b += operator(18, 368, .57, coffee=True)
    b += shape('M144 464 L190 464 L195 548 L139 548 Z', 'mustard')
    b += shape(circle(167, 480, 10), 'paper')
    b += line('M167 480 L172 473 M151 506 H182')
    b += arrow('M174 452 L183 431', '', 'slate', 4)
    b += shape(circle(185, 425, 7), 'coral')
    return b


def laptop():
    """The factory is a power tool on your desk, not a replacement for you."""
    b = ground()
    # An open laptop is the factory enclosure; screen and keyboard are separate.
    b += shape('M220 139 Q219 114 245 114 L851 123 Q872 124 872 147 L855 479 L219 475 Z', 'slate')
    b += shape('M241 148 L845 156 L830 448 L241 445 Z', 'paper')
    b += parts([('solid', circle(546,136,3))])
    # A small roof edge inside the screen keeps the factory metaphor immediate.
    b += shape('M257 241 L257 218 L376 176 L376 210 L497 171 L497 211 L616 174 L616 213 L812 216 L811 246 Z', 'teal')
    b += line('M280 214 L353 188 L353 214 M405 213 L474 188 L474 214 M526 214 L593 190 L593 215')
    b += line('M265 253 L265 417 M808 254 L804 419')
    # Two independent agents inside the tool.
    b += robot(298, 244, .79, 'make')
    b += robot(620, 246, .79, 'check')
    b += text('MAKE', 352, 237, 20, 'deep-teal')
    b += text('CHECK', 677, 237, 20, 'deep-teal')
    # Labels live on the roof fascia, clear of the robots' antennae.
    b += shape('M273 394 L790 396 L789 415 L274 414 Z', 'slate')
    for x in range(285,790,25):
        b += shape(circle(x,406,4), 'paper')
    b += card(457, 313, .91, 'code', -3)
    b += arrow('M414 363 L444 363', 'M433 355 L445 363 L433 371', 'slate', 3)
    b += arrow('M565 363 L613 364', 'M602 356 L615 364 L602 372', 'slate', 3)
    b += arrow('M675 419 Q673 437 524 436 Q351 437 350 417', 'M343 425 L350 415 L357 425', 'blue', 3)
    b += text('CHECK. LEARN. REPEAT.', 522, 291, 21, 'blue')
    # Output exits the screen as an actual finished interface, not generic boxes.
    b += arrow('M798 357 C836 355 846 329 865 311', 'M852 315 L868 309 L864 325', 'forest', 4)
    b += card(865, 231, .89, 'done', 6)
    b += text('SOFTWARE', 920, 199, 19, 'forest')
    b += text('OUT', 920, 220, 19, 'forest')
    b += spark(930, 227, .7)
    # Seed card enters from outside the machine.
    b += card(104, 234, .84, 'idea', -9)
    b += text('YOUR INTENT', 148, 212, 23, 'deep-teal')
    b += arrow('M195 295 Q227 292 253 320', 'M250 305 L255 323 L239 316', 'slate', 3)
    # Keyboard is also the visibility/control surface. It sits in front of screen.
    b += shape('M219 475 L855 479 L939 563 Q943 578 917 582 L151 579 Q129 576 143 562 Z', 'slate')
    b += shape('M145 562 L936 563 L923 584 L154 581 Z', 'paper')
    b += shape('M254 486 L519 489 L542 540 L224 537 Z', 'paper')
    for y,w in ((499,267),(512,280),(525,289)):
        b += line(f'M246 {y} L{246+w} {y+3}')
    for x in range(268,519,27):
        b += line(f'M{x} 490 L{x-11} 536')
    b += shape('M392 547 L563 549 L578 563 L379 561 Z', 'bubble')
    b += panel(620, 485, .88, False)
    b += text('VISIBILITY + CONTROL', 684, 468, 21, 'deep-teal')
    # A person at the side of the tool, not trapped on its production line.
    b += operator(5, 388, .55, coffee=True)
    b += icon('sprout', 876, 488, .50)
    b += text('THE FACTORY WORKS. YOU STAY IN CHARGE.', 536, 630, 26, 'deep-teal')
    return b


CONCEPTS = [
    dict(slug='01-open-workshop', number='01', name='The open workshop',
         kicker='A factory you can see into',
         description='A light-filled cutaway. One agent makes, another checks, and unfinished work loops back. You set the direction from the control desk.',
         fit='The clearest first impression. A recognisable factory, without smokestacks or a black box.',
         alt='A cutaway software factory with maker and checker robots, an orchestrator, a blue feedback rail and a human at the controls. An idea enters on the left; checked software leaves on the right.', draw=workshop),
    dict(slug='02-quality-carousel', number='02', name='The quality carousel',
         kicker='Better with every lap',
         description='A small circular production cell. Code travels between maker and checker; feedback comes round again, while checked software takes the exit.',
         fit='The most playful direction. The loop is the picture, rather than an arrow added as an afterthought.',
         alt='A circular software-factory conveyor with maker and validator robots, a central orchestration console and a human beside a stop lever. A marked code card returns for another pass; approved software takes a separate exit.', draw=carousel),
    dict(slug='03-factory-in-your-hands', number='03', name='The factory in your hands',
         kicker='A power tool, not a replacement',
         description='An entire little factory inside an open laptop. Agents make and check the work; the controls stay on your side of the screen.',
         fit='The most direct link to software engineering. Compact, approachable and easy to place beside a homepage headline.',
         alt='An open laptop containing a miniature sawtooth-roof factory. Two agents make and check software in a feedback loop. A person stands beside the laptop, whose keyboard includes visible factory controls.', draw=laptop),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font = base64.b64encode((OUT / 'fonts/patrick-hand-sc.ttf').read_bytes()).decode()
    defs = (brand.filt('w', .035, 3.5, '-50 -50 1100 800') + brand.WASH + brand.CHAR_DEFS)
    for c in CONCEPTS:
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="700" viewBox="0 0 1000 700" role="img" aria-labelledby="title desc">'
               f'<title id="title">{html.escape(c["name"])}</title><desc id="desc">{html.escape(c["alt"])}</desc>'
               f'<defs>{defs}<style>@font-face{{font-family:"Patrick Hand SC";src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:400;font-style:normal}}text{{font-weight:400}}</style></defs>'
               f'<rect width="1000" height="700" fill="{C["paper"]}"/>{c["draw"]()}</svg>')
        (OUT / f'{c["slug"]}.svg').write_text(svg)
    manifest = [{k:v for k,v in c.items() if k != 'draw'} for c in CONCEPTS]
    (OUT / 'concepts.json').write_text(json.dumps(manifest, indent=2) + '\n')
    print('Factory heroes built:', ', '.join(c['slug'] for c in CONCEPTS))


if __name__ == '__main__':
    main()
