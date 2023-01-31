# run_rt_right.py -- raytrace a scene with a simple progress indicator
#    usage: pypy run_rt_right.py scene0 320 240

import sys
import time
from math import tau, cos, sin

from ren3d.scenedef import load_scene
from ren3d.render_ray import raytrace
from ren3d.image import Image
from ren3d.math3d import Vector


class Progress:

    def __init__(self, size):
        self.size = size
        self.count = 0

    def show(self):
        self.count += 1
        print(str(round(self.count/self.size*100, 1))+"%", end="\r")
        sys.stdout.flush()


def main():
    scene, scenename = load_scene(sys.argv[1])
    w, h = int(sys.argv[2]), int(sys.argv[3])
    img = Image((w, h))
    x, y, z = 4, 3, 5
    d_theta = tau / 90
    theta = 0
    for i in range(90):
        scene.camera.set_view((x, y, z), (0, 0, -20))
        t1 = time.time()
        raytrace(scene, img, Progress(h).show)
        t2 = time.time()
        img.save("rb-right/{}-shift-rt-{:d}-{:d}-{}.ppm".format(scenename, w, h, i))

        x = 25 * cos(theta) 
        z = 25 * sin(theta) - 20 

        x1 = 0 - x
        z1 = -20 - z
        v = Vector((x1, y, z1)).normalized()
        x2 = -v.z
        z2 = v.x

        x += 2 * x2
        z += 2 * z2
        
        theta += d_theta

        #img.show()
        print(t2-t1, "seconds")
    input("Press <Enter> to quit")
    #img.unshow()


if __name__ == "__main__":
    main()
