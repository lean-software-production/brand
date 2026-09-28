"""Three architectural variations on the selected open-workshop hero.

Python 3.12+: python3 src/build_workshop_variations.py
Uses the existing kit and first-round drawing helpers, without changing either.
"""
from pathlib import Path
import base64
import html
import json

from build_factory_heroes import (
    brand, C, arrow, card, circle, ground, icon, line, operator,
    panel, robot, shape, spark, text, wash,
)

OUT = Path(__file__).resolve().parents[1] / 'concepts/software-factory/workshop-variations'


def conveyor(x1, x2, y, height=34):
    r = height / 2
    b = shape(f'M{x1+r} {y} H{x2-r} Q{x2} {y} {x2} {y+r} Q{x2} {y+height} {x2-r} {y+height} H{x1+r} Q{x1} {y+height} {x1} {y+r} Q{x1} {y} {x1+r} {y} Z', 'slate')
    b += line(f'M{x1+17} {y+7} L{x2-17} {y+7}')
    for x in range(x1 + 20, x2 - 12, 29):
        b += shape(circle(x, y + r + 3, 5.5), 'paper')
    return b


def desk(x, y, s=.7):
    from build_factory_heroes import group
    b = shape('M9 68 L135 68 L141 145 L1 145 Z', 'teal')
    b += panel(0, 0, 1, False)
    return group(b, x, y, s)


def airy():
    """A pared-back, single-storey workshop, with more room around each action."""
    b = ground()
    b += shape('M216 250 L216 546 L864 546 L864 249 Z', 'paper')
    b += wash('M233 263 L849 263 L849 532 L234 532 Z', 'mustard', .09)
    b += shape('M202 544 L877 544 L898 561 L191 562 Z', 'slate')
    # Two generous roof bays instead of the original three.
    b += shape('M204 250 L204 207 L445 104 L445 204 L684 115 L684 207 L878 207 L878 251 Z', 'teal')
    b += shape('M248 202 L419 127 L419 202 Z', 'bubble')
    b += shape('M488 201 L658 139 L658 203 Z', 'bubble')
    b += line('M365 151 L365 202 M604 158 L604 203')
    b += line('M232 265 L232 536 M849 265 L849 536')
    # The orchestrator remains visible but does not demand another label.
    b += line('M484 304 L463 304 L463 343 L412 343 L412 356 M581 304 L603 304 L603 342 L692 342 L692 356')
    b += panel(484, 277, .66, False)
    b += text('MAKE', 411, 306, 25, 'deep-teal')
    b += text('CHECK', 694, 306, 25, 'deep-teal')
    # A pendant over the incoming brief adds a little workshop warmth.
    b += line('M272 252 L272 327')
    b += shape('M257 343 Q260 325 272 325 Q285 325 288 343 Z', 'mustard')
    b += line('M265 349 Q273 357 280 349')
    b += wash('M270 355 L231 407 L315 407 Z', 'mustard', .09)
    b += line('M313 526 L306 543 M794 526 L801 543')
    b += conveyor(211, 930, 490, 36)
    b += robot(342, 321, .97, 'make')
    b += robot(627, 321, .97, 'check')
    b += card(235, 414, .82, 'idea', -7)
    b += card(505, 421, .78, 'code', 3)
    b += card(814, 400, 1.03, 'done', -4)
    b += arrow('M765 466 L795 466', 'M785 458 L797 466 L785 474', 'forest', 3)
    b += spark(905, 391, .75)
    # The return route is separated from the conveyor, not drawn through it.
    b += arrow('M701 529 C700 580 415 581 412 529', 'M403 541 L412 528 L421 541', 'blue', 4)
    b += text('FEEDBACK', 555, 596, 24, 'blue')
    b += operator(22, 348, .61)
    b += desk(174, 461, .66)
    b += icon('sprout', 873, 521, .47)
    return b


def loft():
    """A compact two-storey cutaway with human direction on the control loft."""
    b = ground()
    b += shape('M248 215 L800 215 L800 561 L248 561 Z', 'paper')
    b += wash('M265 229 L783 229 L783 330 L265 330 Z', 'mustard', .13)
    b += wash('M265 361 L783 361 L783 551 L265 551 Z', 'mustard', .06)
    b += shape('M234 216 L234 173 L429 85 L429 171 L623 91 L623 174 L816 176 L816 218 Z', 'teal')
    b += shape('M276 168 L405 109 L405 168 Z', 'bubble')
    b += shape('M468 168 L599 115 L599 171 Z', 'bubble')
    b += line('M362 128 L362 168 M556 134 L556 170')
    b += shape('M232 559 L816 559 L839 576 L218 576 Z', 'slate')
    # Open loft, with a window and a real console rather than a supervisory cloud.
    b += shape('M665 242 L760 242 L760 311 L665 311 Z', 'bubble')
    b += line('M713 244 V310 M668 278 L758 278')
    b += operator(330, 202, .40, coffee=True)
    b += desk(473, 259, .54)
    b += text('YOU SET THE DIRECTION', 541, 248, 18, 'deep-teal')
    b += icon('sprout', 702, 290, .34)
    # Solid balcony fascia masks feet and console base behind it.
    b += shape('M247 333 L800 334 L800 351 L247 350 Z', 'mustard')
    b += line('M264 220 L264 332 M784 222 L784 333 M264 351 L264 554 M784 352 L784 554')
    # External stair: behind the input card and foreground conveyor.
    b += line('M134 561 L234 365 L247 365 M145 513 L145 489 L224 338 L247 338')
    for x,y in ((145,539),(158,516),(170,493),(182,470),(194,447),(206,424),(218,401),(230,378)):
        b += line(f'M{x} {y} h25 v15')
    # Two independent machines below the human's control deck.
    b += line('M517 351 L517 389 L377 389 L377 410 M517 389 L675 389 L675 410')
    b += text('MAKE', 377, 378, 24, 'deep-teal')
    b += text('CHECK', 675, 378, 24, 'deep-teal')
    b += line('M297 548 L288 557 M758 548 L767 557')
    b += conveyor(153, 930, 516, 34)
    b += robot(317, 386, .85, 'make')
    b += robot(615, 386, .85, 'check')
    b += card(174, 440, .86, 'idea', -6)
    b += card(476, 440, .80, 'code', 3)
    b += card(820, 427, 1.00, 'done', -3)
    b += arrow('M283 487 L307 487', 'M295 479 L308 487 L295 495', 'slate', 3)
    b += arrow('M737 484 L794 484', 'M782 476 L796 484 L782 492', 'forest', 3)
    b += spark(905, 420, .75)
    b += arrow('M675 554 C676 605 380 607 379 554', 'M370 565 L379 552 L388 565', 'blue', 4)
    b += text('FEEDBACK', 527, 622, 24, 'blue')
    return b


def corner():
    """A three-quarter cutaway: same open front, with a visible roof and side wall."""
    b = ground()
    # Side wall and three receding roof planes, drawn back to front.
    b += shape('M750 255 L860 145 L860 420 L750 530 Z', 'mustard')
    b += shape('M750 149 L860 39 L860 145 L750 255 Z', 'teal')
    # Each roof bay has both a sloping plane and a vertical return. Without
    # the returns, the receding peaks read as disconnected fins.
    b += shape('M380 143 L490 33 L490 99 L380 209 Z', 'bubble')
    b += shape('M565 138 L675 28 L675 95 L565 205 Z', 'bubble')
    b += shape('M210 216 L380 143 L490 33 L320 106 Z', 'teal')
    b += shape('M380 209 L565 138 L675 28 L490 99 Z', 'teal')
    b += shape('M565 205 L750 149 L860 39 L675 95 Z', 'teal')
    # Roof seams follow the same receding axis as the side wall.
    b += line('M266 192 L376 82 M442 185 L552 75 M627 186 L737 76')
    b += shape('M777 278 L835 220 L835 291 L777 349 Z', 'bubble')
    b += line('M806 250 V320 M779 313 L833 259')
    b += shape('M210 255 L750 255 L750 530 L210 530 Z', 'paper')
    b += wash('M226 268 L734 268 L734 518 L226 518 Z', 'mustard', .08)
    # The familiar sawtooth face, with uneven panes.
    b += shape('M201 257 L201 215 L381 139 L381 209 L566 133 L566 205 L751 144 L751 256 Z', 'teal')
    for d in ('M239 210 L358 158 L358 211 Z', 'M419 209 L542 156 L542 208 Z', 'M604 207 L728 165 L728 211 Z'):
        b += shape(d, 'bubble')
    b += line('M318 176 V210 M501 174 V208 M687 180 V210')
    b += line('M226 270 L226 521 M735 269 L735 519')
    b += shape('M750 530 L860 420 L878 438 L755 550 Z', 'slate')
    b += shape('M198 530 L751 530 L755 550 L186 550 Z', 'slate')
    b += line('M464 305 L441 305 L441 340 L374 340 M556 305 L561 305 L561 340 L621 340')
    b += panel(464, 277, .62, False)
    b += text('MAKE', 372, 299, 23, 'deep-teal')
    b += text('CHECK', 622, 299, 23, 'deep-teal')
    b += line('M291 484 L281 528 M753 484 L763 521')
    b += conveyor(165, 880, 450, 34)
    b += robot(311, 317, .87, 'make')
    b += robot(561, 317, .87, 'check')
    b += card(201, 377, .79, 'idea', -7)
    b += card(442, 378, .78, 'code', 3)
    b += card(769, 365, 1.00, 'done', -4)
    b += arrow('M691 428 L749 428', 'M738 420 L751 428 L738 436', 'forest', 3)
    b += spark(858, 357, .75)
    b += arrow('M625 488 C625 524 373 529 372 488', 'M363 500 L372 487 L381 500', 'blue', 4)
    b += text('FEEDBACK', 500, 509, 20, 'blue')
    b += operator(2, 336, .61)
    b += desk(132, 445, .68)
    b += icon('sprout', 849, 501, .49)
    return b


CONCEPTS = [
    dict(slug='01-airy-workshop', number='01', name='The airy workshop',
         kicker='Less diagram. More breathing room.',
         description='Two generous roof bays, a warm task light and fewer labels. The same make–check–feedback story, with more space around each part.',
         fit='Closest to the original. My pick for a homepage: the factory reads quickly and leaves the headline to do the explaining.',
         alt='An open, single-storey software workshop with two broad sawtooth skylights. Maker and checker robots work along a conveyor, connected to a small orchestration panel. A human stands at the controls; a blue feedback arrow returns work for improvement.', draw=airy),
    dict(slug='02-control-loft', number='02', name='The control loft',
         kicker='People direct. Agents get on with it.',
         description='A two-storey cutaway. Upstairs, a person sets direction at the controls. Downstairs, the agents make and check software, with feedback returning for another pass.',
         fit='The strongest picture of human agency. A taller, compact silhouette with a little architectural character.',
         alt='A two-storey, sawtooth-roof software factory with an external stair. A human with a mug operates a console in the open loft. Below, maker and checker robots work on a conveyor with a blue feedback loop.', draw=loft),
    dict(slug='03-corner-workshop', number='03', name='The corner workshop',
         kicker='The same workshop, with another dimension.',
         description='A three-quarter cutaway with a receding roof, a sunlit side wall and an open front. The production line stays simple and visible.',
         fit='The most architectural direction. More sense of place, without turning the factory into a mysterious black box.',
         alt='A three-quarter view of an open software workshop with a teal sawtooth roof, a warm side wall and a window. A human controls a visible make-and-check line; a blue feedback arrow loops back beneath the conveyor.', draw=corner),
]


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    font = base64.b64encode((OUT.parent / 'fonts/patrick-hand-sc.ttf').read_bytes()).decode()
    defs = brand.filt('w', .035, 3.5, '-50 -50 1100 800') + brand.WASH + brand.CHAR_DEFS
    for c in CONCEPTS:
        svg = (f'<svg xmlns="http://www.w3.org/2000/svg" width="1000" height="700" viewBox="0 0 1000 700" role="img" aria-labelledby="title desc">'
               f'<title id="title">{html.escape(c["name"])}</title><desc id="desc">{html.escape(c["alt"])}</desc>'
               f'<defs>{defs}<style>@font-face{{font-family:"Patrick Hand SC";src:url(data:font/ttf;base64,{font}) format("truetype");font-weight:400;font-style:normal}}text{{font-weight:400}}</style></defs>'
               f'<rect width="1000" height="700" fill="{C["paper"]}"/>{c["draw"]()}</svg>')
        (OUT / f'{c["slug"]}.svg').write_text(svg)
    (OUT / 'concepts.json').write_text(json.dumps([{k:v for k,v in c.items() if k != 'draw'} for c in CONCEPTS], indent=2) + '\n')
    print('Workshop variations built:', ', '.join(c['slug'] for c in CONCEPTS))


if __name__ == '__main__':
    main()
