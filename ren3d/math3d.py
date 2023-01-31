# math3d.py
# implementation of points and vectors in 3-space


from math import sqrt
import ren3d.matrix as mat



class Point:
    """A location in 2- or 3-space

    """

    def __init__(self, coords):
        """ A point in 2- or 3-space
        >>> p2 = Point([1,2])
        >>> p3 = Point([1,2,3])
        """
        self._coords = [float(v) for v in coords]

    def __repr__(self):
        """ 
        >>> Point([1,2,3])
        Point([1.0, 2.0, 3.0])
        """
        return "Point(" + str(self._coords) + ")"

    @property
    def x(self):
        return self._coords[0]

    @x.setter
    def x(self, v):
        self._coords[0] = float(v)

    @property
    def y(self):
        return self._coords[1]

    @y.setter
    def y(self, v):
        self._coords[1] = float(v)

    @property
    def z(self):
        return self._coords[2]

    @z.setter
    def z(self, v):
        self._coords[2] = float(v)

    def __getitem__(self, i):
        return self._coords[i]

    def __setitem__(self, i, value):
        self._coords[i] = float(value)

    def __iter__(self):
        """ Point is a sequence of its coordinates
        >>> p = Point([1,2,3])
        >>> tuple(p)
        (1.0, 2.0, 3.0)
        >>> list(p)
        [1.0, 2.0, 3.0]
        >>> for v in p: print(v)
        1.0
        2.0
        3.0
        >>> x, y, z = p
        >>> x, y, z
        (1.0, 2.0, 3.0)
        """
        return iter(self._coords)

    def __sub__(self, other):
        """ Difference of Point with another Point or a Vector

        A point minus a point produces a vector.
        A point minus a vector produces a point.
        
       >>> Point([1,2,3]) - Point([5,-3,2])
       Vector([-4.0, 5.0, 1.0])
        >>> Point([1,2,3]) - Vector([5,-3,2])
        Point([-4.0, 5.0, 1.0])
        >>>

        """
        restype = Vector if type(other) == Point else Point
        return restype([a-b for a, b in zip(self, other)])

    def trans(self,transform):
        p = mat.apply(transform,list(self)+[1])
        return Point(p[0:3])
        


class Vector:
    """A vector in 2- or 3-space
    """

    def __init__(self, coords):
        """
        >>> v1 = Vector([1, 2, 3])
        >>> v2 = Vector([4.3, 5.2])

        """
        self._coords = [float(v) for v in coords]
        
    def __repr__(self):
        """
        >>> Vector([1,2,3])
        Vector([1.0, 2.0, 3.0])
        """
        return "Vector(" + str(self._coords) + ")"

    @property
    def x(self):
        return self._coords[0]

    @x.setter
    def x(self, v):
        self._coords[0] = float(v)

    @property
    def y(self):
        return self._coords[1]

    @y.setter
    def y(self, v):
        self._coords[1] = float(v)

    @property
    def z(self):
        return self._coords[2]

    @z.setter
    def z(self, v):
        self._coords[2] = float(v)
    
    def __iter__(self):
        """
        >>> list(Vector([1,2,3]))
        [1.0, 2.0, 3.0]
        """
        return iter(self._coords)

    def __getitem__(self, i):
        """ get ith item 
        >>> v = Vector((1, 3, 5))
        >>> v[0]
        1.0
        >>> v[2]
        5.0
        
        """
        assert i < len(self._coords), "Invalid index for vector"
        return self._coords[i]

    def __setitem__(self, i, v):
        """ set ith item 

        >>> v = Vector((1, 3, 5))
        >>> v[1] = 4
        >>> v[1]
        4.0

        """
        assert i < len(self._coords), "Invalid index for vector"
        self._coords[i] = float(v)
        

    def __rmul__(self, s):
        """ multiplication by a preceeding scalar

        >>> 3 * Vector([1,2,3])
        Vector([3.0, 6.0, 9.0])
        """
        return Vector([i*s for i in self])

    def __mul__(self, s):
        """ multiplication by a succeeding scalar
        >>> Vector([1,2,3]) * 3
        Vector([3.0, 6.0, 9.0])
            """
        return Vector([i*s for i in self])

    def __add__(self, other):
        """ vector addition with other on right
        the result type depends on other: 
            vector + point --> point
            vector + vector --> vector

        >>> Vector([3, -1, 2]) + Point([1, 2, 3])
        Point([4.0, 1.0, 5.0])
        >>> Vector([3, -1, 2]) + Vector([1, 2, 3])
        Vector([4.0, 1.0, 5.0])
        """
        restype = Point if type(other) == Point else Vector
        return restype([float(a+b) for a,b in zip(self,other)])

    def __radd__(self, other):
        """ vector addition with other (point or vector) on left (see __add__)

        >>> Vector([1,2,3]) + Vector([4,5,6])
        Vector([5.0, 7.0, 9.0])
        """
        restype = Point if type(other) == Point else Vector
        return restype([float(a+b) for a,b in zip(self,other)])

    def __neg__(self):
        """negation
        >>> -Vector([1,-2,3])
        Vector([-1.0, 2.0, -3.0])
        """
        return Vector([-i for i in self])
        
        

    def __sub__(self, other):
        """vector subtraction
        >>> Vector([1,2,3]) - Vector([-3,1,2.5])
        Vector([4.0, 1.0, 0.5])
        """
        return Vector([a-b for a,b in zip(self,other)])

    def dot(self, other):
        """ Vector dot product

        >>> Vector([1,2,3]).dot(Vector([2,3,4]))
        20.0
        """
        return sum([a*b for a,b in zip(self,other)])

    def cross(self, other):
        """ Vector cross product

        >>> Vector([1,2,3]).cross(Vector([4,5,6]))
        Vector([-3.0, 6.0, -3.0])
        """
        x = self.y*other.z - self.z*other.y
        y = self.z*other.x - self.x*other.z
        z = self.x*other.y - self.y*other.x
        return Vector([x,y,z])

    def mag2(self):
        """ Square of magnitude

        >>> Vector([1,2,3]).mag2()
        14.0
        """
        return sum(i**2 for i in self)

    def mag(self):
        """ Magnitude
        >>> Vector([1,2,3]).mag()
        3.7416573867739413
        """
        return sqrt(self.mag2())
        

    def normalize(self):
        """ make this vector unit length

        >>> v = Vector([1,2,3])
        >>> v.normalize()
        >>> v
        Vector([0.2672612419124244, 0.5345224838248488, 0.8017837257372732])
        """
        magnitude= self.mag()
        for i in range (len(self._coords)):
            self[i] /= magnitude

    def normalized(self):
        """ return normalized version of this vector
        >>> v = Vector([1,2,3])
        >>> v.normalized()
        Vector([0.2672612419124244, 0.5345224838248488, 0.8017837257372732])
        >>> v
        Vector([1.0, 2.0, 3.0])
        """
        m = self.mag()
        return Vector([i/m for i in self])

    def reflect(self,n):
        return self - 2*(self.dot(n))*n

    def trans(self,transform):
        p = mat.apply(transform,list(self)+[0])
        return Vector(p[0:3])


if __name__ == "__main__":
    import doctest
    doctest.testmod()
