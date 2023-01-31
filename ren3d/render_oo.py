# render_oo.py

"""FrameBuffer that keeps the z coordinates of points to implement a
depth buffer for hidden surface removal.

"""


from math import inf

from collections import namedtuple, defaultdict
import ren3d.matrix as mat



def render_signature(scene, img):
    """Render signature view of scene

    All polygons are drawn with their assigned raw color

    """
    camera = scene.camera
    img.clear(scene.background.quantize(255))
    d = -camera.distance
    fb = FrameBuffer(img, camera.window)
    for poly in scene.surface.iter_polygons():
        #draw triangle fan of the projected polygon
        points = [(d*p.x/p.z, d*p.y/p.z, p.z) for p in poly.points]
        colors = [poly.color]*3  # use raw polygon color for all 3 vertices
        for i in range(1, len(poly.points)-1):
            fb.draw_filled_triangle([points[0], points[i], points[i+1]], colors)

def render_wireframe(scene, img):
    """Render wireframe view of scene into img
    """
    # put your render_wireframe here and tweak it to use the new FB
    camera = scene.camera
    group = scene.objects
    window = camera.window
    dist = camera.distance
    img.clear(scene.background.quantize(255))
    fb = FrameBuffer(img,window)
    for poly in scene.surface.iter_polygons():
        campoints = [p.trans(camera.trans) for p in poly.points]
        points = [(-dist * p.x/p.z , -dist * p.y/p.z,p.z) for p in campoints] 
        fb.draw_polygon(points,poly.color)


def render_gouraud(scene, img):
    """Render scene with Gouraud shaded polygons"""
    camera = scene.camera
    group = scene.objects
    window = camera.window
    d = -camera.distance
    img.clear(scene.background.quantize(255))
    fb = FrameBuffer(img,window)
    for poly in group.iter_polygons():
        #draw triangle fan of the projected polygon
        points = [(d*p.x/p.z, d*p.y/p.z, p.z) for p in poly.points]
        colors = lambert_colors(scene,poly)  # use raw polygon color for all 3 vertices
        for i in range(1, len(poly.points)-1):
            fb.draw_filled_triangle([points[0], points[i], points[i+1]],
                                    [colors[0],colors[i],colors[i+1]])
        


def lambert_colors(scene, poly):
    """return lambert shaded colors corresponding to veritices of polygon

    helper method for render_gouraud. The poly record will need to have:
       points: list of  vertices of the polygon
       normals: list of normal vectors (one for each point)
       color: an RGB color of the polygon
    """
    eye = scene.camera.eye
    colors = []
    for i in range(len(poly.points)):
        normal = poly.normals[i]
        lvec =(scene.light - poly.points[i]).normalized()
        lambert  = max(0, lvec.dot(normal))
        color = lambert*poly.color + scene.ambient*poly.color
        colors.append(color)
    return colors


# ---------------------------------------------------------------------------
# Helper class
pixloc = namedtuple("pixloc", "x y z")


class FrameBuffer:
    """ Wrapper for images to provide a window mapping and drawing primitives.
    This is a stripped down combination of elements from our Painter
    and Render2d projects

    This version is updated to keep the z component of the points to use for 
    depth buffering.
    """
    #Add data structure that for each pixel stores a depth for that pixel
    #Data structure to use -> collections.defaultdict
    #depth_buff = defaultdict(lambda: -inf)
    #use that as an additional check when settingga pixel
    #is the z of this pixel bigger than the oneset in framebuffer?
    #if so set

    def __init__(self, img, window):
        self.img = img
        self.size = img.size
        # viewport dimensions are 1 unit larger than pixel dimensions
        w, h = self.size[0] + 1, self.size[1] + 1
        l, b, r, t = window
        self.transform = [[w/(r-l), 0.0, 0.0, (-.5*r-(w-.5)*l)/(r-l)],
                          [0.0, h/(t-b), 0.0, (-.5*t-(h-.5)*b)/(t-b)],
                          [0.0, 0.0, 1.0, 0.0],
                          [0.0, 0.0, 0.0, 1.0]]
        self.depth_buffer = defaultdict(lambda: -inf)

    def transpt(self, point):
        # Transform point from window (world) coordinates to pixel coordinates
        # x and y are ints, z is a float indicating depth
        x, y, z, _ = mat.apply(self.transform, point+(1,))
        return pixloc(int(x + .5), int(y + .5), z)

    def set_pixel(self, loc, z, color):
        w, h = self.size
        if 0 <= loc[0] < w and 0 <= loc[1] < h:
            if self.depth_buffer[loc] < z:
                self.depth_buffer[loc]=z
                self.img[loc] = color.diffuse.quantize(255)

    def draw_line(self, a, b, rgb):
        # pre: a and b are pixel locations (int, int, float)
        if a[:2] == b[:2]:   # handle degenerate case same pixel location
            self.set_pixel(a[:2], a.z, rgb)
            return
        # Otherwise, handle the general case
        dx = b.x - a.x
        dy = b.y - a.y
        dz = b.z - a.z 
        if abs(dx) > abs(dy):  # x changes faster, walk it
            if a.x > b.x:
                a, b = b, a
            yinc = dy/dx
            y = a.y
            zinc = dz/dx
            z = a.z
            for x in range(a.x, b.x + 1):
                self.set_pixel((x, round(y)), z, rgb)
                y += yinc
                z += zinc
        else:
            if a.y > b.y:
                a, b = b, a
            xinc = dx/dy
            x = a.x
            zinc = dz/dy
            z = a.z
            for y in range(a.y, b.y + 1):
                self.set_pixel((round(x), y), z, rgb)
                x += xinc
                z += zinc

    def draw_polygon(self, points, color):
        # points are 3D window points (tuple of floats)
        pixels = [self.transpt(p) for p in points]
        for i in range(len(pixels) - 1):
            self.draw_line(pixels[i], pixels[i+1], color)
        self.draw_line(pixels[-1], pixels[0], color)

    def draw_filled_triangle(self, pts, rgbs):
        """Draw a filled triangle, smoothly interpolating vertex 

        pts is a list 3D window points (tuple of floats)
        rgbs is a list of corresponding rbgs
        """
        # make pixlocs a, b, c
        a, b, c = tuple(self.transpt(p) for p in pts)
        # make sure rgbs is a list of colors, one for each vertex
        if type(rgbs) != list:
            rgbs = [rgbs, rgbs, rgbs]

        def linefunc(p0, p1):
            x0, y0, _ = p0
            x1, y1, _ = p1

            def f(x, y):
                return (y0-y1)*x + (x1-x0)*y + x0*y1-x1*y0

            return f
        try:
            fbc = linefunc(b, c)
            alphamul = 1 / fbc(a.x, a.y)
            fac = linefunc(a, c)
            betamul = 1 / fac(b.x, b.y)
            fab = linefunc(a, b)
            gammamul = 1 / fab(c.x, c.y)
        except ZeroDivisionError:
            # protection against degenerate triangles
            return

        for x in range(min(a.x, b.x, c.x), max(a.x, b.x, c.x)+1):
            for y in range(min(a.y, b.y, c.y), max(a.y, b.y, c.y)+1):
                alpha = fbc(x, y) * alphamul
                if alpha < 0:
                    continue
                beta = fac(x, y) * betamul
                if beta < 0:
                    continue
                gamma = fab(x, y) * gammamul
                if gamma < 0:
                    continue

                # point is inside draw it with interpolated z and color
                z = alpha*a.z + beta*b.z + gamma*c.z
                rgb = alpha*rgbs[0] + beta*rgbs[1] + gamma*rgbs[2]
                self.set_pixel((x, y), z, rgb)

    
