from __future__ import division
from math import *

#Constants
CONST_G = 10
CONST_T = 1

def forceOfGravity(v1, v2, m1, m2):
    force = (CONST_G * m1 * m2) / ((v1-v2).mag)
    v = v2 - v1
    v.setMag(force)
    return v

def nextPos(pos, vel, acc):
    newvel = vel + acc * CONST_T
    return pos + (newvel + vel) * 0.5 * CONST_T

