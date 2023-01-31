# anaglyph_red_blue.py
# by Alexandra Wonyu 2022/5/9

"""
Simple image filter program applies a sepia effect
"""

import sys

from ren3d.image import Image


def anaglyph_red_blue(img1, img2, outfilename, animate=False):
    img1 = Image(img1)
    img2 = Image(img2)
    w, h = img1.size
    img = Image((w, h))
    for y in range(h):
        for x in range(w):
            r1, g1, b1 = img1[x, y]
            r2, g2, b2 = img2[x, y]

            left_eye = round(0.299*r1 + 0.589*g1 + 0.174*b1)
            right_eye = round(0.299*r2 + 0.589*g2 + 0.174*b2)
            
            r = left_eye if left_eye <= 255 else 255
            b = right_eye if right_eye <= 255 else 255

            img[x, y] = (r, 0, b)
        if animate:
            img.show()
    img.save(outfilename)