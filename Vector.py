from math import *

class Vector:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y
        self.mag = 0
        self.theta = 0
        self._updatePol()

    def __add__(self, targ):
        return Vector(self.x + targ.x, self.y+targ.y)

    def __sub__(self, targ):
        return Vector(self.x-targ.x, self.y-targ.y)

    def __mul__(self, targ):
        return Vector(self.x*targ, self.y*targ)

    def __repr__(self):
        return "(" + str(self.x) + "," + str(self.y) + ")" 

    def __str__(self):
        return (self.__repr__() + 
            " Mag: " + str(self.mag) + " Theta: " + str(self.theta))

    def _updatePol(self):
        self.mag = sqrt(self.x**2 + self.y**2)
        self.theta = atan2(self.y, self.x)

    def _updateRect(self):
        self.x = self.mag * cos(self.theta)
        self.y = self.mag * sin(self.theta)

    def setPol(self, m, t):
        self.mag = m
        self.theta = t
        self._updateRect()

    def set_rect(self, x, y):
        self.x = x
        self.y = y
        self._updatePol()

    def rect(self): return (self.x, self.y)
    def pol(self): return (self.mag, self.theta)

    def setMag(self, m):
        self.mag = m
        self._updateRect()

    def setTheta(self, t):
        self.theta = t
        self._updateRect()

    def dot(self, other):
        return self.x * other.x + self.y * other.y


