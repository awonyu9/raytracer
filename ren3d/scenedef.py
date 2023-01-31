# scenedef.py
#    A scene is a collection of modeling elements.
#    This file is the basic "header" needed to define scenes


from ren3d.rgb import RGB
from ren3d.models import Sphere, Group, Box
from ren3d.camera import Camera
from ren3d.math3d import Point
from ren3d.materials import *
from ren3d.textures import *
import ren3d.matrix as mat
from ren3d.trans3d import *
from ren3d.bvh import make_BVH
from ren3d.mesh import Mesh


# ----------------------------------------------------------------------
class Scene:

    def __init__(self):
        self.camera = Camera()
        #self.objects = Group()
        self.objects= []
        self.background = (0, 0, 0)
        self.ambient= (0.2,0.2,0.2)
        self.lights = [(Point((0,0,0)),RGB((0,0,0)))]
        self.reflections = 8
        self.textures = True

        self._surface = None

    def set_light(self,pos,color):
        self.lights = [(Point(pos),RGB(color))]

    def add_light(self,pos,color):
        self.lights.append((Point(pos),RGB(color)))

    def add(self, object):
        #self.objects.add(object)
        self.objects.append(object)
        self._surface = None


    @property
    def surface(self):
        if self._surface is None:
            self._surface = make_BVH(self.objects)
        return self._surface


    @property
    def background(self):
        return self._background

    @background.setter
    def background(self, color):
        self._background = RGB(color)

    @property
    def ambient(self):
        return self._ambient
    @ambient.setter
    def ambient(self,color):
        if type(color) == float:
            color = [color]*3
        self._ambient = RGB(color)

class Transformable:
    """
    >>> s = Transformable(Sphere(color=(0, 0, 0)))
    >>> s.scale(2,3,4).rotate_y(30).translate(5,-3,8)
    >>> s.trans[0]
    [1.7320508075688774, 0.0, 1.9999999999999998, 5.0]
    >>> s.trans[1]
    [0.0, 3.0, 0.0, -3.0]
    >>> s.trans[2]
    [-0.9999999999999999, 0.0, 3.464101615137755, 8.0]
    >>> s.trans[3]
    [0.0, 0.0, 0.0, 1.0]
    >>> s.itrans[0]
    [0.43301270189221935, 0.0, -0.24999999999999997, -0.16506350946109705]
    >>> s.itrans[1]
    [0.0, 0.3333333333333333, 0.0, 1.0]
    >>> s.itrans[2]
    [0.12499999999999999, 0.0, 0.21650635094610968, -2.357050807568877]
    >>> s.itrans[3]
    [0.0, 0.0, 0.0, 1.0]
    >>> s.ntrans[0]
    [0.43301270189221935, 0.0, 0.12499999999999999, 0.0]
    >>> s.ntrans[1]
    [0.0, 0.3333333333333333, 0.0, 0.0]
    >>> s.ntrans[2]
    [-0.24999999999999997, 0.0, 0.21650635094610968, 0.0]
    >>> s.ntrans[3]
    [-0.16506350946109705, 1.0, -2.357050807568877, 1.0]
    >>> 
    """

    def __init__(self,obj):
        #self.obj = obj
        
        self.trans = mat.unit(4)
        self.itrans = mat.unit(4)
        self.ntrans = mat.unit(4)
        self.surface= obj
        self.bbox = self.surface.bbox

    def scale(self,sx,sy,sz):
        trans = scale(sx,sy,sz)
        itrans= scale(1/sx,1/sy,1/sz)
        self._set_trans(trans,itrans)

        return self


    def translate(self,dx,dy,dz):
        trans= translate(dx,dy,dz)
        itrans= translate(-dx,-dy,-dz)
        self._set_trans(trans,itrans)

        return self


    def rotate_x(self,angle):
        trans = rotate_x(angle)
        itrans= rotate_x(-angle)
        self._set_trans(trans,itrans)

        return self

    def rotate_y(self,angle):
        trans = rotate_y(angle)
        itrans = rotate_y(-angle)
        self._set_trans(trans,itrans)

        return self

    def rotate_z(self,angle):
        trans = rotate_z(angle)
        itrans= rotate_z(-angle)
        self._set_trans(trans,itrans)

        return self

    def iter_polygons(self):
        for poly in self.surface.iter_polygons():
            transpoints = [p.trans(self.trans) for p in poly.points]
            poly.points = transpoints
            yield poly
            
            

    def intersect(self,ray,interval,info):
        if not self.bbox.hit(ray,interval):
            return False
        transray = ray.trans(self.itrans)
        intrsect = self.surface.intersect(transray,interval,info)
        if intrsect:
            info.normal = info.normal.trans(self.ntrans).normalized()
            info.point = info.point.trans(self.trans)
        return intrsect
    
    def _set_trans(self,t,it):
        self.trans = mat.mul(t,self.trans)
        self.itrans = mat.mul(self.itrans,it)
        self.ntrans = mat.transpose(self.itrans)
        self.bbox = self.surface.bbox.transform(self.trans) 
        
        
    
     
        
# ----------------------------------------------------------------------
# global scene
#   for files that define a scene use: from scenedef import *


scene = Scene()
camera = scene.camera

# ----------------------------------------------------------------------
# use this function to load scene modules for rendering


def load_scene(modname):
    if modname.endswith(".py"):
        modname = modname[:-3]
    scene = __import__(modname).scene
    return scene, modname


if __name__ == "__main__":
    import doctest
    doctest.testmod()
