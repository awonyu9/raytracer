# test5.py
#   A nice scene from spheres, boxes, and squares

from ren3d.scenedef import *


board = Transformable(Box(color=(.3, .3, .8), texture=Boxtexture("textures/wood.ppm")))
thick = .2
board.scale(3, thick, 3).translate(0, -thick/2, 0)
scene.add(board)

"""
line = Transformable(Square(BLACK_PLASTIC))
line.scale(2.75, .01, .1)
line.translate(0, .0001, 0)
line1 = Transformable(line).translate(0, 0, .5)
scene.add(line1)
line2 = Transformable(line).translate(0, 0, -.5)
scene.add(line2)
line3 = Transformable(line).rotate_y(90).translate(-.5, 0, 0)
scene.add(line3)
line4 = Transformable(line).rotate_y(90).translate(.5, 0, 0)
scene.add(line4)
"""

oh = Sphere((0, 0, 0), .5, GOLD)
oh1 = Transformable(oh)
oh1.scale(.70, .3, .70).translate(0, thick/2, 0)
scene.add(oh1)

oh2 = Transformable(oh).scale(.7, .3, .7).translate(1, thick/2, 0)
scene.add(oh2)

oh3 = Transformable(oh).scale(.7, .3, .7).translate(-1, thick/2, -1)
scene.add(oh3)

scene.add(Transformable(oh).scale(.7, .3, .7).translate(0, thick/2, 1))

x = .2
exleg1 = Transformable(Sphere((0, 0, 0), .5, COPPER)
                       ).scale(.8, x, x).rotate_y(45)
exleg2 = Transformable(Sphere((0, 0, 0), .5, COPPER)
                       ).scale(.8, x, x).rotate_y(-45)
ex = Group()
ex.add(exleg1)
ex.add(exleg2)

ex1 = Transformable(ex).translate(-1, thick/2, 0)
scene.add(ex1)

ex2 = Transformable(ex).translate(-1, thick/2, 1)
scene.add(ex2)

ex3 = Transformable(ex).translate(0, thick/2, -1)
scene.add(ex3)

ex4 = Transformable(ex).translate(1, thick/2, -1)
scene.add(ex4)

ex5 = Transformable(ex).translate(1, thick/2, 1)
scene.add(ex5)

camera.set_view((2, 2.5, 4), (-.2, -.5, 0), (0, 1, 0))
camera.set_perspective(45, 1.33, 5)

scene.set_light((0, 20, 0), (.8, .8, .8))
scene.add_light((0, 20, 20), (.3, .3, .3))
scene.ambient = (.4, .4, .4)
scene.background = (.2, .3, .2)
scene.shadows = True
scene.textures = True
