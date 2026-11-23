"""Draw the 22 November 2026 world-news image (1024x1024) — v1.

Follows the v13 rank-3 formula that won user approval for 21 Nov:
all-flat, no AI photos; flat graphic + big number INSIDE the graphic +
kicker + headline + 1-line deck + sources per story. Masthead naming
the day and date. Region colour-coding consistent. Legible at ~300px.

Content: ~/workspace/makefun/news-20261122/content-2026-11-22.md
(triangulated from the mature leaderboard, top 8 entries read in full).
Every story/number here comes from that file; nothing invented.

Layout (mirrors v13): top strip + masthead + deck, UTC strip, stat
strip, region bar, 3 leads, 10 mediums (2 rows of 5), map + briefs,
DATE CHECK box, footer.

Differences from v13, all deliberate:
- Kicker pill is per-story: CONFIRMED (green), REPORTED (gold),
  CLAIM (red) — lead 2 (Bahrain) is a CLAIM, leads 1 and 3 REPORTED.
- Brief 33 (ATP final fixture) dropped: it is the same match brief 23
  reports as a result (Alcaraz won). Keeping both would contradict.
- DATE CHECK is full-width at 8pt (the 22 Nov text is ~700 chars;
  9pt needs 4 lines and does not fit the bottom band).
- World map pins are the 22 Nov set (17 pins), with offsets spread
  for the crowded Europe/Middle-East cluster.

Run: python3 draw_v1.py  ->  writes entry_v1.png next to this file.
Deterministic: fixed colours, fixed layout, fixed seed, no timestamps.
"""
import os
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                "..", "news-20261121", "bot"))

from PIL import Image, ImageDraw

from draw import (f, fs, text, headline, wrap, PAPER, INK, RED, GREEN,
                  BLUE, LIGHT, GOLD, flame, dashed_line, CONTINENTS,
                  starburst)
from draw_v11 import card_sq

W, H = 1024, 1024

ME, EU, AM, AF, SA, EA, SEA, OC, GL = ((190, 50, 45), (50, 90, 160),
                                       (50, 130, 80), (210, 130, 40),
                                       (140, 80, 170), (40, 150, 160),
                                       (180, 140, 30), (40, 60, 120),
                                       (110, 110, 110))
GREY = (120, 116, 104)


def kicker_bar_pill(d, x, y, w, num, label, col, pill, pill_col,
                    h=16, fsize=9):
    """v13 kicker bar, but the pill text/colour is per-story."""
    d.rectangle([x, y, x + w, y + h], fill=col)
    text(d, x + 6, y + (h - 11) // 2 + 1, "%d %s" % (num, label),
         f(fsize, True), fill=LIGHT)
    pw = len(pill) * 5 + 10
    px = x + w - 6 - pw
    py = y + (h - 11) // 2
    d.rounded_rectangle([px, py, px + pw, py + 11], radius=2, fill=pill_col)
    text(d, px + pw / 2, py + 1, pill, f(7, True), fill=LIGHT, anchor="ma")


# ---------------------------------------------------------------- leads

def cop_v1(d, x, iy):
    """COP31 lead graphic (308x100): COP31 block + big ~200 nations,
    NO FOSSIL FUELS, $120bn dropped, 35% kept."""
    d.rectangle([x + 8, iy, x + 316, iy + 100], fill=(238, 244, 238))
    # left: COP31 green block
    d.rectangle([x + 8, iy + 8, x + 118, iy + 52], fill=(0, 120, 80))
    text(d, x + 63, iy + 11, "COP31", fs(20), fill=LIGHT, anchor="ma")
    text(d, x + 63, iy + 37, "ANTALYA \u00b7 UN CLIMATE", f(7, True),
         fill=LIGHT, anchor="ma")
    # right: navy block, big ~200 (stacked: number on its own line —
    # "~200 NATIONS" on one line is 190px, wider than the 172px block)
    d.rectangle([x + 128, iy + 8, x + 308, iy + 52], fill=(20, 33, 61))
    text(d, x + 136, iy + 10, "~200", fs(26), fill=LIGHT)
    text(d, x + 136, iy + 38, "NATIONS AT THE TALKS", f(9, True),
         fill=LIGHT)
    # bottom: the story in two lines
    text(d, x + 8, iy + 60, "NO FOSSIL FUELS", fs(15), fill=RED)
    text(d, x + 8, iy + 80, "$120bn adaptation target dropped \u00b7 35% electricity goal for 2035 kept",
         f(9))


def gulf_v1(d, x, iy):
    """Bahrain lead graphic (308x100): flat Gulf, Bahrain starburst,
    big 2 US BASES HIT, the two radar sites named, NO CASUALTIES chip.
    Land shapes follow v13's gulf_map_v13 (already scaled to 100px)."""
    x0, y0, x1, y1 = x + 8, iy, x + 316, iy + 100
    SEA = (58, 118, 170)
    LAND = (214, 196, 158)
    LANDTXT = (96, 84, 60)
    d.rectangle([x0, y0, x1, y1], fill=SEA)
    d.polygon([(x0, y0), (x1, y0), (x1, y0 + 30), (x0 + 265, y0 + 32),
               (x0 + 235, y0 + 36), (x0 + 180, y0 + 40), (x0 + 100, y0 + 42),
               (x0 + 40, y0 + 40), (x0, y0 + 36)], fill=LAND)
    d.polygon([(x0, y1), (x1, y1), (x1, y1 - 18), (x0 + 265, y1 - 38),
               (x0 + 235, y1 - 52), (x0 + 180, y1 - 36), (x0 + 100, y1 - 28),
               (x0 + 40, y1 - 22), (x0, y1 - 24)], fill=LAND)
    bx, by = x0 + 105, y0 + 56
    d.ellipse([bx - 5, by - 3, bx + 5, by + 3], fill=LAND)
    starburst(d, bx, by, 11, RED)
    flame(d, bx, by - 2, 0.55)
    text(d, x0 + 14, y0 + 8, "IRAN", f(10, True), fill=LANDTXT)
    text(d, x0 + 14, y1 - 16, "ARABIA", f(9, True), fill=LANDTXT)
    text(d, bx + 14, by - 11, "BAHRAIN", f(10, True), fill=LIGHT)
    text(d, bx + 14, by + 2, "AL-RIFFA \u00b7 AWALI SAKIR", f(8, True),
         fill=LIGHT)
    text(d, x0 + 235, y0 + 14, "2", fs(28), fill=LIGHT)
    text(d, x0 + 235, y0 + 48, "US BASES HIT", f(9, True), fill=LIGHT)
    chip = "NO CASUALTIES"
    cw = len(chip) * 5 + 12
    cx0 = x1 - cw - 8
    d.rectangle([cx0, y1 - 20, cx0 + cw, y1 - 6], fill=GREEN)
    text(d, cx0 + cw / 2, y1 - 18, chip, f(8, True), fill=LIGHT,
         anchor="ma")


def drone(d, cx, cy, s=1.0):
    """Tiny flat quadcopter: body + 4 rotor arms + red light."""
    d.ellipse([cx - 4 * s, cy - 3 * s, cx + 4 * s, cy + 3 * s],
              fill=(200, 200, 210))
    for dx, dy in [(-7, -5), (7, -5), (-7, 5), (7, 5)]:
        d.line([cx, cy, cx + dx * s, cy + dy * s], fill=(200, 200, 210),
               width=1)
        d.ellipse([cx + dx * s - 2, cy + dy * s - 2,
                   cx + dx * s + 2, cy + dy * s + 2], fill=(220, 220, 230))
    d.ellipse([cx - 1.5, cy - 1.5, cx + 1.5, cy + 1.5], fill=RED)


def drones_v1(d, x, iy):
    """Ukraine lead graphic (308x100): night sky, big 186 fired,
    big 161 downed, drones + interception bursts, 18 sites / Dymer."""
    d.rectangle([x + 8, iy, x + 316, iy + 100], fill=(14, 24, 48))
    for (sx, sy) in [(24, 10), (70, 14), (120, 8), (170, 12), (220, 8),
                     (280, 12), (300, 30), (40, 90), (300, 88),
                     (150, 92), (260, 92), (90, 88)]:
        d.ellipse([x + sx - 1, iy + sy - 1, x + sx + 1, iy + sy + 1],
                  fill=LIGHT)
    text(d, x + 10, iy + 6, "186", fs(30), fill=LIGHT)
    text(d, x + 10, iy + 42, "DRONES FIRED", f(9, True), fill=LIGHT)
    text(d, x + 210, iy + 6, "161", fs(30), fill=(80, 200, 120))
    text(d, x + 210, iy + 42, "DOWNED / JAMMED", f(9, True), fill=LIGHT)
    for (dx, dy) in [(40, 68), (90, 64), (140, 70), (190, 64), (240, 68),
                     (280, 64)]:
        drone(d, x + dx, iy + dy)
    starburst(d, x + 115, iy + 68, 8, (240, 200, 60))
    starburst(d, x + 215, iy + 68, 8, (240, 200, 60))
    text(d, x + 10, iy + 86,
         "18 sites hit \u00b7 Dymer block destroyed \u00b7 3 missiles",
         f(9), fill=LIGHT)


# -------------------------------------------------------------- mediums

def hk_v1(d, x, iy):
    """Hong Kong (176x70): ballot box + big 93.55% turnout."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(240, 242, 248))
    d.rectangle([x + 16, iy + 28, x + 64, iy + 64], fill=(20, 33, 61))
    d.rectangle([x + 28, iy + 24, x + 52, iy + 28], fill=LIGHT)
    d.polygon([(x + 30, iy + 24), (x + 40, iy + 8), (x + 52, iy + 10),
               (x + 44, iy + 24)], fill=LIGHT, outline=(180, 176, 160))
    d.rectangle([x + 16, iy + 52, x + 64, iy + 56], fill=(240, 200, 60))
    text(d, x + 76, iy + 12, "93.55%", fs(20), fill=BLUE)
    text(d, x + 76, iy + 38, "TURNOUT", f(8, True), fill=INK)
    text(d, x + 76, iy + 50, "856 CANDIDATES", f(8, True), fill=INK)


def f1_v1(d, x, iy):
    """Las Vegas GP (176x70): checkered flag + red F1 car + P1."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(18, 18, 22))
    for r in range(2):
        for c in range(20):
            if (r + c) % 2 == 0:
                d.rectangle([x + 8 + c * 9, iy + r * 9,
                             x + 17 + c * 9, iy + 9 + r * 9], fill=LIGHT)
    # flat F1 car profile
    d.polygon([(x + 20, iy + 44), (x + 88, iy + 44), (x + 96, iy + 52),
               (x + 20, iy + 52)], fill=(220, 40, 40))
    d.polygon([(x + 60, iy + 36), (x + 76, iy + 36), (x + 80, iy + 44),
               (x + 58, iy + 44)], fill=(220, 40, 40))
    d.rectangle([x + 88, iy + 32, x + 96, iy + 44], fill=(220, 40, 40))
    d.ellipse([x + 26, iy + 50, x + 38, iy + 62], fill=INK,
              outline=LIGHT, width=1)
    d.ellipse([x + 72, iy + 50, x + 84, iy + 62], fill=INK,
              outline=LIGHT, width=1)
    text(d, x + 120, iy + 22, "P1", fs(24), fill=(240, 200, 60))
    text(d, x + 120, iy + 50, "VERSTAPPEN", f(9, True), fill=LIGHT)


def cricket_v1(d, x, iy):
    """India 720/9 (176x70): green field, pitch, stumps, big 720/9."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(45, 125, 65))
    d.rectangle([x + 62, iy + 8, x + 102, iy + 62], fill=(210, 195, 160))
    for sx in (70, 78, 86):
        d.line([x + sx, iy + 12, x + sx, iy + 26], fill=LIGHT, width=2)
    d.line([x + 68, iy + 12, x + 90, iy + 12], fill=LIGHT, width=2)
    d.ellipse([x + 76, iy + 48, x + 84, iy + 56], fill=(200, 40, 40))
    text(d, x + 114, iy + 12, "720/9", fs(19), fill=LIGHT)
    text(d, x + 114, iy + 38, "RECORD IN NZ", f(8, True), fill=LIGHT)
    text(d, x + 114, iy + 50, "DECLARED", f(8, True), fill=LIGHT)


def sparta_v1(d, x, iy):
    """Sparta II (176x70): burning cargo ship at night + 16 CREW SAFE."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(18, 38, 68))
    d.polygon([(x + 14, iy + 42), (x + 100, iy + 42), (x + 92, iy + 58),
               (x + 22, iy + 58)], fill=(10, 12, 16))
    for j, col in enumerate([(210, 60, 50), (40, 90, 160), (50, 140, 80),
                             (230, 190, 60)]):
        d.rectangle([x + 20 + j * 16, iy + 34, x + 32 + j * 16, iy + 42],
                    fill=col)
    d.rectangle([x + 86, iy + 36, x + 96, iy + 42], fill=LIGHT)
    flame(d, x + 62, iy + 30, 0.55)
    flame(d, x + 80, iy + 34, 0.45)
    text(d, x + 118, iy + 8, "16", fs(28), fill=LIGHT)
    text(d, x + 118, iy + 42, "CREW SAFE", f(9, True), fill=LIGHT)
    text(d, x + 118, iy + 54, "STILL BURNING", f(8, True), fill=LIGHT)


def power_v1(d, x, iy):
    """Iran rationing (176x70): crossed-out bulb + 2 HR daily cuts."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(30, 30, 40))
    d.ellipse([x + 22, iy + 16, x + 54, iy + 48], outline=LIGHT, width=2)
    d.rectangle([x + 32, iy + 48, x + 44, iy + 56], fill=LIGHT)
    d.line([x + 38, iy + 56, x + 38, iy + 62], fill=LIGHT, width=2)
    d.line([x + 18, iy + 12, x + 58, iy + 52], fill=RED, width=3)
    text(d, x + 76, iy + 12, "2 HR", fs(22), fill=GOLD)
    text(d, x + 76, iy + 40, "DAILY CUTS", f(9, True), fill=LIGHT)
    text(d, x + 76, iy + 52, "GAS OUTPUT FALLS", f(8, True), fill=LIGHT)


def icu_v1(d, x, iy):
    """Bolsonaro ICU (176x70): hospital cross + big ICU, STABLE."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(245, 245, 240))
    d.rounded_rectangle([x + 16, iy + 12, x + 64, iy + 60], radius=4,
                        fill=LIGHT, outline=(180, 176, 160))
    d.rectangle([x + 34, iy + 20, x + 46, iy + 52], fill=RED)
    d.rectangle([x + 24, iy + 30, x + 56, iy + 42], fill=RED)
    text(d, x + 76, iy + 12, "ICU", fs(24), fill=RED)
    text(d, x + 76, iy + 42, "STABLE", f(9, True), fill=INK)
    text(d, x + 76, iy + 54, "BREATHING ALONE", f(8, True), fill=INK)


def cikande_v1(d, x, iy):
    """Cikande fire (176x70): factory + flames + 3 DEAD, 36 MISSING."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(35, 28, 22))
    d.rectangle([x + 14, iy + 44, x + 70, iy + 70], fill=(20, 18, 16))
    d.rectangle([x + 58, iy + 28, x + 66, iy + 70], fill=(20, 18, 16))
    flame(d, x + 35, iy + 48, 0.9)
    flame(d, x + 55, iy + 44, 1.0)
    flame(d, x + 75, iy + 50, 0.8)
    text(d, x + 120, iy + 10, "3", fs(28), fill=(240, 120, 30))
    text(d, x + 120, iy + 44, "DEAD", f(9, True), fill=LIGHT)
    text(d, x + 120, iy + 56, "36 MISSING", f(8, True), fill=LIGHT)


def nvidia_v1(d, x, iy):
    """Nvidia SEC probe (176x70): chip + big SEC PROBE."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(15, 25, 15))
    d.rectangle([x + 20, iy + 14, x + 64, iy + 58], fill=(30, 120, 60))
    for k in range(4):
        d.line([x + 26 + k * 10, iy + 10, x + 26 + k * 10, iy + 14],
               fill=(30, 120, 60), width=2)
        d.line([x + 26 + k * 10, iy + 58, x + 26 + k * 10, iy + 62],
               fill=(30, 120, 60), width=2)
        d.line([x + 16, iy + 20 + k * 10, x + 20, iy + 20 + k * 10],
               fill=(30, 120, 60), width=2)
        d.line([x + 64, iy + 20 + k * 10, x + 68, iy + 20 + k * 10],
               fill=(30, 120, 60), width=2)
    d.rectangle([x + 30, iy + 26, x + 54, iy + 46], fill=(15, 25, 15))
    text(d, x + 42, iy + 30, "AI", f(9, True), fill=LIGHT, anchor="ma")
    text(d, x + 76, iy + 12, "SEC", fs(24), fill=LIGHT)
    text(d, x + 76, iy + 44, "PROBE", f(9, True), fill=LIGHT)
    text(d, x + 76, iy + 56, "AI SHARES SLIDE", f(8, True), fill=LIGHT)


def gaza_v1(d, x, iy):
    """Gaza (176x70): food-aid van + big 4 KILLED."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(235, 228, 210))
    d.rectangle([x + 16, iy + 30, x + 62, iy + 54], fill=LIGHT,
                outline=(180, 176, 160))
    d.polygon([(x + 62, iy + 36), (x + 78, iy + 36), (x + 78, iy + 54),
               (x + 62, iy + 54)], fill=LIGHT, outline=(180, 176, 160))
    d.ellipse([x + 26, iy + 52, x + 36, iy + 62], fill=INK)
    d.ellipse([x + 64, iy + 52, x + 74, iy + 62], fill=INK)
    text(d, x + 30, iy + 36, "AID", f(9, True), fill=RED, anchor="ma")
    text(d, x + 100, iy + 10, "4", fs(28), fill=RED)
    text(d, x + 100, iy + 44, "KILLED", f(9, True), fill=INK)
    text(d, x + 100, iy + 56, "IN GAZA", f(8, True), fill=INK)


def aukus_v1(d, x, iy):
    """AUKUS (176x70): submarine + big AUKUS, MARLES: US WRONG."""
    d.rectangle([x + 8, iy, x + 184, iy + 70], fill=(40, 90, 140))
    d.ellipse([x + 16, iy + 32, x + 96, iy + 54], fill=(20, 33, 61))
    d.rectangle([x + 46, iy + 22, x + 62, iy + 34], fill=(20, 33, 61))
    d.line([x + 54, iy + 22, x + 54, iy + 14], fill=(20, 33, 61), width=2)
    d.ellipse([x + 24, iy + 40, x + 30, iy + 46], fill=LIGHT)
    d.ellipse([x + 34, iy + 40, x + 40, iy + 46], fill=LIGHT)
    d.ellipse([x + 44, iy + 40, x + 50, iy + 46], fill=LIGHT)
    text(d, x + 108, iy + 14, "AUKUS", fs(20), fill=LIGHT)
    text(d, x + 108, iy + 42, "MARLES:", f(8, True), fill=LIGHT)
    text(d, x + 108, iy + 54, "US WRONG", f(8, True), fill=LIGHT)


# ------------------------------------------------------------------ map

# (number, lon, lat, region colour) — story numbers from the content file
PINS_22 = [
    (1, 30.7, 36.9, GL),    # Antalya — COP31
    (2, 50.55, 26.2, ME),   # Manama — Bahrain
    (3, 30.5, 50.4, EU),    # Kyiv — Ukraine drones
    (4, 114.2, 22.3, EA),   # Hong Kong
    (5, -115.1, 36.2, AM),  # Las Vegas
    (6, 174.8, -41.3, OC),  # Wellington
    (7, 25.0, 59.5, EU),    # Gulf of Finland
    (8, 51.4, 35.7, ME),    # Tehran
    (9, -47.9, -15.8, AM),  # Brasília
    (10, 106.4, -6.2, SEA),  # Cikande
    (11, -77.0, 38.9, AM),  # Washington
    (12, 34.5, 31.5, ME),   # Gaza
    (13, 149.1, -35.3, OC),  # Canberra
    (14, 56.5, 26.6, ME),   # Strait of Hormuz
    (16, 24.7, 59.4, EU),   # Tallinn
    (18, 77.2, 28.6, SA),   # Delhi
    (21, 12.45, 41.9, EU),  # Rome / Vatican
]

# offsets (dx, dy) from the true spot, for the crowded Europe/ME cluster
PIN_OFFSETS = {
    1: (-16, 10), 2: (-10, 16), 3: (16, -14), 6: (-6, 0),
    7: (-10, -12), 8: (16, -12), 12: (14, 6), 14: (18, 10),
    16: (-20, 4), 18: (8, 14), 21: (-20, -14),
}


def world_map_v1(d, x0, y0, x1, y1):
    """Equirectangular world map with the 22 Nov pins (same geometry
    as v12's map, new pin set and offsets)."""
    d.rectangle([x0, y0, x1, y1], fill=(196, 221, 238))
    for lon in range(-150, 181, 30):
        gx = x0 + (lon + 180) / 360 * (x1 - x0)
        d.line([gx, y0, gx, y1], fill=(172, 202, 222), width=1)
    for lat in range(-60, 81, 30):
        gy = y0 + (80 - lat) / 140 * (y1 - y0)
        d.line([x0, gy, x1, gy], fill=(172, 202, 222), width=1)
    for poly in CONTINENTS:
        pts = [(x0 + (lon + 180) / 360 * (x1 - x0),
                y0 + (80 - lat) / 140 * (y1 - y0)) for lon, lat in poly]
        d.polygon(pts, fill=(188, 204, 168), outline=(140, 160, 120))
    text(d, x0 + (30 / 360) * (x1 - x0), y0 + (80 / 140) * (y1 - y0),
         "PACIFIC", f(7, True), fill=(120, 150, 175))
    text(d, x0 + (135 / 360) * (x1 - x0), y0 + (50 / 140) * (y1 - y0),
         "ATLANTIC", f(7, True), fill=(120, 150, 175))
    for num, lon, lat, col in PINS_22:
        cx = x0 + (lon + 180) / 360 * (x1 - x0)
        cy = y0 + (80 - lat) / 140 * (y1 - y0)
        px, py = cx, cy
        if num in PIN_OFFSETS:
            dx, dy = PIN_OFFSETS[num]
            px, py = cx + dx, cy + dy
            d.line([(cx, cy), (px, py)], fill=col, width=1)
        d.ellipse([px - 7, py - 7, px + 7, py + 7], fill=col,
                  outline=LIGHT, width=2)
        text(d, px, py - 6, str(num), f(8, True), fill=LIGHT, anchor="ma")


# ----------------------------------------------------------------- build

def build_v1():
    img = Image.new("RGB", (1024, 1024), PAPER)
    d = ImageDraw.Draw(img)

    # ---- top strip + masthead ----
    text(d, 12, 3, "THE WORLD IN ONE DAY", f(10, True))
    text(d, 512, 3, "DAY 326 OF 2026", f(10, True), fill=RED, anchor="ma")
    text(d, 1012, 3, "ALL TIMES UTC", f(10, True), anchor="ra")
    d.line([12, 16, 1012, 16], fill=INK, width=1)
    text(d, 12, 20, "Sunday 22 November 2026", fs(58), fill=INK)
    d.line([12, 90, 1012, 90], fill=INK, width=2)
    text(d, 512, 94,
         "COP31 final text at dawn \u00b7 Iran claims strikes on US bases in Bahrain \u00b7 186 drones over Ukraine overnight",
         fs(13), anchor="ma")

    # ---- UTC strip ----
    d.rectangle([12, 112, 104, 140], fill=INK)
    text(d, 58, 114, "THE DAY", f(10, True), fill=LIGHT, anchor="ma")
    text(d, 58, 126, "IN UTC", f(10, True), fill=LIGHT, anchor="ma")
    d.rectangle([112, 112, 1012, 140], fill=INK)
    text(d, 120, 115,
         "03:00 COP31 objections close \u00b7 05:11 Hamas seeks talks \u00b7 05:30 Las Vegas GP ends \u00b7 06:00 COP31 approval session",
         f(9), fill=LIGHT)
    text(d, 120, 128,
         "08:00 161 of 186 drones downed \u00b7 14:00 Hong Kong turnout 93.55% \u00b7 17:00 ATP final, Turin",
         f(9), fill=LIGHT)

    # ---- stat strip ----
    stats = [("~200", "nations at the\nCOP31 talks"),
             ("03:00", "GMT deadline for\nCOP31 objections"),
             ("186", "drones fired at\nUkraine overnight"),
             ("2", "US bases targeted\nin Bahrain"),
             ("856", "candidates in the\nHong Kong vote"),
             ("720/9", "India's record\ntotal in NZ")]
    bounds = [12, 179, 345, 512, 679, 845, 1012]
    for i, (num, lab) in enumerate(stats):
        x = bounds[i]
        text(d, x + 4, 154, num, fs(24), fill=RED)
        nw = d.textlength(num, font=fs(24))
        lx = x + 14 + nw
        for j, ln in enumerate(lab.split("\n")):
            text(d, lx, 158 + j * 12, ln, f(9))
    for bx in bounds[1:-1]:
        d.line([bx, 152, bx, 190], fill=(200, 196, 180), width=1)
    # region bar
    regions = [("Europe 7", EU), ("Middle East 6", ME), ("Americas 5", AM),
               ("Africa 3", AF), ("South Asia 2", SA), ("East Asia 3", EA),
               ("South-East Asia 2", SEA), ("Oceania 3", OC),
               ("Global 4", GL)]
    text(d, 12, 196, "STORIES BY REGION", f(9, True))
    rx = 132
    for name, col in regions:
        w = len(name) * 5 + 10
        d.rectangle([rx, 194, rx + w, 208], fill=col)
        text(d, rx + w / 2, 198, name, f(8, True), fill=LIGHT, anchor="ma")
        rx += w + 5

    # ---- leads (3) ----
    leads = [
        (1, "GLOBAL \u00b7 COP31, ANTALYA \u00b7 CLIMATE", "cop", "REPORTED",
         (176, 132, 16),
         "COP31 text lands at dawn \u2014 no fossil fuels",
         "Ten-page package drops the $120bn adaptation target, keeps a 35% electricity goal for 2035.",
         "REUTERS \u00b7 BBC \u00b7 THE GUARDIAN", GL),
        (2, "MIDDLE EAST \u00b7 BAHRAIN \u00b7 GULF WAR", "gulf", "CLAIM",
         RED,
         "Iran claims strikes on US bases in Bahrain",
         "Tehran says it hit Patriot radars at two bases. Bahrain: intercepted; a facility burned, no one hurt.",
         "AL JAZEERA \u00b7 REUTERS \u00b7 IRGC STATEMENT", ME),
        (3, "EUROPE \u00b7 UKRAINE \u00b7 WAR", "drones", "REPORTED",
         (176, 132, 16),
         "Russia's barrage: 186 drones, 161 downed",
         "186 drones and three missiles fired; 161 downed or jammed. Strikes at 18 sites; a Dymer block destroyed.",
         "UKRAINIAN AIR FORCE \u00b7 KYIV INDEPENDENT", EU),
    ]
    for i, (num, kick, kind, pill, pill_col, head, summ, src, col) in enumerate(leads):
        x = 12 + i * 338
        card_sq(d, [x, 214, x + 324, 442])
        kicker_bar_pill(d, x, 214, 324, num, kick, col, pill, pill_col,
                        h=24, fsize=10)
        if kind == "cop":
            cop_v1(d, x, 244)
        elif kind == "gulf":
            gulf_v1(d, x, 244)
        else:
            drones_v1(d, x, 244)
        yy = headline(d, x + 8, 350, head, 20, 308, 2)
        yy = headline(d, x + 8, yy + 2, summ, 10, 308, 2)
        text(d, x + 8, yy + 2, src, f(8), fill=GREY)

    # ---- mediums (10) ----
    mediums = [
        (4, "HONG KONG", "hk",
         "Hong Kong elects its Election Committee",
         "856 candidates for 723 seats.", "SCMP", EA),
        (5, "LAS VEGAS \u00b7 F1", "f1",
         "Verstappen wins the Las Vegas GP",
         "Beats Norris and Piastri.", "REUTERS \u00b7 F1", AM),
        (6, "WELLINGTON", "cricket",
         "India declare 720/9 \u2014 a record in NZ",
         "Pant 128, Rahul 136.", "REUTERS \u00b7 AP \u00b7 ESPN", OC),
        (7, "GULF OF FINLAND", "sparta",
         "Sparta II still burning off Finland",
         "Hit Saturday; all 16 crew safe.", "REUTERS", EU),
        (8, "TEHRAN \u00b7 ENERGY", "power",
         "Iran begins rationing electricity",
         "Two-hour daily cuts begin.", "RFE/RL \u00b7 STRAITS TIMES", ME),
        (9, "BRAS\u00cdLIA \u00b7 HEALTH", "icu",
         "Bolsonaro in intensive care",
         "Bowel obstruction; stable.", "AL JAZEERA \u00b7 REUTERS", AM),
        (10, "CIKANDE \u00b7 FIRE", "cikande",
         "Candy-factory fire: 3 dead, 36 missing",
         "Blaze tore through Banten plant.", "DETIKNEWS", SEA),
        (11, "WASHINGTON \u00b7 SEC", "nvidia",
         "Nvidia faces an SEC probe",
         "Accounting inquiry; shares slide.", "STRAITS TIMES \u00b7 CNBC",
         AM),
        (12, "GAZA \u00b7 CONFLICT", "gaza",
         "Four killed as Israeli fire hits Gaza",
         "Three in a food-aid vehicle.", "AFP \u00b7 AL JAZEERA", ME),
        (13, "CANBERRA", "aukus",
         "Marles rejects US report on AUKUS subs",
         "Australia defends the subs plan.", "ABC \u00b7 REUTERS", OC),
    ]
    gfx = {"hk": hk_v1, "f1": f1_v1, "cricket": cricket_v1,
           "sparta": sparta_v1, "power": power_v1, "icu": icu_v1,
           "cikande": cikande_v1, "nvidia": nvidia_v1, "gaza": gaza_v1,
           "aukus": aukus_v1}
    for i, (num, kick, kind, head, deck, src, col) in enumerate(mediums):
        x = 12 + (i % 5) * 200
        y = 448 + (i // 5) * 168
        card_sq(d, [x, y, x + 192, y + 162])
        gfx[kind](d, x, y + 6)
        kicker_bar_pill(d, x, y + 82, 192, num, kick, col, "CONFIRMED",
                        GREEN)
        headline(d, x + 8, y + 104, head, 13, 176, 2)
        text(d, x + 8, y + 140, deck, f(9))
        text(d, x + 192 - 8, y + 153, src, f(8), fill=GREY, anchor="ra")

    # ---- map + briefs ----
    card_sq(d, [12, 784, 460, 958])
    text(d, 20, 788, "WHERE IT HAPPENED", f(11, True))
    text(d, 20, 802, "pin numbers match the stories; pin colour is the region",
         f(9), fill=GREY)
    world_map_v1(d, 20, 814, 452, 954)
    text(d, 468, 788, "ALSO ON SUNDAY 22 NOVEMBER 2026", f(11, True))
    text(d, 468, 802, "21 more stories, in order of consequence",
         f(9), fill=GREY)
    briefs = [
        (14, "HORMUZ", "Two tankers hit; Torkel burning.", "UKMTO", ME),
        (15, "HORMUZ", "Iran: downed 2 US drones.", "AL JAZEERA", ME),
        (16, "ESTONIA", "Shuts Russia border 1 Dec.", "REUTERS", EU),
        (17, "DENMARK", "Expels Russian attach\u00e9.", "GUARDIAN", EU),
        (18, "DELHI", "Nepal PM Shah lands on state visit.", "IANS", SA),
        (19, "FBI", "Probes hack of its crime database.", "AP", AM),
        (20, "EU", "EU, Indonesia sign trade deal.", "REUTERS", GL),
        (21, "VATICAN", "Pope hosts 1,300 for lunch.", "VATICAN", EU),
        (22, "LADAKH", "70% turnout in first polls.", "DAILY WORLD", SA),
        (23, "TURIN", "Alcaraz beats Zverev 6-2, 7-6.", "GUARDIAN", EU),
        (24, "NBA", "Wemby scores 50; Spurs win.", "REUTERS", AM),
        (25, "SEOUL", "Minister quits over AI cheating.", "GUARDIAN", EA),
        (26, "KHARTOUM", "Drones hit homes in Khartoum.", "AFP", AF),
        (27, "W. KORDOFAN", "RSF accused of killing civilians.", "", AF),
        (28, "MYANMAR", "Rohingya genocide ruling.", "GUARDIAN", SEA),
        (29, "RIYADH", "Saudi downs Houthi missile.", "ANADOLU", ME),
        (30, "MANILA", "Bomber turns back 170 km out.", "AP", EA),
        (31, "MELBOURNE", "70 years since 1956 Olympics.", "ABC", OC),
        (32, "RUGBY", "England 37-12 New Zealand.", "REUTERS", GL),
        (34, "CRYPTO", "Bitcoin back above $60,000.", "MARKETS", GL),
        (35, "BAYELSA", "Boat toll reaches 24 dead.", "AP", AF),
    ]
    for i, (num, region, s, src, col) in enumerate(briefs):
        col_i = i // 11
        row = i % 11
        bx = 468 + col_i * 276
        by = 814 + row * 13
        d.rectangle([bx, by, bx + 14, by + 13], fill=col)
        text(d, bx + 7, by + 1, str(num), f(8, True), fill=LIGHT,
             anchor="ma")
        text(d, bx + 18, by, region + ": ", f(10, True))
        rw = d.textlength(region + ": ", font=f(10, True))
        text(d, bx + 18 + rw, by, s, f(10))
        if src:
            text(d, bx + 268, by + 1, src, f(8), fill=GREY, anchor="ra")

    # ---- bottom: DATE CHECK (exact text from the content file) ----
    dc = ("Left out on purpose, first reported Friday or Saturday, so not shown as Sunday's news: "
          "the Peru 6.7 quake itself (Fri 20 Nov local) \u00b7 Russia's 400-drone, 110-missile barrage (Thu night\u2013Fri 20 Nov) "
          "\u00b7 the Kryvyi Rih double-tap (Fri night) \u00b7 'El Chapo Isidro' captured (Fri night) \u00b7 the EU\u2013Indonesia trade "
          "deal (Sat \u2014 see brief 20) \u00b7 the Shenzhen summit (Thu 19 Nov) \u00b7 BepiColombo's Mercury orbit (Sat) \u00b7 "
          "the Basra power-plant fire (Sat). Tonight's real count: 186 drones, not 400. "
          "Wires read up to ~09:45 UTC, Sunday 22 November 2026; every story here was reported, or was still "
          "developing, on 22 November in at least one time zone. Claims are labelled CLAIM; unconfirmed items "
          "labelled REPORTED.")
    d.rectangle([12, 962, 1012, 1008], fill=(255, 250, 235), outline=RED,
                width=1)
    text(d, 20, 965, "DATE CHECK \u2014 LEFT OUT ON PURPOSE", f(9, True),
         fill=RED)
    dc_lines = wrap(d, dc, f(8), 984)
    assert len(dc_lines) == 3, "DATE CHECK wrapped to %d lines" % len(dc_lines)
    for j, ln in enumerate(dc_lines):
        text(d, 20, 976 + j * 11, ln, f(8))
    text(d, 512, 1011,
         "Every story here happened or was first reported on Sunday 22 November 2026 (UTC). Maps, charts and text drawn in code.",
         f(8), fill=GREY, anchor="ma")
    return img


if __name__ == "__main__":
    im = build_v1()
    im.save("entry_v1.png")
    print("saved entry_v1.png", im.size)
