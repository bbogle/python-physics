from math import *

class Vector:
    """General 2D vector class used and utilities.
       
       Supports vector addition and scalar multiplictaion."""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.mag = 0
        self.theta = 0
        self._updatePolarCoords()

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

    # Descriptor methods
    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")" 
    def __str__(self):
        return (self.__repr__() + 
            " Mag: " + str(self.mag) + " Theta: " + str(self.theta))

    def _updatePolarCoords(self):
        """Updates the polar coordinates. Meant to be used after a change in
           the cartesian coordiantes is made"""
        self.mag = sqrt(self.x**2 + self.y**2)
        self.theta = atan2(self.y, self.x)

    def _updateRect(self):
        """Update the cartesian coodrinates. Meant to be used after a change in
           the polar coordiantes is made"""
        self.x = self.mag * cos(self.theta)
        self.y = self.mag * sin(self.theta)

    def setPolarCoords(self, m, t):
        """Sets the magnitude and direction of the vector"""
        self.mag = m
        self.theta = t
        self._updateRect()

    def setRect(self, x, y):
        """Sets the x and y elements of the vector"""
        self.x = x
        self.y = y
        self._updatePolarCoords()

    def rect(self): return (self.x, self.y)
    def pol(self): return (self.mag, self.theta)

    def setMag(self, m):
        """Sets the magnitude of the vector"""
        self.mag = m
        self._updateRect()

    def setTheta(self, t):
        """Sets the angle of the vector"""
        self.theta = t
        self._updateRect()

    def dot(self, other):
        """Computes the dot product of this vector and another vector"""
        return self.x * other.x + self.y * other.y


