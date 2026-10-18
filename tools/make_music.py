# Mit diesem Skript habe ich die Hintergrundmusik erzeugt (Chiptune-Stil).
# Die Melodie ist "Korobeiniki", ein russisches Volkslied aus dem 19. Jahrhundert (gemeinfrei),
# bekannt als Tetris-Melodie. Die Toene werden als Rechteckwellen berechnet wie bei alten Konsolen.
# Aufruf aus dem Projektordner:  python3 tools/make_music.py
# Danach umwandeln:              ffmpeg -i assets/music.wav -q:a 4 assets/music.ogg
# Benoetigt: pip install numpy
import numpy as np, wave, os

OUT = os.path.join(os.path.dirname(__file__), "..", "assets")
SR = 22050
BPM = 150
EIGHTH = 60.0 / BPM / 2

NOTES = {"C":0,"C#":1,"D":2,"D#":3,"E":4,"F":5,"F#":6,"G":7,"G#":8,"A":9,"A#":10,"B":11}
def freq(n):
    if n == "r": return 0.0
    name, octv = n[:-1], int(n[-1])
    return 440.0 * 2 ** ((NOTES[name] + (octv - 4) * 12 - 9) / 12)

# Korobeiniki (russisches Volkslied) - Melodie in Achteln
A = [("E5",2),("B4",1),("C5",1),("D5",2),("C5",1),("B4",1),
     ("A4",2),("A4",1),("C5",1),("E5",2),("D5",1),("C5",1),
     ("B4",3),("C5",1),("D5",2),("E5",2),
     ("C5",2),("A4",2),("A4",2),("r",2),
     ("r",1),("D5",2),("F5",1),("A5",2),("G5",1),("F5",1),
     ("E5",3),("C5",1),("E5",2),("D5",1),("C5",1),
     ("B4",2),("B4",1),("C5",1),("D5",2),("E5",2),
     ("C5",2),("A4",2),("A4",2),("r",2)]
B = [("E4",4),("C4",4),("D4",4),("B3",4),
     ("C4",4),("A3",4),("G#3",4),("B3",4),
     ("E4",4),("C4",4),("D4",4),("B3",4),
     ("C4",2),("E4",2),("A4",4),("G#4",8)]
MELODY = A + A + B

# Akkord-Grundtoene pro Takt (8 Achtel)
BASS_A = ["A2","A2","E2","A2","D2","A2","E2","A2"]
BASS_B = ["A2","E2","A2","E2"]
BASS_BARS = BASS_A + BASS_A + BASS_B

def square(f, n, duty=0.5):
    t = np.arange(n) / SR
    return np.where((t * f) % 1.0 < duty, 1.0, -1.0)

def env(n, attack=0.005, release=0.04):
    e = np.ones(n)
    a = int(attack * SR); r = int(release * SR)
    e[:a] = np.linspace(0, 1, a)
    if r > 0: e[-r:] *= np.linspace(1, 0, r)
    return e

def render_track(seq, duty, vol, gap=0.9):
    out = []
    for note, d in seq:
        n = int(d * EIGHTH * SR)
        f = freq(note)
        if f == 0:
            out.append(np.zeros(n)); continue
        on = int(n * gap)
        s = square(f, on, duty) * env(on) * vol
        out.append(np.concatenate([s, np.zeros(n - on)]))
    return np.concatenate(out)

lead = render_track(MELODY, 0.5, 0.28)

bass_seq = []
for root in BASS_BARS:
    up = {"A2": "E3", "E2": "B2", "D2": "A2"}[root]
    # Wechselbass: Grundton, Quinte, Grundton, Quinte ... auf jedem Achtel
    for i in range(8):
        bass_seq.append((root if i % 2 == 0 else up, 1))
bass = render_track(bass_seq, 0.25, 0.22, gap=0.7)

# einfacher Hi-Hat aus Rauschen auf jedem Achtel, Akzent auf 1 und 3
rng = np.random.default_rng(1)
hat = []
total_eighths = sum(d for _, d in MELODY)
for i in range(total_eighths):
    n = int(EIGHTH * SR)
    ln = int(0.03 * SR)
    v = 0.09 if i % 4 == 0 else 0.045
    h = rng.uniform(-1, 1, ln) * np.linspace(1, 0, ln) * v
    hat.append(np.concatenate([h, np.zeros(n - ln)]))
hat = np.concatenate(hat)

L = min(len(lead), len(bass), len(hat))
mix = lead[:L] + bass[:L] + hat[:L]
mix = np.clip(mix, -1, 1)
pcm = (mix * 32767).astype(np.int16)
with wave.open(os.path.join(OUT, "music.wav"), "wb") as w:
    w.setnchannels(1); w.setsampwidth(2); w.setframerate(SR); w.writeframes(pcm.tobytes())
print("music.wav gespeichert, Laenge:", L / SR, "Sekunden")
