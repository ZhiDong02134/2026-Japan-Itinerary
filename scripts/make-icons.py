#!/usr/bin/env python3
"""Japan 2026 app icons and iPhone launch screens, in the same glass language as the Taiwan +
Hong Kong companion: a dark layered ground lit by two soft glows, a route arc with three stops,
and the landmark in the middle (Mt. Fuji with a torii, where Taiwan has Taipei 101).

Icons are full-bleed and opaque. iOS fills any transparency in apple-touch-icon with black and
applies its own rounded mask, so a pre-rounded icon shows black corners. Only the launch-screen
badge is rounded here, with a real mask, so no glow can spill outside it.

Run from anywhere:  python3 scripts/make-icons.py
"""
from __future__ import annotations
import math, random
from pathlib import Path
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
random.seed(23)


def hexrgb(value):
    value = value.lstrip('#')
    return tuple(int(value[i:i + 2], 16) for i in (0, 2, 4))


def glow(image, center, radius, color, alpha):
    layer = Image.new('RGBA', image.size, (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    x, y = center
    d.ellipse((x - radius, y - radius, x + radius, y + radius), fill=(*hexrgb(color), alpha))
    image.alpha_composite(layer.filter(ImageFilter.GaussianBlur(radius / 2.3)))


def vertical_fill(size, top, bottom):
    w, h = size
    grad = Image.new('RGBA', (1, h))
    a, b = hexrgb(top), hexrgb(bottom)
    for y in range(h):
        t = y / max(1, h - 1)
        grad.putpixel((0, y), tuple(round(a[i] + (b[i] - a[i]) * t) for i in range(3)) + (255,))
    return grad.resize((w, h))


def fuji_torii_mark(size=1024):
    s = size
    image = Image.new('RGBA', (s, s), hexrgb('#100E18') + (255,))
    glow(image, (s * .66, s * .30), s * .36, '#FF6F6A', 110)
    glow(image, (s * .28, s * .74), s * .34, '#6C6CF0', 92)
    draw = ImageDraw.Draw(image)
    # route arc with three stops, as on the Taiwan icon
    box = (s * .18, s * .20, s * .82, s * .84)
    draw.arc(box, 212, 520, fill='#5C5674', width=max(3, int(s * .012)))
    cx, cy = (box[0] + box[2]) / 2, (box[1] + box[3]) / 2
    rx, ry = (box[2] - box[0]) / 2, (box[3] - box[1]) / 2
    for ang, col in [(232, '#FFC2B8'), (330, '#F2B86F'), (430, '#FF7A6E')]:
        a = math.radians(ang % 360)
        x, y = cx + rx * math.cos(a), cy + ry * math.sin(a)
        r = s * .026
        draw.ellipse((x - r, y - r, x + r, y + r), fill=col)
    # Mt. Fuji: a glassy lavender cone with a flattened crater and a snow cap
    base_y, peak_y = s * .745, s * .375
    cone = [(s * .20, base_y), (s * .435, s * .415), (s * .47, peak_y), (s * .53, peak_y), (s * .565, s * .415), (s * .80, base_y)]
    mask = Image.new('L', (s, s), 0)
    ImageDraw.Draw(mask).polygon(cone, fill=255)
    body = vertical_fill((s, s), '#CBC5F2', '#5E5A99')
    image.paste(body, (0, 0), mask)
    # a faint sheen down the lit (right) flank
    sheen = Image.new('L', (s, s), 0)
    ImageDraw.Draw(sheen).polygon([(s * .53, peak_y), (s * .565, s * .415), (s * .80, base_y), (s * .66, base_y)], fill=46)
    image.paste(Image.new('RGBA', (s, s), (255, 255, 255, 255)), (0, 0), sheen)
    draw = ImageDraw.Draw(image)
    snow = [(s * .435, s * .415), (s * .47, peak_y), (s * .53, peak_y), (s * .565, s * .415),
            (s * .585, s * .447), (s * .558, s * .438), (s * .538, s * .466), (s * .515, s * .44),
            (s * .494, s * .47), (s * .474, s * .443), (s * .448, s * .462), (s * .415, s * .447)]
    draw.polygon(snow, fill='#F6F4FF')
    # torii in front of the mountain
    red, shade = '#FF6A5E', '#C9443C'
    tx, top = s * .5, s * .565
    half = s * .118
    # kasagi: the top lintel, ends swept up
    draw.polygon([(tx - half - s * .022, top - s * .012), (tx - half, top + s * .012), (tx + half, top + s * .012),
                  (tx + half + s * .022, top - s * .012), (tx + half * .55, top - s * .002), (tx - half * .55, top - s * .002)], fill=red)
    draw.rectangle((tx - half * .92, top + s * .012, tx + half * .92, top + s * .028), fill=shade)
    # nuki: the lower tie beam
    draw.rectangle((tx - half * .86, top + s * .062, tx + half * .86, top + s * .08), fill=red)
    # gakuzuka: the short post in the middle
    draw.rectangle((tx - s * .009, top + s * .028, tx + s * .009, top + s * .062), fill=red)
    # pillars, slightly splayed
    for side in (-1, 1):
        x0 = tx + side * half * .62
        draw.polygon([(x0 - s * .017, top + s * .028), (x0 + s * .017, top + s * .028),
                      (x0 + s * .021 + side * s * .006, base_y - s * .004), (x0 - s * .021 + side * s * .006, base_y - s * .004)], fill=red)
    # lake underline, as Taiwan's harbour line
    draw.rounded_rectangle((round(s * .28), round(s * .79), round(s * .72), round(s * .815)), radius=round(s * .012), fill='#C9C4F2')
    draw.rounded_rectangle((round(s * .39), round(s * .825), round(s * .61), round(s * .842)), radius=round(s * .008), fill='#FF9A8E')
    return image


def maskable_mark(size=1024):
    # Android crops maskable icons to the centre circle: shrink the art onto the same ground.
    ground = Image.new('RGBA', (size, size), hexrgb('#100E18') + (255,))
    glow(ground, (size * .66, size * .30), size * .36, '#FF6F6A', 110)
    glow(ground, (size * .28, size * .74), size * .34, '#6C6CF0', 92)
    art = fuji_torii_mark(size).resize((int(size * .8), int(size * .8)), Image.Resampling.LANCZOS)
    inset = (size - art.width) // 2
    ground.alpha_composite(art, (inset, inset))
    return ground


def rounded_badge(mark, size):
    badge = mark.resize((size, size), Image.Resampling.LANCZOS)
    big = Image.new('L', (size * 4, size * 4), 0)
    ImageDraw.Draw(big).rounded_rectangle((0, 0, size * 4 - 1, size * 4 - 1), radius=int(size * 4 * .225), fill=255)
    badge.putalpha(big.resize((size, size), Image.Resampling.LANCZOS))
    return badge


def font(size, kind='bold'):
    candidates = {
        'bold': ['/System/Library/Fonts/HelveticaNeue.ttc', '/System/Library/Fonts/Helvetica.ttc'],
        'regular': ['/System/Library/Fonts/HelveticaNeue.ttc', '/System/Library/Fonts/Helvetica.ttc'],
        'ja': ['/System/Library/Fonts/ヒラギノ角ゴシック W5.ttc', '/System/Library/Fonts/Hiragino Sans GB.ttc'],
    }[kind]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size, index=1 if kind == 'bold' and path.endswith('HelveticaNeue.ttc') else 0)
    raise SystemExit(f'No font found for {kind}: {candidates}')


def splash(width, height, mark):
    img = Image.new('RGBA', (width, height), hexrgb('#0C0B13') + (255,))
    glow(img, (width * .68, height * .35), min(width, height) * .45, '#FF6F6A', 70)
    glow(img, (width * .30, height * .68), min(width, height) * .42, '#6C6CF0', 52)
    icon_size = int(width * .25)
    x, y = (width - icon_size) // 2, int(height * .34 - icon_size * .5)
    img.alpha_composite(rounded_badge(mark, icon_size), (x, y))
    d = ImageDraw.Draw(img)
    title, sub = 'JAPAN 2026', '日本 · TRIP COMPANION'
    tf, sf = font(max(18, int(width * .040)), 'bold'), font(max(11, int(width * .021)), 'ja')
    ty = y + icon_size + int(width * .055)
    tw = d.textlength(title, font=tf)
    d.text(((width - tw) / 2, ty), title, font=tf, fill='#F3F1FA')
    sw = d.textlength(sub, font=sf)
    d.text(((width - sw) / 2, ty + int(width * .06)), sub, font=sf, fill='#A9A3C8')
    line_y = ty + int(width * .125)
    d.line((width * .31, line_y, width * .69, line_y), fill='#4A4560', width=max(1, int(width * .002)))
    for px, col in [(width * .31, '#FFC2B8'), (width * .50, '#F2B86F'), (width * .69, '#FF7A6E')]:
        r = max(2, int(width * .006))
        d.ellipse((px - r, line_y - r, px + r, line_y + r), fill=col)
    return img.convert('RGB')


if __name__ == '__main__':
    mark = fuji_torii_mark(1024)
    mask_mark = maskable_mark(1024)
    for name, size, art in [('apple-touch-icon.png', 180, mark), ('icon-192.png', 192, mark), ('icon-512.png', 512, mark),
                            ('icon-maskable-192.png', 192, mask_mark), ('icon-maskable-512.png', 512, mask_mark)]:
        art.resize((size, size), Image.Resampling.LANCZOS).convert('RGB').save(ROOT / name, optimize=True)
    for w, h in [(750, 1334), (828, 1792), (1080, 2340), (1125, 2436), (1170, 2532), (1179, 2556), (1206, 2622),
                 (1242, 2688), (1284, 2778), (1290, 2796), (1320, 2868)]:
        splash(w, h, mark).save(ROOT / f'splash-{w}x{h}.png', optimize=True)
    print('icons and launch screens written to', ROOT)
