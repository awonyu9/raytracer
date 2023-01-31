# trans3d.py
"""matrices for performing 3D transformations in homogeneous coordinates"""

from math import radians, sin, cos, tan
from ren3d.math3d import Point, Vector
import ren3d.matrix as mat


def translate(dx=0., dy=0., dz=0.):
    """ returns matrix that translates by dx, dy, dz

    >>> translate(2,1,3)
    [[1.0, 0.0, 0.0, 2.0], [0.0, 1.0, 0.0, 1.0], [0.0, 0.0, 1.0, 3.0], [0.0, 0.0, 0.0, 1.0]]
    """
    unit= mat.unit(4)
    trans = [dx,dy,dz,1]
    for r in range(mat.nrows(unit)):
        unit[r][-1] = float(trans[r])
    return unit


def scale(sx=1., sy=1., sz=1.):
    """ returns matrix that scales by sx, sy, sz

    >>> scale(2,3,4)
    [[2.0, 0.0, 0.0, 0.0], [0.0, 3.0, 0.0, 0.0], [0.0, 0.0, 4.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    >>>
    """
    unit =mat.unit(4)
    scale = [sx,sy,sz,1]
    for r in range(len(unit)):
        unit[r][r]*= scale[r]
    return unit


def rotate_x(angle):
    """ returns matrix that rotates angle degrees about X axis

    >>> rotate_x(30)
    [[1.0, 0.0, 0.0, 0.0], [0.0, 0.8660254037844387, -0.49999999999999994, 0.0], [0.0, 0.49999999999999994, 0.8660254037844387, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    angle = radians(angle)
    return [[1.0,  0.0,     0.0,        0.0],
            [0.0,cos(angle),-sin(angle),0.0],
            [0.0,sin(angle),cos(angle), 0.0],
            [0.0,  0.0,     0.0,        1.0]]


def rotate_y(angle):
    """ returns matrix that rotates by angle degrees around the Y axis

    >>> rotate_y(30)
    [[0.8660254037844387, 0.0, 0.49999999999999994, 0.0], [0.0, 1.0, 0.0, 0.0], [-0.49999999999999994, 0.0, 0.8660254037844387, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    angle = radians(angle)
    return [[cos(angle), 0.0,sin(angle), 0.0],
            [0.0,        1.0,   0.0,     0.0],
            [-sin(angle),0.0,cos(angle), 0.0],
            [0.0,        0.0,   0.0,     1.0]]

def rotate_z(angle):
    """returns a matrix that rotates by angle degrees around Z axis

    >>> rotate_z(30)
    [[0.8660254037844387, -0.49999999999999994, 0.0, 0.0], [0.49999999999999994, 0.8660254037844387, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0], [0.0, 0.0, 0.0, 1.0]]
    """
    angle = radians(angle)
    return [[cos(angle),-sin(angle),0.0,0.0],
            [sin(angle),cos(angle),0.0, 0.0],
            [0.0,         0.0,     1.0, 0.0],
            [0.0,         0.0,     0.0, 1.0]]


def to_uvn(u, v, n, eye):
    """returns a matrix that transforms a point to UVN coordinates

    >>> to_uvn(Vector([1.0, 2.0, 3.0]), Vector([4.0, 5.0, 6.0]), Vector([7.0, 8.0, 9.0]), Vector([10.0, 11.0, 12.0]))
    [[1.0, 2.0, 3.0, -68.0], [4.0, 5.0, 6.0, -167.0], [7.0, 8.0, 9.0, -266.0], [0, 0, 0, 1]]
    """
    
    return [[u.x,u.y,u.z,-u.dot(eye)],
            [v.x,v.y,v.z,-v.dot(eye)],
            [n.x,n.y,n.z,-n.dot(eye)],
            [0  , 0,  0,       1    ]]
    

if __name__ == '__main__':
    import doctest
    doctest.testmod()
