# scene5 a single transformed sphere

from ren3d.scenedef import *

# tranformable unit sphere
sphere1 = Transformable(Sphere(color=(.8, .3, .3)))
sphere1.scale(20, 5, 5)
sphere1.rotate_y(45)
sphere1.rotate_z(45)
sphere1.translate(0, 0, -50)

# alternatively, these could all be done at once:
#sphere1.scale(20, 5, 5).rotate_y(45).rotate_z(45).translate(0,10,-50)

scene.add(sphere1)

scene.set_light((0, 100, 100), (1, 1, 1))
scene.ambient = (.4, .4, .4)
scene.background = (1, 1, 1)

camera.set_view((0, 0, 0), (0, 0, -50), (0, 1, 0))
camera.set_perspective(55, 1.0, 3)
