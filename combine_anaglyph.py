# combine_anaglyph.py

import sys

from ren3d.anaglyph_red_blue import *

def combine(w, h):
    for i in range(1, 90):
        img1 = f"rb-left/scene3h-behind-rt-{w}-{h}-{i}.ppm"
        img2 = f"rb-right/scene3h-behind-shift-rt-{w}-{h}-{i}.ppm"
        anaglyph_red_blue(img1, img2, f"rb-final/scene-rb-{i}.ppm")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: pypy combine_anaglyph.py width height")
        sys.exit()
    w, h = int(sys.argv[1]), int(sys.argv[2])
    combine(w, h)