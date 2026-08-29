# Generates the search and social cards for the GigFee guides.
#
# NOT part of the served site and nothing runs it automatically. Run it by
# hand when a guide's headline changes, then commit the PNGs it writes into
# assets/cards/. Windows only as written: it reads Arial from C:\Windows\Fonts,
# which is what assets/og-card.png was set in.
# Same palette and furniture as assets/og-card.png so a guide shared on
# Facebook and the landing page shared on Facebook look like one site.
#
# Three ratios per guide because Google's Article guidance asks for 16:9,
# 4:3 and 1:1 and picks whichever fits the surface.

import os
from PIL import Image, ImageDraw, ImageFont

SITE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT = os.path.join(SITE, "assets", "cards")
FONTS = r"C:\Windows\Fonts"

BOLD = os.path.join(FONTS, "arialbd.ttf")
REG = os.path.join(FONTS, "arial.ttf")

HERO_FROM = (43, 31, 112)   # --hero-from #2b1f70
HERO_TO = (22, 18, 47)      # --hero-to   #16122f
AMBER = (240, 160, 44)      # --amber
WHITE = (255, 255, 255)
BODY = (207, 201, 242)      # --hero-body

RATIOS = [("16x9", 1200, 675), ("4x3", 1200, 900), ("1x1", 1200, 1200)]


def gradient(w, h):
    """160deg linear gradient, matching the CSS on the hero."""
    base = Image.new("RGB", (w, h))
    px = base.load()
    # 160deg in CSS runs top-ish to bottom-ish, leaning left. Project each
    # pixel onto that axis and normalise.
    import math
    a = math.radians(160)
    dx, dy = math.sin(a), -math.cos(a)
    corners = [(0, 0), (w, 0), (0, h), (w, h)]
    proj = [x * dx + y * dy for x, y in corners]
    lo, hi = min(proj), max(proj)
    span = hi - lo
    for y in range(h):
        ybit = y * dy
        for x in range(w):
            t = (x * dx + ybit - lo) / span
            px[x, y] = (
                int(HERO_FROM[0] + (HERO_TO[0] - HERO_FROM[0]) * t),
                int(HERO_FROM[1] + (HERO_TO[1] - HERO_FROM[1]) * t),
                int(HERO_FROM[2] + (HERO_TO[2] - HERO_FROM[2]) * t),
            )
    return base


def tracked(draw, xy, text, font, fill, tracking):
    """PIL has no letter-spacing, so step the pen along by hand."""
    x, y = xy
    for ch in text:
        draw.text((x, y), ch, font=font, fill=fill)
        x += draw.textlength(ch, font=font) + tracking
    return x


def wrap(draw, text, font, width):
    lines, line = [], ""
    for word in text.split():
        trial = (line + " " + word).strip()
        if draw.textlength(trial, font=font) <= width or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    if line:
        lines.append(line)
    return lines


def fit(draw, text, path, width, max_lines, start, floor=34):
    """Largest size that still wraps into max_lines."""
    size = start
    while size > floor:
        font = ImageFont.truetype(path, size)
        lines = wrap(draw, text, font, width)
        if len(lines) <= max_lines:
            return font, lines
        size -= 2
    font = ImageFont.truetype(path, floor)
    return font, wrap(draw, text, font, width)


ICON = Image.open(os.path.join(SITE, "assets", "gigfee-icon.png")).convert("RGBA")


def rounded(img, size):
    """The launcher icon ships square. The site rounds it in CSS, so the
    card has to round it here or the two look like different apps."""
    img = img.resize((size, size), Image.LANCZOS)
    mask = Image.new("L", (size * 4, size * 4), 0)
    ImageDraw.Draw(mask).rounded_rectangle(
        [0, 0, size * 4 - 1, size * 4 - 1], radius=int(size * 4 * 0.225), fill=255)
    mask = mask.resize((size, size), Image.LANCZOS)
    out = img.copy()
    out.putalpha(mask)
    return out


def card(kicker, headline, subline, w, h, path):
    im = gradient(w, h)
    d = ImageDraw.Draw(im)
    pad = 80
    wide = h < w * 0.8          # the 16:9 card sets the icon beside the text
    im_w = w

    icon_px = 150 if wide else 170
    icon = rounded(ICON, icon_px)
    im.paste(icon, (w - pad - icon_px, pad), icon)

    text_w = w - pad * 2 - (icon_px + 40 if wide else 0)

    # Build the block before drawing any of it, so a tall card can centre
    # what it holds instead of stranding half a card of empty gradient.
    kf = ImageFont.truetype(BOLD, 25)
    hf, hlines = fit(d, headline, BOLD,
                     text_w, {675: 3, 900: 4, 1200: 4}[h],
                     {675: 76, 900: 82, 1200: 84}[h])
    sf = ImageFont.truetype(REG, 31 if wide else 34)
    slines = wrap(d, subline, sf, text_w)[:3]

    hlh, slh = int(hf.size * 1.16), int(sf.size * 1.42)
    block = 58 + len(hlines) * hlh + 26 + len(slines) * slh

    top = pad if wide else pad + icon_px + 40
    bottom = h - pad - 34 - 46
    y = top if wide else top + max(0, (bottom - top - block) // 2)

    tracked(d, (pad, y), kicker.upper(), kf, AMBER, 3.2)
    y += 58
    for ln in hlines:
        d.text((pad, y), ln, font=hf, fill=WHITE)
        y += hlh
    y += 26
    for ln in slines:
        d.text((pad, y), ln, font=sf, fill=BODY)
        y += slh

    # Footer: amber rule, wordmark, domain
    fy = h - pad - 34
    d.rectangle([pad, fy - 26, pad + 58, fy - 22], fill=AMBER)
    bf = ImageFont.truetype(BOLD, 26)
    endx = tracked(d, (pad, fy), "GIGFEE", bf, WHITE, 1.6)
    df = ImageFont.truetype(REG, 26)
    d.text((endx + 22, fy), "gigfee.tones-au.com", font=df, fill=BODY)

    im.save(path, "PNG", optimize=True)
    return path


GUIDES = [
    ("payday-super-for-musicians",
     "Super \u00b7 2026",
     "Payday super, explained for people who play for a living",
     "What changed on 1 July, and what it means for a $300 pub gig"),
    ("super-out-of-your-fee",
     "Your money",
     "The venue is taking 12% out of your fee",
     "What the law says about who wears the cost of super"),
    ("band-leader-super-and-splits",
     "Band leaders",
     "You invoice for the whole band. Who owes the super?",
     "The question nobody answered before 1 July, worked through"),
    ("super-details-a-venue-needs",
     "Get paid",
     "Five details a venue needs before it can pay your super",
     "Have these ready and the money lands. Miss one and it stalls"),
    ("your-structure-and-super",
     "Structures",
     "Sole trader, partnership or company: how each is treated",
     "Why the rules land differently, and what the industry wants"),
    ("guides-index",
     "GigFee guides",
     "Super, tax and invoicing for Australian musicians",
     "Plain answers to the paperwork nobody teaches at music school"),
]

os.makedirs(OUT, exist_ok=True)
for slug, kicker, headline, subline in GUIDES:
    for name, w, h in RATIOS:
        if slug == "guides-index" and name != "16x9":
            continue
        p = os.path.join(OUT, f"{slug}-{name}.png")
        card(kicker, headline, subline, w, h, p)
        print(f"{os.path.basename(p):48s} {os.path.getsize(p) // 1024:4d} KB")
