# camera.py
#    Implementation of simple camera for describing views

from math import tan, radians
from ren3d.math3d import Point,Vector
from ren3d.ray3d import Ray
import ren3d.matrix as mat
from ren3d.trans3d import to_uvn


class Camera:
    """Camera is used to specify the view of the scene.


        >>> c = Camera()
	>>> c.set_perspective(60, 1.333, 20)
	>>> c.set_view(eye=(1, 2, 3), lookat=(0, 0, -10))
	>>> c.trans[0]
	[0.9970544855015816, 0.0, -0.07669649888473705, -0.7669649888473704]
	>>> c.trans[1]
	[-0.01162869315077414, 0.9884389178158018, -0.15117301096006383, -1.5117301096006381]
	>>> c.trans[2]
	[0.07580980435789034, 0.15161960871578067, 0.9855274566525744, -3.335631391747175]
	>>> c.trans[3]
	[0, 0, 0, 1]
	>>> c.set_resolution(400, 300)
	>>> r = c.ij_ray(0, 0)
	>>> r.start
	Point([1.0, 2.0, 3.0])
	>>> r.dir
	Vector([-12.900010270830052, -11.566123962675615, -17.521989305329008])
	>>> r = c.ij_ray(100, 200)
	>>> r.start
	Point([1.0, 2.0, 3.0])
	>>> r.dir
	Vector([-7.277823674777881, -0.14976036620738498, -19.7108288275589])
    """

    def __init__(self):
        self.eye = Point([0, 0, 0])
        self.window = (-10.0, -10.0, 10.0, 10.0)
        self.distance = 10
        self.trans= mat.unit(4)
        self.u = Vector([1,0,0])
        self.v = Vector([0,1,0])
        self.n = Vector([0,0,1])
        

    def set_perspective(self, hfov, aspect, distance):
        """ Set up perspective view
        hfov is horizontal field of view (in degrees)
        aspect is the aspect ratio horizontal/vertical
        distance is distance from eye to focal plane.

        >>> c = Camera()
        >>> c.set_perspective(60, 1.333, 20)
        >>> c.eye
        Point([0.0, 0.0, 0.0])
        >>> c.distance
        20
        >>> c.window
        (-11.547005383792515, -8.662419642755076, 11.547005383792515, 8.662419642755076)
        """
        self.distance = distance
        angle = radians(hfov/2)
        half_win_length = tan(angle)*self.distance
        half_win_height = half_win_length/aspect
        self.window = (-half_win_length, -half_win_height,
                       half_win_length, half_win_height)
        

    def set_view(self,eye,lookat,up=(0,1,0)):
        self.eye = Point(eye)
        lookat = Point(lookat)
        up = Vector(up)
        self.n = (self.eye-lookat).normalized()
        self.u = up.cross(self.n).normalized()
        self.v = self.n.cross(self.u).normalized()
        self.trans = to_uvn(self.u,self.v,self.n,self.eye)
        #print(type(self.u),type(self.v),type(self.n))
    
            
        

    # ------------------------------------------------------------
    # These methods used for ray tracing

    def set_resolution(self, width, height):
        """ Set resolution of pixel sampling across the window.
        """
        
        l,b,r,t = self.window
        self.dx =(r-l)/width
        self.dy=(t-b)/height

    def ij_ray(self, i, j):
        """ return the ray from the eye through the ijth pixel.
        >>> c = Camera()
        >>> c.set_resolution(400, 300)
        >>> c.ij_ray(-0.5, -0.5)
        Ray(Point([0.0, 0.0, 0.0]), Vector([-10.0, -10.0, -10.0]))
        >>> c.ij_ray(399.5, 299.5)
        Ray(Point([0.0, 0.0, 0.0]), Vector([10.0, 10.0, -10.0]))
        >>> c.ij_ray(0, 0)
        Ray(Point([0.0, 0.0, 0.0]), Vector([-9.975, -9.966666666666667, -10.0]))
        >>> c.ij_ray(399/2, 299/2)
        Ray(Point([0.0, 0.0, 0.0]), Vector([0.0, 0.0, -10.0]))
        >>>

        """
        
        l,b,r,t = self.window
        x = (l + self.dx*(0.5+i))
        y = (b + self.dy*(0.5+j))
        z= -self.distance

        ray_dir = self.u*x + self.v*y + self.n*z
        ray_start = self.eye
        ray = Ray(ray_start,ray_dir)

        return ray


if __name__ == "__main__":
    import doctest
    doctest.testmod()


#set_view(eye,lookat,upish)
#UVN - coord system for camera
#n = (eye-lookat).normalized()
#u = (upish.cross(n)).normalized()
#v = (n.cross(u)).normalized

#any world point(x,y,z)= eye+ x'*u +y'*v + z'*n

#pure rotation:
    #u.dot(x,y,z) = x'
    #v.dot(x,y,z) = y'
    #n.dot(x,y,z) = z'

"""
main color of objests appearence - diffuse lighting
to simulate absorption and reemitance o photons in different wavelengths we use
    Lambers law:
            The diffuse illumination is proportional to the cosine of the angle
            of surface to the light

cosine of angle between a line (betwen the up vector of plane's starting point
    and light source) and the plane itself

lvec = unit vector from p to light(normalized)
norn = unit vector normal(surface normal returned from intersect) to
        surface(normalized)

lambert = max(0, lvec . norm)
color = lambert* rgb_surface

light is at eye *at this point in project*
"""
