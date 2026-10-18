# Mit diesem Skript habe ich die Pixel-Grafiken fuer das Spiel erzeugt.
# Jedes Bild ist als Text "gemalt": ein Buchstabe = ein Pixel, "." = durchsichtig.
# Aufruf aus dem Projektordner:  python3 tools/make_sprites.py
# Benoetigt: pip install pillow
from PIL import Image
import os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")

PAL = {
    ".": None,
    "H": (42, 27, 20),      # Haare dunkel
    "h": (78, 52, 36),      # Haare Glanz
    "S": (246, 201, 160),   # Haut
    "E": (29, 20, 16),      # Auge
    "M": (232, 120, 130),   # Wange
    "R": (140, 40, 50),     # Mund
    "D": (232, 71, 106),    # Kleid
    "d": (194, 51, 79),     # Kleid dunkel
    "W": (255, 244, 230),   # Kragen / Socke
    "B": (59, 42, 92),      # Schuh
    "X": (200, 30, 30),     # X-Auge (tot)
    # poop
    "P": (107, 68, 35),     # braun
    "p": (67, 42, 20),      # braun dunkel
    "L": (148, 100, 47),    # braun hell
    "w": (255, 255, 255),
    "k": (0, 0, 0),
    "g": (150, 200, 60),    # stink
}

# Maedchen: 6 Bilder, je 16 x 24 Pixel, Blickrichtung rechts.
# Reihenfolge: stehen, laufen 1, laufen 2, laufen 3, springen, getroffen
HEAD = [
    "....H...H..H....",
    "..H.HH.HHHHH.H..",
    "..HHHHHHHHHHHH..",
    ".HHHHhHHHHHHHHH.",
    ".HHHHHHHHHHHHH..",
    "HHHHHSSSSSSHHHH.",
    ".HHHSSSSSSSSHH..",
    "HHHHSSESSSSESH..",
    ".HHHSSSSSSSSSHH.",
    ".HHHSMSSSSSMSH..",
    "..HHHSSSRRSSH...",
    "...HHSSSSSSH....",
]
# Rumpf + Beine (12 Zeilen), der Kopf ist bei allen gleich
BODY_IDLE = [
    ".....SSSSS......",
    "....WDDDDDW.....",
    "...SDDDDDDDS....",
    "...SDDDDDDDS....",
    "...SdDDDDDDS....",
    "....DDDDDDDD....",
    "...DDDDDDDDDD...",
    "..DDDDDDDDDDDD..",
    "..dddddddddddd..",
    ".....SS..SS.....",
    ".....WW..WW.....",
    "....BBB..BBB....",
]
BODY_RUN1 = [
    ".....SSSSS......",
    "....WDDDDDW.....",
    "...SDDDDDDDS....",
    "..S.DDDDDDD.S...",
    "....dDDDDDD.....",
    "....DDDDDDDD....",
    "...DDDDDDDDDD...",
    "..DDDDDDDDDDDD..",
    "..dddddddddddd..",
    "...SS......SS...",
    "..WW........WW..",
    ".BBB........BBB.",
]
BODY_RUN2 = [
    ".....SSSSS......",
    "....WDDDDDW.....",
    "...SDDDDDDDS....",
    "...SDDDDDDDS....",
    "....dDDDDDDS....",
    "....DDDDDDDD....",
    "...DDDDDDDDDD...",
    "..DDDDDDDDDDDD..",
    "..dddddddddddd..",
    ".....SS.SS......",
    ".....WW.WW......",
    "....BBB.BBB.....",
]
BODY_RUN3 = [
    ".....SSSSS......",
    "....WDDDDDW.....",
    "...SDDDDDDDS....",
    "..S.DDDDDDD.S...",
    "....dDDDDDD.....",
    "....DDDDDDDD....",
    "...DDDDDDDDDD...",
    "..DDDDDDDDDDDD..",
    "..dddddddddddd..",
    "...SS....SS.....",
    "..WW......WW....",
    ".BBB.....BBB....",
]
BODY_JUMP = [
    "..S..SSSSS..S...",
    "..S.WDDDDDW.S...",
    "..SSDDDDDDDSS...",
    "....DDDDDDD.....",
    "....dDDDDDD.....",
    "...DDDDDDDDDD...",
    "..DDDDDDDDDDDD..",
    ".DDDDDDDDDDDDDD.",
    ".dddddddddddddd.",
    "....SS....SS....",
    "...WW......WW...",
    "..BBB......BBB..",
]

def frame(head, body):
    return head + body

HEAD_DEAD = [r.replace("E", "X").replace("RR", "R.") for r in HEAD]

FRAMES = [
    frame(HEAD, BODY_IDLE),
    frame(HEAD, BODY_RUN1),
    frame(HEAD, BODY_RUN2),
    frame(HEAD, BODY_RUN3),
    frame(HEAD, BODY_JUMP),
    frame(HEAD_DEAD, BODY_JUMP),
]

def build(frames, w, h, name):
    img = Image.new("RGBA", (w * len(frames), h), (0, 0, 0, 0))
    for fi, f in enumerate(frames):
        assert len(f) == h, (name, fi, len(f))
        for y, row in enumerate(f):
            assert len(row) == w, (name, fi, y, row)
            for x, c in enumerate(row):
                col = PAL[c]
                if col:
                    img.putpixel((fi * w + x, y), col + (255,))
    img.save(os.path.join(OUT, name + ".png"))

build(FRAMES, 16, 24, "girl")

# Hundehaufen: 4 Bilder, je 20 x 16 Pixel (wackelt, Fliege kreist)
POOP = [
[
    "....g....g..........",
    "...g......g.........",
    "....g....g.....kk...",
    ".........pp.........",
    "........ppp.........",
    "......pPPPp.........",
    ".....pPLPPPp........",
    ".....pPPPPPp........",
    "....pPLPPPPPp.......",
    "...pPPPPPPPPPp......",
    "...pPLPPPPPPPp......",
    "..pPPPPPPPPPPPp.....",
    ".pPLPPPPPPPPPPPp....",
    ".pPPPPPPPPPPPPPp....",
    "..pppppppppppppp....",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
],
[
    "..g........g........",
    "...g......g.........",
    "..g......g..........",
    ".........pp.........",
    "........ppp.........",
    "......pPPPp.........",
    ".....pPLPPPp........",
    ".....pPPPPPp........",
    "....pPLPPPPPp.......",
    "...pPPPPPPPPPp......",
    "...pPLPPPPPPPp..kk..",
    "..pPPPPPPPPPPPp.....",
    ".pPLPPPPPPPPPPPp....",
    ".pPPPPPPPPPPPPPp....",
    "..pppppppppppppp....",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
],
[
    "...g.....g..........",
    "..g.......g.........",
    "...g.....g..........",
    "kk.......pp.........",
    "........ppp.........",
    ".......pPPPp........",
    "......pPLPPPp.......",
    "......pPPPPPp.......",
    ".....pPLPPPPPp......",
    "....pPPPPPPPPPp.....",
    "....pPLPPPPPPPp.....",
    "...pPPPPPPPPPPPp....",
    "..pPLPPPPPPPPPPPp...",
    "..pPPPPPPPPPPPPPp...",
    "...pppppppppppppp...",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
],
[
    "..g........g........",
    ".g........g.........",
    "..g........g...kk...",
    ".........pp.........",
    "........ppp.........",
    "......pPPPp.........",
    ".....pPLPPPp........",
    ".....pPPPPPp........",
    "....pPLPPPPPp.......",
    "...pPPPPPPPPPp......",
    "...pPLPPPPPPPp......",
    "..pPPPPPPPPPPPp.....",
    ".pPLPPPPPPPPPPPp....",
    ".pPPPPPPPPPPPPPp....",
    "..pppppppppppppp....",
    "....................",
    "....................",
    "....................",
    "....................",
    "....................",
],
]
# Gesicht in alle Frames
for f in POOP:
    r = list(f[10]); r[6] = "w"; r[7] = "k"; r[10] = "w"; r[11] = "k"; f[10] = "".join(r)
    r = list(f[9]);  r[6] = "w"; r[7] = "w"; r[10] = "w"; r[11] = "w"; f[9] = "".join(r)
    r = list(f[12]); r[7] = "p"; r[8] = "p"; r[9] = "p"; r[10] = "p"; f[12] = "".join(r)
# Frame 3 ist verschoben, Gesicht dort um 1 nach rechts korrigieren
f = POOP[2]
for y in (9, 10, 12):
    r = list(f[y])
    row = list(POOP[0][y])
    # kopiere Gesichtspixel eins nach rechts
    for x in range(6, 12):
        r[x + 1] = row[x]
    r[6] = "P"
    f[y] = "".join(r)

# Die unteren 4 Zeilen sind leer, deshalb auf 16 Zeilen kuerzen
POOP16 = [f[:16] for f in POOP]
build(POOP16, 20, 16, "poop")
print("Sprites gespeichert in", os.path.abspath(OUT))
