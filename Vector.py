from math import *

class Vector(object):
    """General 2D vector class used and utilities.
       Supports vector addition and scalar multiplictaion."""

    def __init__(self, x=0, y=0):
        self._x = x
        self._y = y
        self._mag = 0
        self._theta = 0
        self._updatePolarCoords()


    #--------------------------------------------------------------
    # Descriptor methods

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")" 
    def __str__(self):
        return (self.__repr__() + 
            " Mag: " + str(self.mag) + " Theta: " + str(self.theta))

    #--------------------------------------------------------------
    # Local utility functions to maintain the consistancy between
    # vector attributes

    def _updatePolarCoords(self):
        """Updates the polar coordinates. Meant to be used after a change in
           the cartesian coordiantes is made"""
        self._mag = sqrt(self.x**2 + self.y**2)
        self._theta = atan2(self.y, self.x)

    def _updateCartesianCoords(self):
        """Update the cartesian coodrinates. Meant to be used after a change in
           the polar coordiantes is made"""
        self._x = self.mag * cos(self.theta)
        self._y = self.mag * sin(self.theta)


    #----------------------------------------------------------------
    # Getters for vector attributes

    def coords(self): 
        """Returns a tuple representing the cartesian coordinates
           of the vector"""
        return (self.x, self.y)
    
    def int_coords(self):
        """Returns a tuple of (int(x), int(y)). Useful for drawing"""
        return (int(self.x), int(self.y))

    @property
    def x(self): 
        """The x element of the vector"""
        return self._x;

    @property
    def y(self): 
        """The y element of the vector"""
        return self._y

    @property
    def mag(self): 
        """The magnitue of the vector. sqrt(x**2 + y**2)"""
        return self._mag

    @property
    def theta(self): 
        """The angle of the vector in radians. 
           0 is to the right, counterclockwise"""
        return self._theta


    #----------------------------------------------------------------
    # Setters for vector attributes

    @x.setter
    def x(self, value):
        self._x = value
        self._updatePolarCoords()

    @y.setter
    def y(self, value):
        self._y = value
        self._updatePolarCoords()

    @mag.setter
    def mag(self, value):
        self._mag = value
        self._updateCartesianCoords()

    @theta.setter
    def theta(self, value):
        self._theta = value
        self._updateCartesianCoords()


    #----------------------------------------------------------------
    # Vector utility functions

    def dot(self, other):
        """Computes the dot product of this vector and another vector"""
        return self.x * other.x + self.y * other.y

    # Operator definitions for vector addidon and subtraction

    def __add__(self, v):
        return Vector(self.x + v.x, self.y+v.y)
    def __sub__(self, v):
        return Vector(self.x-v.x, self.y-v.y)


    # Operator definitions for scalar multiplication and division

    def __mul__(self, c):
        return Vector(self.x*c, self.y*c)
    def __rmul__(c, v):
        return Vector(v.x*c, v.y*c)
    def __div__(self, c):
        return Vector(self.x/c, self.y/c)
    def __truediv__(self, c):
        return Vector(self.x/c, self.y/c)
