"""Build-time renderer for entry.png (needs Pillow; main.py itself is stdlib-only and just copies the PNG).

Run: python3 build.py  -> writes entry.png (1024x1024)
"""
from PIL import Image, ImageDraw, ImageFont

S = 2  # supersample, downscaled at the end for clean anti-aliasing
W = H = 1024
FD = '/usr/share/fonts/truetype/noto/'

img = Image.new('RGB', (W * S, H * S), '#f4efe4')
d = ImageDraw.Draw(img)


def F(name, size):
    return ImageFont.truetype(FD + name + '.ttf', round(size * S))


SERIF = lambda s: F('NotoSerif-CondensedBlack', s)
XB = lambda s: F('NotoSans-CondensedExtraBold', s)
BOLD = lambda s: F('NotoSans-CondensedBold', s)
MED = lambda s: F('NotoSans-CondensedMedium', s)

NAVY, GOLD, INK, PAPER = '#14213d', '#fca311', '#1b1b1b', '#fffdf8'
CAT = {  # category -> colour
    'CONFLICT': '#c0392b', 'POLITICS': '#2c5aa0', 'ECONOMY': '#1e8449', 'SPORT': '#d35400',
    'CULTURE': '#7d3c98', 'SCIENCE': '#148f9f', 'SOCIETY': '#8a6d1f',
}


def text(g, x, y, s, font, fill, anchor='la'):
    g.text((x * S, y * S), s, font=font, fill=fill, anchor=anchor)


def rect(g, x0, y0, x1, y1, fill=None, outline=None, width=1, r=0):
    g.rounded_rectangle([x0 * S, y0 * S, x1 * S, y1 * S], radius=r * S, fill=fill,
                        outline=outline, width=round(width * S))


def poly(g, pts, fill, outline=None, width=1):
    g.polygon([(x * S, y * S) for x, y in pts], fill=fill, outline=outline, width=round(width * S))


def circ(g, x, y, r, fill, outline=None, width=1):
    g.ellipse([(x - r) * S, (y - r) * S, (x + r) * S, (y + r) * S], fill=fill, outline=outline,
              width=round(width * S))


def line(g, pts, fill, width):
    g.line([(x * S, y * S) for x, y in pts], fill=fill, width=round(width * S), joint='curve')


def wrap(s, font, maxw, maxlines):
    lines, cur = [], ''
    for w in s.split():
        t = (cur + ' ' + w).strip()
        if d.textlength(t, font=font) <= maxw * S:
            cur = t
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    assert len(lines) <= maxlines, (s, lines)  # self-check: no text overflows its box
    return lines


def gradient(g, w, h, top, bottom, y0=0, y1=None):
    y1 = h if y1 is None else y1
    t0, t1 = [int(top[i:i + 2], 16) for i in (1, 3, 5)], [int(bottom[i:i + 2], 16) for i in (1, 3, 5)]
    for y in range(y0 * S, y1 * S):
        k = (y - y0 * S) / max(1, (y1 - y0) * S - 1)
        g.line([(0, y), (w * S, y)], fill=tuple(round(a + (b - a) * k) for a, b in zip(t0, t1)))


def label(g, x, y, s):
    f = XB(11)
    tw = g.textlength(s, font=f) / S
    rect(g, x, y, x + tw + 12, y + 17, fill=(0, 0, 0, 170), r=3)
    text(g, x + 6, y + 8.5, s, f, 'white', 'lm')


# ---------------------------------------------------------------- hero scenes
def scene_libya(g, w, h):
    gradient(g, w, h, '#f6bd60', '#7b4b6e', 0, 92)
    rect(g, 0, 92, w, h, fill='#1d3557')
    rect(g, 0, 80, 64, 94, fill='#2b2d42')  # quay
    line(g, [(20, 80), (20, 50), (44, 50)], '#2b2d42', 3)  # crane
    line(g, [(44, 50), (44, 64)], '#2b2d42', 1.5)
    for (x, y, r) in [(150, 52, 22), (172, 36, 17), (132, 30, 15), (160, 16, 12)]:
        circ(g, x, y, r, '#5f6670')
    # warship heeled over and settling by the bow: grey hull, mast and gun still visible
    poly(g, [(70, 112), (212, 80), (220, 92), (92, 126)], '#59606e')
    poly(g, [(70, 112), (212, 80), (214, 85), (73, 117)], '#9b2226')  # red keel showing
    poly(g, [(120, 102), (156, 94), (150, 70), (128, 76)], '#6c7584')  # superstructure
    line(g, [(140, 74), (132, 46)], '#3c4250', 2.5)  # mast
    line(g, [(127, 56), (140, 52)], '#3c4250', 2)
    line(g, [(184, 88), (204, 70)], '#3c4250', 3)  # gun barrel
    rect(g, 0, 112, w, h, fill=(29, 53, 87, 150))  # water over the sunk side
    circ(g, 150, 84, 11, '#ff7b00')
    circ(g, 150, 86, 6, '#ffd166')
    for bx, by in [(28, 128), (52, 138)]:  # sea drones and their wakes
        poly(g, [(bx, by), (bx + 16, by - 3), (bx + 16, by + 3)], '#111111')
        line(g, [(bx - 26, by - 7), (bx, by)], '#cfe8ff', 1.5)
        line(g, [(bx - 26, by + 7), (bx, by)], '#cfe8ff', 1.5)
    label(g, 6, h - 24, 'BENGHAZI, LIBYA')


def scene_cop(g, w, h):
    gradient(g, w, h, '#2a9d8f', '#1d3a46')
    for sx in (14, 32):  # smokestacks: the fossil-fuel split
        rect(g, sx, 98, sx + 10, h, fill='#22303c')
    for (x, y, r) in [(22, 88, 8), (30, 76, 10), (42, 62, 12)]:
        circ(g, x, y, r, '#8d99ae')
    circ(g, 128, 70, 54, '#4ea8de', outline='#d8f3ff', width=2)
    for (x, y, rx, ry) in [(108, 52, 20, 14), (148, 80, 18, 22), (116, 96, 12, 9), (150, 44, 10, 7)]:
        g.ellipse([(x - rx) * S, (y - ry) * S, (x + rx) * S, (y + ry) * S], fill='#80b918')
    line(g, [(128, 16), (122, 40), (134, 58), (120, 80), (132, 100), (126, 124)], '#1b1b1b', 3)
    # rotated NO DEAL stamp
    st = Image.new('RGBA', (150 * S, 44 * S), (0, 0, 0, 0))
    sg = ImageDraw.Draw(st)
    rect(sg, 2, 2, 148, 42, outline='#e63946', width=4, r=4)
    text(sg, 75, 22, 'NO DEAL', XB(26), '#e63946', 'mm')
    st = st.rotate(14, resample=Image.BICUBIC, expand=True)
    g._image.paste(st, (round(108 * S), round(50 * S)), st)
    label(g, 6, h - 24, 'COP31 · ANTALYA, TÜRKIYE')


def scene_hormuz(g, w, h):
    gradient(g, w, h, '#ffd6a5', '#e98a5a', 0, 96)
    rect(g, 0, 96, w, h, fill='#264653')
    for (x, y, r) in [(96, 70, 16), (88, 50, 19), (98, 28, 22), (82, 8, 20)]:
        circ(g, x, y, r, '#3a3a3a')
    poly(g, [(36, 96), (204, 96), (194, 114), (46, 114)], '#2f2f3a')  # tanker hull
    rect(g, 40, 92, 200, 97, fill='#7a2e2e')
    rect(g, 172, 74, 192, 93, fill='#f1f1f1')
    rect(g, 178, 66, 184, 75, fill='#d62828')
    circ(g, 98, 88, 11, '#ff7b00')
    circ(g, 98, 90, 6, '#ffd166')
    # MQ-1-style drone, struck
    dx, dy = 196, 34
    line(g, [(dx - 22, dy), (dx + 16, dy)], '#222', 3)
    line(g, [(dx - 4, dy - 15), (dx - 4, dy + 15)], '#222', 2.5)
    line(g, [(dx + 14, dy), (dx + 20, dy - 7)], '#222', 2)
    line(g, [(dx + 14, dy), (dx + 20, dy + 7)], '#222', 2)
    line(g, [(dx - 30, dy - 9), (dx - 16, dy + 9)], '#d62828', 3)
    line(g, [(dx - 30, dy + 9), (dx - 16, dy - 9)], '#d62828', 3)
    circ(g, 58, 128, 8, '#111')  # naval mine
    for ax, ay in [(-11, 0), (11, 0), (0, -11), (-8, -8), (8, -8)]:
        line(g, [(58, 128), (58 + ax, 128 + ay)], '#111', 2)
    label(g, 6, h - 24, 'STRAIT OF HORMUZ')


def scene_tennis(g, w, h):
    rect(g, 0, 0, w, h, fill='#1f4e8c')
    rect(g, 14, 14, w - 14, h - 14, outline='#e9f1fb', width=2)
    line(g, [(w / 2, 14), (w / 2, h - 14)], '#e9f1fb', 2)
    # trophy
    poly(g, [(98, 26), (150, 26), (144, 64), (130, 78), (118, 78), (104, 64)], '#d9dde3', outline='#8d99ae', width=1.5)
    line(g, [(98, 32), (86, 36), (90, 54), (104, 60)], '#d9dde3', 4)
    line(g, [(150, 32), (162, 36), (158, 54), (144, 60)], '#d9dde3', 4)
    rect(g, 120, 78, 128, 98, fill='#c9ced6')
    rect(g, 106, 98, 142, 110, fill='#b5bcc6', r=2)
    poly(g, [(108, 30), (116, 30), (112, 60)], '#ffffff')
    # racket
    g.ellipse([42 * S, 38 * S, 82 * S, 92 * S], outline='#fca311', width=4 * S)
    for k in range(1, 6):
        line(g, [(42 + k * 6.7, 42), (42 + k * 6.7, 88)], '#ffe8b0', 0.8)
        line(g, [(44, 38 + k * 9), (80, 38 + k * 9)], '#ffe8b0', 0.8)
    line(g, [(62, 92), (62, 124)], '#2b2d42', 6)
    circ(g, 184, 92, 13, '#d4e157')
    g.arc([173 * S, 80 * S, 197 * S, 104 * S], 300, 60, fill='white', width=2 * S)
    g.arc([171 * S, 80 * S, 195 * S, 104 * S], 120, 240, fill='white', width=2 * S)
    label(g, 6, h - 24, 'TURIN · ATP FINALS')


def paste_scene(fn, x, y, w, h):
    sc = Image.new('RGB', (w * S, h * S), 'white')
    g = ImageDraw.Draw(sc, 'RGBA')
    g._image = sc
    fn(g, w, h)
    img.paste(sc, (x * S, y * S))


# ---------------------------------------------------------------- header
rect(d, 0, 0, 1024, 100, fill=NAVY)
text(d, 22, 15, 'THE WORLD IN ONE PAGE  ·  DAILY NEWS SUMMARY', BOLD(14), GOLD)
text(d, 20, 60, 'SUNDAY 22 NOVEMBER 2026', SERIF(48), 'white', 'lm')
text(d, 1004, 30, '24 stories · 5 continents', XB(20), GOLD, 'rm')
text(d, 1004, 55, 'Events that happened or were first', MED(14), '#dfe6f0', 'rm')
text(d, 1004, 74, 'reported on 22 Nov 2026 (any time zone)', MED(14), '#dfe6f0', 'rm')
rect(d, 0, 100, 1024, 104, fill=GOLD)

# ---------------------------------------------------------------- hero stories
HEROES = [
    (scene_libya, 'CONFLICT', 'WAR · LIBYA / UKRAINE', 'Russian warship sunk by sea drones in Libya',
     'Corvette Merkury capsizes at Benghazi naval base; ~10 hurt. Ukraine claims the strike.'),
    (scene_cop, 'SCIENCE', 'CLIMATE · TÜRKIYE', 'COP31 climate summit collapses without a deal',
     'Longest COP ends split over fossil fuels: first breakdown since Copenhagen 2009.'),
    (scene_hormuz, 'CONFLICT', 'IRAN · GULF', 'Iran says 2 tankers hit mines in Strait of Hormuz',
     'IRGC says two "violating" supertankers exploded; it also claims a US MQ-1 drone shot down.'),
    (scene_tennis, 'SPORT', 'TENNIS · ITALY', 'Alcaraz wins his first ATP Finals title',
     'Beats world No. 1 Alexander Zverev 6-2, 7-6 in the Turin final.'),
]
HX = [16 + i * 250 for i in range(4)]
for i, (fn, cat, tag, title, summ) in enumerate(HEROES):
    x, y = HX[i], 112
    rect(d, x, y, x + 242, 390, fill=PAPER, outline='#d6cfc0')
    paste_scene(fn, x, y, 242, 146)
    circ(d, x + 228, y + 14, 11, NAVY, outline='white', width=1.5)
    text(d, x + 228, y + 14, str(i + 1), XB(13), 'white', 'mm')
    rect(d, x, y + 146, x + 242, y + 150, fill=CAT[cat])
    text(d, x + 8, y + 158, tag, XB(12), CAT[cat])
    for k, ln in enumerate(wrap(title, XB(20), 228, 2)):
        text(d, x + 8, y + 174 + k * 23, ln, XB(20), INK)
    for k, ln in enumerate(wrap(summ, MED(14), 228, 3)):
        text(d, x + 8, y + 224 + k * 17, ln, MED(14), '#333')

# ---------------------------------------------------------------- grid stories (numbers 5..24)
GRID = [  # (category, tag, headline, two-line summary, lon, lat)
    ('POLITICS', 'USA · IRAN', 'Trump: Iran strikes may resume', 'Tells Fox he is inclined to strike in the new year if there is no deal.', -77.0, 38.9),
    ('CONFLICT', 'SAUDI ARABIA', 'Houthi missile intercepted', 'Saudi-led coalition downs ballistic missile aimed at the western region.', 39.8, 21.4),
    ('ECONOMY', 'MARKETS · GULF', 'Saudi stocks slide 1.95%', 'TASI closes at 9,960, below 10,000, on regional security fears.', 46.7, 24.7),
    ('CONFLICT', 'BAHRAIN', 'Bahrain: 2 hurt in Iran strike', 'IRGC says its attacks on Bahrain targeted US Patriot sites.', 50.5, 26.1),
    ('CONFLICT', 'SUDAN', 'Drones hit Khartoum', 'Four killed; a UN building is damaged with staff inside.', 32.5, 15.6),
    ('CONFLICT', 'UKRAINE', 'Drone hits flats near Kyiv', 'Four killed in Dymer; Russian strike on Vyshneve supermarket kills 3.', 30.3, 50.8),
    ('CONFLICT', 'WEST BANK', 'Settlers torch cars by Ramallah', 'Israeli police open arson probe; Eisenkot calls it "Jewish terror".', 35.2, 31.9),
    ('ECONOMY', 'CHINA · USA', 'Beijing slams US phone rule', 'Urges FCC to revoke US-number ban on Chinese telecom carriers.', 116.4, 39.9),
    ('POLITICS', 'SOUTH KOREA', 'Education minister resigns', 'Quits over rushed anti-AI-cheating rules for the Suneung exam.', 127.0, 37.5),
    ('SOCIETY', 'BANGLADESH', 'Garment wage protest', 'Police fire tear gas in Gazipur; 19 closed factories reopen.', 90.4, 24.0),
    ('SOCIETY', 'INDIA', '12 dead in Rajasthan crashes', 'Pilgrim vehicle hits parked truck near Kota; 3 die near Jodhpur.', 75.8, 25.2),
    ('POLITICS', 'USA', 'Democrat unseats Foxx in N.C.', 'Hubbard win lifts House Democrats to at least 258 seats.', -81.0, 36.2),
    ('CULTURE', 'VATICAN', 'Pope Leo appeals for peace', 'Shares lunch with 1,300 poor people on Christ the King Sunday.', 12.5, 41.9),
    ('SCIENCE', 'SPACE · USA', 'SpaceX sets 32-hour pad record', 'Falcon 9 launches NROL-136 spy satellite from Vandenberg.', -120.6, 34.7),
    ('CULTURE', 'FILM · TAIWAN', 'Golden Horse best film', "Hong Kong's 'We Are Born Good' takes top prize in Taipei.", 121.5, 25.0),
    ('SPORT', 'MOTOGP · PORTUGAL', "Márquez's 8th MotoGP title", "Equals Agostini's record; Bezzecchi wins at Portimão.", -8.5, 37.1),
    ('SPORT', 'F1 · USA', 'Verstappen wins Las Vegas GP', 'Beats McLaren pair Norris and Piastri in the night race.', -115.2, 36.2),
    ('SPORT', 'CRICKET · NEW ZEALAND', 'India declare on 720 for 9', 'Highest away Test total; Pant hits a century in Wellington.', 174.8, -41.3),
    ('SPORT', 'FOOTBALL · ENGLAND', 'Liverpool 4-0 Man United', 'Ten-man United routed at Anfield in the Premier League.', -3.0, 53.4),
    ('SOCIETY', 'THAILAND', 'Floods hit Phatthalung', 'Man, 87, found dead in floodwater; flash-flood alert for 11 districts.', 100.1, 7.6),
]
assert len(GRID) == 20
GY0, RH = 638, 72
for n, (cat, tag, head, summ, _, _) in enumerate(GRID):
    col, row = n % 4, n // 4
    x, y = HX[col], GY0 + row * RH
    rect(d, x, y, x + 242, y + 68, fill=PAPER, outline='#ddd5c4')
    rect(d, x, y, x + 5, y + 68, fill=CAT[cat])
    text(d, x + 12, y + 4, f'{n + 5}  {tag}', XB(11), CAT[cat])
    assert d.textlength(head, font=XB(16)) <= 224 * S, head
    text(d, x + 12, y + 17, head, XB(16), INK)
    for k, ln in enumerate(wrap(summ, MED(12.5), 224, 2)):
        text(d, x + 12, y + 38 + k * 14.5, ln, MED(12.5), '#3a3a3a')

# ---------------------------------------------------------------- world map band
MX0, MY0, MW, MH = 16, 398, 662, 232
LON0, LON1, LAT0, LAT1 = -132, 184, 65, -45


def proj(lon, lat):
    return (lon - LON0) * MW / (LON1 - LON0), (LAT0 - lat) * MH / (LAT0 - LAT1)


LAND = [
    [(-168, 66), (-140, 70), (-110, 72), (-85, 70), (-75, 62), (-60, 55), (-55, 50), (-66, 45), (-70, 42), (-76, 35),
     (-81, 31), (-80, 25), (-84, 30), (-90, 29), (-97, 27), (-97, 21), (-92, 18), (-87, 21), (-88, 15), (-83, 9),
     (-79, 8), (-86, 12), (-92, 14), (-105, 20), (-110, 23), (-112, 30), (-117, 33), (-124, 40), (-124, 48),
     (-133, 56), (-150, 60), (-165, 62)],
    [(-55, 60), (-43, 60), (-20, 70), (-20, 80), (-60, 82), (-70, 76), (-55, 68)],
    [(-80, 8), (-72, 12), (-60, 10), (-50, 0), (-35, -6), (-39, -15), (-48, -26), (-58, -35), (-65, -42), (-68, -52),
     (-72, -50), (-74, -40), (-71, -30), (-70, -18), (-76, -14), (-81, -5), (-78, 2)],
    [(-10, 36), (-9, 43), (-2, 44), (-5, 48), (0, 50), (5, 53), (8, 57), (5, 62), (15, 69), (28, 71), (40, 67),
     (60, 69), (80, 73), (105, 78), (140, 72), (180, 68), (180, 65), (160, 60), (142, 53), (135, 44), (129, 35),
     (122, 40), (121, 31), (118, 24), (108, 21), (106, 10), (100, 13), (99, 8), (103, 1), (98, 8), (97, 16), (92, 22),
     (88, 22), (80, 15), (77, 8), (73, 20), (67, 25), (57, 26), (56, 27), (51, 29), (48, 30), (50, 26), (56, 24),
     (59, 22), (55, 17), (44, 12), (40, 20), (35, 28), (34, 31), (36, 36), (28, 36), (26, 40), (23, 37), (20, 40),
     (13, 46), (16, 41), (12, 38), (8, 44), (3, 43), (-5, 36)],
    [(-17, 21), (-17, 15), (-8, 5), (5, 5), (9, 4), (9, -1), (13, -12), (12, -18), (18, -34), (26, -34), (33, -26),
     (35, -20), (40, -15), (40, -3), (51, 11), (43, 11), (38, 17), (33, 27), (32, 31), (20, 31), (10, 37), (0, 36),
     (-6, 36), (-10, 30)],
    [(-5, 50), (1, 51), (0, 53), (-2, 56), (-4, 58), (-6, 57), (-5, 54), (-3, 53)],
    [(130, 31), (135, 34), (140, 35), (142, 40), (141, 45), (144, 43), (140, 38), (136, 36), (131, 34)],
    [(114, -22), (122, -18), (130, -12), (137, -12), (142, -11), (146, -19), (153, -26), (150, -37), (141, -38),
     (135, -34), (129, -32), (116, -35), (114, -26)],
    [(95, 5), (106, -6), (104, -5), (98, 0)],
    [(109, 1), (117, 7), (119, 0), (116, -4), (110, -3)],
    [(105, -6), (114, -7), (114, -8), (105, -7)],
    [(131, -1), (141, -3), (150, -10), (141, -9), (137, -5)],
    [(44, -25), (50, -15), (49, -12), (43, -22)],
    [(172, -35), (178, -38), (174, -41), (168, -46), (172, -42)],
]
def scene_map(g, w, h):  # drawn in its own image so land is clipped to the box
    rect(g, 0, 0, w, h, fill='#d9e6ef')
    for p in LAND:
        poly(g, [proj(lon, lat) for lon, lat in p], '#cbc3ae', outline='#b3aa92', width=0.8)
    pins = [(20.1, 32.1, 'CONFLICT'), (30.7, 36.9, 'SCIENCE'), (56.3, 26.6, 'CONFLICT'), (7.7, 45.1, 'SPORT')]
    pins += [(lon, lat, cat) for cat, _, _, _, lon, lat in GRID]
    for lon, lat, cat in pins:
        px, py = proj(lon, lat)
        circ(g, px, py, 5.5, CAT[cat], outline='white', width=1.5)
    rect(g, 8, 8, 168, 28, fill=NAVY, r=3)
    text(g, 16, 18, 'WHERE IT HAPPENED', XB(13), 'white', 'lm')
    rect(g, 8, 118, 86, 224, fill=(255, 255, 255, 200), r=3)
    for k, (cat, col) in enumerate(CAT.items()):  # legend, over the empty Pacific
        circ(g, 18, 128 + k * 15, 5, col, outline='white', width=1)
        text(g, 28, 128 + k * 15, cat.title(), BOLD(12), '#26313f', 'lm')
    rect(g, 0, 0, w, h, outline='#b8c7d3')


paste_scene(scene_map, MX0, MY0, MW, MH)

# ---------------------------------------------------------------- numbers box
NX0, NX1 = 686, 1008
rect(d, NX0, MY0, NX1, MY0 + MH, fill=NAVY)
text(d, NX0 + 14, MY0 + 18, 'THE DAY IN NUMBERS', XB(15), GOLD, 'lm')
NUMS = [
    ('720/9d', "India's highest away Test total"),
    ('-1.95%', 'Saudi TASI, closing at 9,960'),
    ('8', "MotoGP titles: Márquez equals Agostini"),
    ('32 h', 'SpaceX launch-pad turnaround record'),
    ('258+', 'US House seats now held by Democrats'),
]
for k, (big, lab) in enumerate(NUMS):
    y = MY0 + 50 + k * 39
    text(d, NX0 + 14, y, big, XB(25), GOLD, 'lm')
    text(d, NX0 + 108, y, lab, MED(13), '#eef2f8', 'lm')
    assert d.textlength(lab, font=MED(13)) <= (NX1 - NX0 - 116) * S, lab
    if k:
        line(d, [(NX0 + 14, y - 19.5), (NX1 - 14, y - 19.5)], '#2f3f63', 1)

# ---------------------------------------------------------------- footer
text(d, 16, 1015, 'Sources: Reuters · AP · AFP · CNN · Al Jazeera · ATP Tour · Formula1.com · ESPNcricinfo · Vatican News · '
     'Space.com · Focus Taiwan · The Daily Star · Xinhua · Times of Israel', MED(11), '#555', 'lm')

img.resize((W, H), Image.LANCZOS).save('entry.png', optimize=True)
print('wrote entry.png')
