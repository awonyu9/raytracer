# models.py
#   Objects used for constructing scenes

from math import sin, cos, pi, sqrt, tau
from ren3d.math3d import Point, Vector
from ren3d.rgb import RGB
from ren3d.materials import Material, make_material
from ren3d.textures import *
from ren3d.bbox import BoundingBox


# Surfaces for Scene Modeling
# ----------------------------------------------------------------------
def circle2d(c,r,n):
        cx,cy =c
        dt = tau/n
        points= [(r*cos(i*dt)+cx,r*sin(i*dt)+cy) for i in range(n)]
        points.append(points[0])
        return points

def find_normal(center,point):
        return (point-center).normalized()


class Sphere:
    def __init__(self, pos=(0, 0, 0), radius=1,
                         color=(0, 1, 0), nlat=20, nlong=20, texture=None):
        """ create a sphere
        """
        self.pos = Point(pos)
        self.radius = radius
        #self.color = RGB(color)
        self.color = make_material(color)
        self.nlat = nlat
        self.nlong = nlong
        self.bands = []
        self.normals = []
        self._make_bands_and_normals(nlat, nlong)
        axis = Vector((0, radius, 0))
        self.northpole = self.pos + axis
        self.southpole = self.pos - axis

        self.texture=texture
        
        x,y,z = self.pos
        self.bbox = BoundingBox((x-self.radius,y-self.radius, z-self.radius),
                                (x+self.radius, y+self.radius,z+self.radius))
        

    def _make_bands_and_normals(self, nlat, nlong):
        """helper method that creates a list of "self.bands"
                and a list of normals for each point on the band called
                self.normals.

        each band consists of a list of points encircling the sphere
        at a latitude. There are nlat evenly (angularly) spaced
        self.bands each with nlong points evenly spaced around the band.

        """
        cx,cy,cz= self.pos
        theta = pi/2
        dtheta = -pi/(nlat+1)

        for i in range(nlat):
            theta += dtheta
            r = self.radius*cos(theta)
            y = self.radius*sin(theta)+cy
            band= [Point((x,y,z)) for x,z in circle2d((cx,cz),r,nlong)]
            normals = [find_normal(self.pos,point) for point in band]
            self.bands.append(band)
            self.normals.append(normals)
              
    def iter_polygons(self):
        """produces a sequence of polygons on the skin of the sphere.

        Each polygon is a Record with fields "points" (a list of n points)
        and color (the color of the triangle).
        """
        northpole_normal =find_normal(self.pos,self.northpole)
        southpole_normal =find_normal(self.pos,self.southpole)
        for i in range(self.nlong):

            #Yield north triangle
            yield Record(
                points=[self.northpole,self.bands[0][i],self.bands[0][i+1]],
                color = self.color,
                normals = [northpole_normal, self.normals[0][i],
                        self.normals[0][i+1]]
                        )
            #Yield all the polygons inbetween the triangles
            for j in range(self.nlat-1):
                b0 = self.bands[j]
                b1 = self.bands[j+1]
                n0 = self.normals[j]
                n1 = self.normals[j+1]
                yield Record(
                        points = [b0[i],b1[i],b1[i+1],b0[i+1]],
                        color= self.color,
                        normals = [n0[i],n1[i],n1[i+1],n0[i+1]]
                        )
            #Yield south triangle
            yield Record(
                points =[self.southpole,self.bands[-1][i],self.bands[-1][i+1]],
                color = self.color,
                normals = [southpole_normal, self.normals[-1][i],
                        self.normals[-1][i+1]]
                )
             
    def intersect(self, ray, interval, info):
        """ returns a True iff ray intersects the sphere within the

        given time interval. The approriate intersection information
        is recorded into info, which is a Record containing:
          point: the point of intersection
          t: the time of the intersection
          normal: the surface normal at the point normal
                  info.normal(p - center).normalized()
          color: the color at the point.
        """
        #if not self.bbox.hit(ray,interval):
            #return False
        
        a = ray.dir.mag2() 
        if a==0:
                return False
        b= 2* ray.dir.dot(ray.start-self.pos)
        c = (ray.start-self.pos).mag2() - self.radius**2

        determ = b**2 - 4*a*c
        if determ < 0:
                return False
        
        t1 = (-b - sqrt(determ))/(2*a)
        if t1 in interval:
                self._setinfo(ray,t1,info)
                return True

        elif t1 < interval.high:
                t2 = (-b + sqrt(determ))/(2*a)
                if t2 in interval:
                        self._setinfo(ray,t2,info)
                        return True
        return False
        
    def _setinfo(self, ray, t, info):
        """ helper method to fill in the info record """
        
        info.point = ray.point_at(t)
        info.normal = (info.point-self.pos).normalized()
        info.t = t
        info.color = self.color
        info.uvn = self.generic_coords(info.point)
        info.texture = self.texture

    def generic_coords(self,point):
        
        u = lerp(point.x,self.pos.x-self.radius,self.pos.x+self.radius,-1,1)
        v = lerp(point.y,self.pos.y-self.radius,self.pos.y+self.radius,-1,1)
        n = lerp(point.z,self.pos.z-self.radius,self.pos.z+self.radius,-1,1)
        return Point((u,v,n))

class Box:

    def __init__(self, pos=(0.0, 0.0, 0.0), size=(1, 1, 1), color=(0,0,0), texture=None):
        self.planes = [(pos[i]-size[i]/2, pos[i]+size[i]/2) for i in range(3)]
        #self.color = RGB(color)
        self.color = make_material(color)
        self.texture = texture

        self.bbox = BoundingBox([self.planes[a][0]for a in range (3)],
                               [self.planes[a][1] for a in range (3)])

    def iter_polygons(self):
        ijseq = [(0, 0), (1, 0), (1, 1), (0, 1)]
        xs, ys, zs = self.planes
        yield Record(points=[Point((xs[0], ys[i], zs[j])) for i, j in ijseq],
                     normals=[Vector((-1, 0, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[1], ys[i], zs[j])) for i, j in ijseq],
                     normals=[Vector((1, 0, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[0], zs[j])) for i, j in ijseq],
                     normals=[Vector((0, -1, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[1], zs[j])) for i, j in ijseq],
                     normals=[Vector((0, 1, 0))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[j], zs[0])) for i, j in ijseq],
                     normals=[Vector((0, 0, -1))]*4, color=self.color)
        yield Record(points=[Point((xs[i], ys[j], zs[1])) for i, j in ijseq],
                     normals=[Vector((0, 0, 1))]*4, color=self.color)

    def intersect(self, ray, interval, info):

        #if not self.bbox.hit(ray,interval):
            #return False
        
        s, d = ray.start, ray.dir
        planes = self.planes
        hit = False
        for axis in range(3):
            if d[axis] == 0.0:
                continue
            for lh in range(2):
                t = (planes[axis][lh] - s[axis])/d[axis]
                if t not in interval:
                    continue
                p = ray.point_at(t)
                if self._inrect(p, axis):
                    hit = True
                    interval.high = t
                    info.t = t
                    info.point = p
                    info.normal = Vector([0]*3)
                    info.normal[axis] = (-1.0, 1.0)[lh]
                    info.color = self.color
                    info.uvn = self.generic_coords(info.point)
                    info.texture = self.texture
        return hit

    def _inrect(self, p, axis):
        axes = [0, 1, 2]
        axes.remove(axis)
        for a in axes:
            low, high = self.planes[a]
            if not low <= p[a] <= high:
                return False
        return True

    def generic_coords(self, pt):
        x, y, z = pt
        xs, ys, zs = self.planes
        u = lerp(x, xs[0], xs[1], -1, 1)
        v = lerp(y, ys[0], ys[1], -1, 1)
        n = lerp(z, zs[0], zs[1], -1, 1)
        return Point((u, v, n))


        
class Group:
    """ Model comprised of a group of other models.
    The contained models may be primitives (such as Sphere) or other groups.
    """

    def __init__(self):
        self.objects = []
        self.bbox = BoundingBox()

    def add(self, model):
        """ Add model to the group
        """
        self.objects.append(model)
        self.bbox.include_box(model.bbox)

    def iter_polygons(self):
        """ Produce all polygons in the group
        """
        for obj in self.objects:
            for  poly in obj.iter_polygons():
                yield poly

    def intersect(self, ray, interval, info):
        """Returns True iff ray intersects some object in the group

        If so, info is the record of the first (in time) object hit, and
        interval.max is set to the time of the first hit.
        """
        if not self.bbox.hit(ray,interval):
            return False
        
        hit = False
        for obj in self.objects:
            if obj.intersect(ray,interval,info):
                hit = True
                interval.high = info.t

        return hit

# ----------------------------------------------------------------------
class Record(object):
    """ conveience for bundling a bunch of info together. Basically
    a dictionary that can use dot notatation

    >>> info = Record()
    >>> info.point = Point([1,2,3])
    >>> info
    Record(point=Point([1.0, 2.0, 3.0]))
    >>> info.t = 3.245
    >>> info
    Record(point=Point([1.0, 2.0, 3.0]), t=3.245)
    >>> info.update(point=Point([-1,0,0]), t=5)
    >>> info.t
    5
    >>> info
    Record(point=Point([-1.0, 0.0, 0.0]), t=5)
    >>> info2 = Record(whatever=53, whereever="Iowa")
    >>> info2.whereever
    'Iowa'
    >>> 
    """

    def __init__(self, **items):
        self.__dict__.update(items)

    def update(self, **items):
        self.__dict__.update(**items)

    def __repr__(self):
        d = self.__dict__
        fields = [k+"="+str(d[k]) for k in sorted(d)]
        return "Record({})".format(", ".join(fields))


if __name__ == "__main__":
    import doctest
    doctest.testmod()
