from __future__ import division
from math import *

#Constants
CONST_G = 10
CONST_T = 1

def forceOfGravity(p1, p2, m1, m2):
    """Compues the force of gravity between the two positions
       with their respective masses"""
    force = (CONST_G * m1 * m2) / ((p1-p2).mag)**2
    v = p2 - p1
    v.setMag(force)
    return v

def nextPos(pos, vel, acc):
    """Computes the nect position based on the velocity and acceleration
       using improved euler method"""
    newvel = vel + acc * CONST_T
    return pos + (newvel + vel) * 0.5 * CONST_T

