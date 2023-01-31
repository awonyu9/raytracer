# run_wf.py
#   Create wireframe image of scene.
# usage: pypy run_wf.py scene0 320 240

import sys
import time

from ren3d.scenedef import load_scene
from ren3d.image import Image
from ren3d.render_oo import render_signature,render_gouraud


def main():
    if len(sys.argv) != 4:
        print("Usage: python run_sig.py scene0 320 240")
    scene, scenename = load_scene(sys.argv[1])
    size = int(sys.argv[2]), int(sys.argv[3])
    img = Image(size)
    t1 = time.time()
    render_gouraud(scene, img)
    t2 = time.time()
    img.show()
    img.save("images/{}-sig-{:d}-{:d}.ppm".format(scenename, *size))
    print(t2-t1, "seconds")


if __name__ == "__main__":
    main()
