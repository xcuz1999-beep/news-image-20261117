#!/usr/bin/env python3
"""THE WORLD TODAY - one-page newspaper image for Tuesday 17 November 2026.

Standard library only. Deterministic: no randomness, no clock, no network.
Writes a 1024x1024 PNG to $MAKEFUN_OUTPUT_DIR/entry.png (default /output).
"""
import os
import struct
import zlib

W = 1024
H = 1024

PAPER = (246, 241, 226)
INK = (22, 22, 22)
RED = (178, 32, 32)
NAVY = (28, 48, 110)
WHITE = (250, 250, 248)
GRAY = (110, 110, 110)
LGRAY = (198, 194, 182)
SKY = (198, 214, 222)
SEA = (44, 84, 128)
SMOKE = (130, 130, 130)

FB = bytearray(W * H * 3)


def set_px(x, y, color):
    if 0 <= x < W and 0 <= y < H:
        i = (y * W + x) * 3
        FB[i] = color[0]
        FB[i + 1] = color[1]
        FB[i + 2] = color[2]


def fill_rect(x, y, w, h, color):
    x0 = max(0, x)
    y0 = max(0, y)
    x1 = min(W, x + w)
    y1 = min(H, y + h)
    if x1 <= x0 or y1 <= y0:
        return
    row = bytes(color) * (x1 - x0)
    for yy in range(y0, y1):
        i = (yy * W + x0) * 3
        FB[i:i + len(row)] = row


def fill_all(color):
    FB[:] = bytes(color) * (W * H)


def draw_rect(x, y, w, h, color, t=1):
    fill_rect(x, y, w, t, color)
    fill_rect(x, y + h - t, w, t, color)
    fill_rect(x, y, t, h, color)
    fill_rect(x + w - t, y, t, h, color)


def draw_line(x0, y0, x1, y1, color, t=1):
    dx = abs(x1 - x0)
    dy = -abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx + dy
    x, y = x0, y0
    while True:
        fill_rect(x - t // 2, y - t // 2, t, t, color)
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 >= dy:
            err += dy
            x += sx
        if e2 <= dx:
            err += dx
            y += sy


def fill_circle(cx, cy, r, color):
    for yy in range(cy - r, cy + r + 1):
        for xx in range(cx - r, cx + r + 1):
            if (xx - cx) * (xx - cx) + (yy - cy) * (yy - cy) <= r * r:
                set_px(xx, yy, color)


# ---------------------------------------------------------------- font
# Hand-authored 5x7 bitmap font. Each glyph is 7 rows of 5 characters.
FONT = {
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "B": ["####.", "#...#", "#...#", "####.", "#...#", "#...#", "####."],
    "C": [".####", "#....", "#....", "#....", "#....", "#....", ".####"],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "E": ["#####", "#....", "#....", "####.", "#....", "#....", "#####"],
    "F": ["#####", "#....", "#....", "####.", "#....", "#....", "#...."],
    "G": [".####", "#....", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "J": ["..###", "...#.", "...#.", "...#.", "...#.", "#..#.", ".##.."],
    "K": ["#...#", "#..#.", "#.#..", "##...", "#.#..", "#..#.", "#...#"],
    "L": ["#....", "#....", "#....", "#....", "#....", "#....", "#####"],
    "M": ["#...#", "##.##", "#.#.#", "#.#.#", "#...#", "#...#", "#...#"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "O": [".###.", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "P": ["####.", "#...#", "#...#", "####.", "#....", "#....", "#...."],
    "Q": [".###.", "#...#", "#...#", "#...#", "#.#.#", "#..#.", ".##.#"],
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "T": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "V": ["#...#", "#...#", "#...#", "#...#", "#...#", ".#.#.", "..#.."],
    "W": ["#...#", "#...#", "#...#", "#.#.#", "#.#.#", "##.##", "#...#"],
    "X": ["#...#", ".#.#.", "..#..", "..#..", "..#..", ".#.#.", "#...#"],
    "Y": ["#...#", "#...#", ".#.#.", "..#..", "..#..", "..#..", "..#.."],
    "Z": ["#####", "....#", "...#.", "..#..", ".#...", "#....", "#####"],
    "0": [".###.", "#...#", "#..##", "#.#.#", "##..#", "#...#", ".###."],
    "1": ["..#..", ".##..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "2": [".###.", "#...#", "....#", "..##.", ".#...", "#....", "#####"],
    "3": [".###.", "#...#", "....#", "..##.", "....#", "#...#", ".###."],
    "4": ["...#.", "..##.", ".#.#.", "#..#.", "#####", "...#.", "...#."],
    "5": ["#####", "#....", "####.", "....#", "....#", "#...#", ".###."],
    "6": [".###.", "#....", "#....", "####.", "#...#", "#...#", ".###."],
    "7": ["#####", "....#", "...#.", "..#..", ".#...", ".#...", ".#..."],
    "8": [".###.", "#...#", "#...#", ".###.", "#...#", "#...#", ".###."],
    "9": [".###.", "#...#", "#...#", ".####", "....#", "....#", ".###."],
    " ": [".....", ".....", ".....", ".....", ".....", ".....", "....."],
    ".": [".....", ".....", ".....", ".....", ".....", ".##..", ".##.."],
    ",": [".....", ".....", ".....", ".....", ".##..", ".##..", ".#..."],
    "'": [".##..", ".##..", ".#...", ".....", ".....", ".....", "....."],
    "-": [".....", ".....", ".....", "#####", ".....", ".....", "....."],
    ":": [".....", ".##..", ".##..", ".....", ".##..", ".##..", "....."],
    ";": [".....", ".##..", ".##..", ".....", ".##..", ".##..", ".#..."],
    "!": ["..#..", "..#..", "..#..", "..#..", "..#..", ".....", "..#.."],
    "?": [".###.", "#...#", "....#", "..##.", "..#..", ".....", "..#.."],
    "/": ["....#", "....#", "...#.", "..#..", ".#...", "#....", "#...."],
    "$": ["..#..", ".####", "#.#..", ".###.", "..#.#", "####.", "..#.."],
    "%": ["##..#", "##.#.", "....#", "...#.", "..#..", ".#.##", "#..##"],
    "(": ["...#.", "..#..", ".#...", ".#...", ".#...", "..#..", "...#."],
    ")": [".#...", "..#..", "...#.", "...#.", "...#.", "..#..", ".#..."],
    "+": [".....", "..#..", "..#..", "#####", "..#..", "..#..", "....."],
    "=": [".....", ".....", "#####", ".....", "#####", ".....", "....."],
    '"': [".#.#.", ".#.#.", ".#.#.", ".....", ".....", ".....", "....."],
    "_": [".....", ".....", ".....", ".....", ".....", ".....", "#####"],
    "|": ["..#..", "..#..", "..#..", "..#..", "..#..", "..#..", "..#.."],
    "*": [".....", "#.#.#", ".###.", "#####", ".###.", "#.#.#", "....."],
    "&": [".###.", "#...#", "#.#..", ".#...", "#.#.#", "#..#.", ".##.#"],
}


def advance(sx, bold=False):
    return 5 * sx + sx + (1 if bold else 0)


def text_width(s, sx, bold=False):
    if not s:
        return 0
    return len(s) * advance(sx, bold) - sx


def draw_text(x, y, s, color, sx=1, sy=1, bold=False):
    s = s.upper()
    adv = advance(sx, bold)
    cx = x
    for ch in s:
        glyph = FONT.get(ch, FONT[" "])
        for gy in range(7):
            row = glyph[gy]
            for gx in range(5):
                if row[gx] == "#":
                    fill_rect(cx + gx * sx, y + gy * sy, sx, sy, color)
                    if bold:
                        fill_rect(cx + gx * sx + 1, y + gy * sy, sx, sy, color)
        cx += adv
    return cx


def draw_centered(y, s, color, sx=1, sy=1, bold=False, cx_mid=None):
    if cx_mid is None:
        cx_mid = W // 2
    x = cx_mid - text_width(s, sx, bold) // 2
    draw_text(x, y, s, color, sx, sy, bold)
    return x


def wrap_text(s, max_width, sx, bold=False):
    adv = advance(sx, bold)
    max_chars = max(1, max_width // adv)
    words = s.upper().split(" ")
    lines = []
    cur = ""
    for word in words:
        if not cur:
            cur = word
        elif len(cur) + 1 + len(word) <= max_chars:
            cur = cur + " " + word
        else:
            lines.append(cur)
            cur = word
    if cur:
        lines.append(cur)
    return lines


def draw_wrapped(x, y, s, color, sx, sy, bold, max_width, line_h):
    lines = wrap_text(s, max_width, sx, bold)
    for i, line in enumerate(lines):
        draw_text(x, y + i * line_h, line, color, sx, sy, bold)
    return len(lines)


# ---------------------------------------------------------------- content
LEAD_HEAD = "UKRAINE SHATTERS THE CRIMEA BRIDGE"
LEAD_SUM = ("A section of the Kerch road bridge collapsed after a Ukrainian "
            "strike Zelenskyy called unprecedented; Russia answered with "
            "missiles on Kyiv's Dnipro bridges.")

MEDIUM = [
    ("TRUMP LANDS IN MANILA",
     "The ASEAN summit opens his Asia trip; a trade statement is signed "
     "with Thailand, and Shenzhen talks with Xi and Putin are set for 19 Nov."),
    ("NVIDIA'S FIRST EARNINGS AFTER HUANG",
     "The chip giant reports after its CEO's exit as Washington moves to "
     "curb China's AI-chip access and close the cloud loophole."),
    ("JPMORGAN: OUTAGE WAS A SOFTWARE BUG",
     "The bank says Monday's online and payments disruption was a software "
     "bug, not a cyberattack."),
    ("VULCAN ROCKET FAILS, 40 SATELLITES LOST",
     "A ULA Vulcan anomaly in flight destroyed its payload of 40 Amazon "
     "Leo internet satellites."),
    ("JAPAN SCRAMBLES JETS AT RUSSIAN JETS",
     "Tokyo protests a suspected Russian airspace violation; South Korea "
     "intercepts Russian aircraft the same day."),
    ("SAUDI ARABIA SACKS YEMEN COMMANDER",
     "The coalition chief is replaced as Houthi forces advance to within "
     "60 km of Aden and government troops quit the Red Sea coast."),
]

BRIEFS = [
    ("BAHRAIN", "IRANIAN DRONES TARGET US RADAR",
     "Tehran's Guards fired drones at a US radar site; Bahrain says the attack was intercepted."),
    ("HORMUZ", "TANKERS HIT MINES, IRAN SAYS",
     "Tehran claims two tankers struck mines in the strait as a third US carrier reaches the region."),
    ("WASHINGTON", "DIRTY-BOMB PLOT ALLEGED",
     "US intel reports an alleged Iranian plot against Trump officials; unconfirmed, and Tehran denies it."),
    ("LONDON", "BRITAIN SANCTIONS SETTLEMENT FIRMS",
     "Eight Israeli builders are sanctioned; four Western nations urge Gaza aid crossings opened."),
    ("JERICHO", "SETTLERS KILL WOMAN, 72",
     "A Palestinian woman was killed overnight in Jericho, Reuters reports."),
    ("GENEVA", "128 STATES DEBATE KILLER ROBOTS",
     "A UN conference weighs a treaty banning lethal autonomous weapons."),
    ("BRUSSELS", "EU CHARGES TEMU",
     "Regulators say the marketplace did too little to stop illegal product sales."),
    ("PARIS", "LE PEN PLEDGES EARLIER RETIREMENT",
     "In France, Depardieu drops his appeal and admits a sexual assault charge."),
    ("WASHINGTON", "PENTAGON FAILS AUDIT, NINTH YEAR",
     "The Defence Department fails its financial audit for the ninth year running."),
    ("HEALTH", "US LOSES MEASLES-FREE STATUS",
     "Cases are the highest since 1991; 13 babies were born with congenital measles."),
    ("CHINA", "ELECTRIC AIRLINER'S FIRST FLIGHT",
     "The 19-seat CE-25A electric aircraft completes its maiden flight."),
    ("ANTALYA", "COP31 TURNS TO ENERGY",
     "The climate summit's second week focuses on energy and transport."),
    ("SPAIN", "FLOODS HIT THE EAST",
     "Severe flooding strikes eastern Spain; Britain braces for winter's first named storm."),
    ("MANILA", "PRABOWO PRESSES SEA CODE",
     "Indonesia's president urges ASEAN and China to finish the South China Sea code of conduct."),
    ("SHENZHEN", "PNG'S MARAPE MEETS XI",
     "Papua New Guinea's PM says his country is no longer a place for Taiwan operations."),
    ("MANILA", "GUTERRES ON THE ROHINGYA",
     "The UN chief urges accountability for abuses against the Rohingya at the ASEAN-UN summit."),
    ("WASHINGTON", "TESTIMONY NEEDS WHITE HOUSE OK",
     "Agencies are ordered to clear staff testimony to Congress with the White House first."),
    ("SPORT", "INDONESIA ROUT AFGHANISTAN 4-0",
     "A 4-0 win puts Indonesia on top of their group."),
]

TICKER = ("BRENT CRUDE $92.76, UP 0.4% | OIL CAUGHT BETWEEN TANKER ATTACKS "
          "AND EXPORTS | US EMERGENCY-ALERT TEST HELD | EUROPEAN SHARES "
          "FALL BEFORE NVIDIA RESULTS")

# Coarse world map, authored as string rows. 'X' = land.
MAP_ROWS = [
    "............................................",
    "..XXXX........XX...XXXXXXXXXXXXXXXXX........",
    ".XXXXXXXX..XX.XXXXXXXXXXXXXXXXXXXXXXX.......",
    "..XXXXXXXXX...XXXXXXXXXXXXXXXXXXXXXX........",
    "...XXXXXXXX....XXXXXXXXXXXXXXXXXX...........",
    "....XXXXXX......XXXXXXXXXXXXXXXX............",
    ".....XXXX........XXXXXXXXXXXXXX.............",
    "......XXX.........XXXXXXXXXXX....XX.........",
    "......XX...........XXXXXXXXX.....XXX........",
    ".....XXXX..........XXXXXXX.......XX.........",
    ".....XXXX...........XXXXX...................",
    "......XXX...........XXXX...........XXXXX....",
    "......XXX...........XXX............XXXXX....",
    ".......XX...........XX..............XXX.....",
    ".......XX...................................",
    "......XXX...................................",
    "......XX....................................",
    ".......X....................................",
]
MAP_MARKERS = [(24, 3), (5, 5), (20, 2), (39, 5), (36, 8), (27, 6), (33, 11)]


def draw_illustration(x, y, w, h):
    draw_rect(x, y, w, h, INK, 2)
    fill_rect(x + 2, y + 2, w - 4, h - 4, SKY)
    sea_y = y + h - 24
    fill_rect(x + 2, sea_y, w - 4, 22, SEA)
    for i in range(9):
        fill_rect(x + 18 + i * 66, sea_y + 6 + (i % 2) * 7, 30, 2, WHITE)
    fill_circle(x + 52, y + 16, 9, (232, 196, 90))
    deck_y = y + h - 34
    fill_rect(x + 2, deck_y, 218, 5, INK)
    fill_rect(x + w - 220, deck_y, 218, 5, INK)
    for tx in (x + 90, x + w - 96):
        fill_rect(tx, deck_y - 26, 5, 26, INK)
        draw_line(tx + 2, deck_y - 26, tx - 34, deck_y, INK, 2)
        draw_line(tx + 2, deck_y - 26, tx + 38, deck_y, INK, 2)
    draw_line(x + 220, deck_y + 2, x + 292, deck_y + 20, RED, 5)
    draw_line(x + w - 220, deck_y + 2, x + w - 292, deck_y + 20, RED, 5)
    fill_rect(x + 286, deck_y + 16, 44, 4, INK)
    for cx, cy, r in ((x + 372, y + 18, 10), (x + 394, y + 15, 12),
                      (x + 420, y + 18, 10), (x + 300, y + 16, 8)):
        fill_circle(cx, cy, r, SMOKE)


def draw_map(x, y):
    draw_text(x, y, "THE DAY ON THE MAP", NAVY, 2, 2, True)
    my = y + 24
    for r, row in enumerate(MAP_ROWS):
        row = row.ljust(44)[:44]
        for c, ch in enumerate(row):
            if ch == "X":
                fill_rect(x + c * 8, my + r * 8, 5, 5, NAVY)
            else:
                set_px(x + c * 8 + 2, my + r * 8 + 2, LGRAY)
    for c, r in MAP_MARKERS:
        fill_rect(x + c * 8 - 1, my + r * 8 - 1, 7, 7, RED)
    draw_text(x, my + 18 * 8 + 8, "RED SQUARES: WHERE THE DAY HAPPENED", RED, 1, 2, False)
    draw_text(x, my + 18 * 8 + 26, "COARSE SCHEMATIC MAP - NOT TO SCALE", GRAY, 1, 1, False)


def build():
    fill_all(PAPER)
    draw_rect(6, 6, W - 12, H - 12, INK, 3)
    # Masthead
    draw_centered(16, "THE WORLD TODAY", INK, 8, 8, False)
    fill_rect(12, 78, W - 24, 4, RED)
    fill_rect(12, 86, W - 24, 1, INK)
    # Date bar
    fill_rect(12, 92, W - 24, 42, NAVY)
    draw_centered(103, "TUESDAY 17 NOVEMBER 2026", WHITE, 4, 3, False)
    draw_centered(140, "ONE DAY | ONE PAGE | THE WHOLE WORLD", RED, 2, 2, True)
    fill_rect(12, 162, W - 24, 2, INK)

    # Lead story + map rail
    draw_illustration(12, 170, 604, 78)
    n = draw_wrapped(12, 254, LEAD_HEAD, INK, 3, 3, True, 604, 24)
    draw_wrapped(12, 254 + n * 24 + 4, LEAD_SUM, INK, 2, 2, False, 604, 17)
    fill_rect(622, 170, 1, 206, LGRAY)
    draw_map(632, 170)
    fill_rect(12, 380, W - 24, 2, INK)

    # Medium stories: 3 columns x 2 rows
    draw_text(12, 388, "TOP STORIES", RED, 2, 2, True)
    draw_text(760, 388, "BUSINESS - SCIENCE - WORLD", GRAY, 1, 2, False)
    col_x = [12, 352, 692]
    col_w = 320
    for idx, (head, summ) in enumerate(MEDIUM):
        cx = col_x[idx % 3]
        cy = 412 + (idx // 3) * 96
        hn = draw_wrapped(cx, cy, head, INK, 2, 2, True, col_w, 17)
        draw_wrapped(cx, cy + hn * 17 + 3, summ, INK, 1, 2, False, col_w, 16)
    fill_rect(342, 412, 1, 182, LGRAY)
    fill_rect(682, 412, 1, 182, LGRAY)
    fill_rect(12, 602, W - 24, 2, INK)

    # Briefs
    draw_text(12, 610, "AROUND THE WORLD IN BRIEFS", INK, 3, 3, True)
    fill_rect(12, 640, W - 24, 1, INK)
    for col in range(2):
        bx = 12 if col == 0 else 520
        by = 648
        items = BRIEFS[col * 9:(col + 1) * 9]
        for j, (place, head, summ) in enumerate(items):
            num = col * 9 + j + 1
            draw_text(bx, by, str(num) + ". " + place + ": " + head, INK, 1, 2, True)
            used = draw_wrapped(bx, by + 17, summ, INK, 1, 1, False, 492, 9)
            by += 17 + used * 9 + 5
    fill_rect(512, 648, 1, 318, LGRAY)

    # Ticker
    fill_rect(12, 976, W - 24, 36, INK)
    draw_centered(987, TICKER, WHITE, 1, 2, False)


def encode_png():
    raw = bytearray()
    stride = W * 3
    for yy in range(H):
        raw.append(0)
        raw.extend(FB[yy * stride:(yy + 1) * stride])
    comp = zlib.compress(bytes(raw), 9)

    def chunk(tag, data):
        out = struct.pack(">I", len(data)) + tag + data
        out += struct.pack(">I", zlib.crc32(tag + data) & 0xFFFFFFFF)
        return out

    ihdr = struct.pack(">IIBBBBB", W, H, 8, 2, 0, 0, 0)
    return (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", ihdr)
            + chunk(b"IDAT", comp) + chunk(b"IEND", b""))


def main():
    build()
    data = encode_png()
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    os.makedirs(out_dir, exist_ok=True)
    path = os.path.join(out_dir, "entry.png")
    with open(path, "wb") as fh:
        fh.write(data)


if __name__ == "__main__":
    main()
