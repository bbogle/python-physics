#hoo
from __future__ import division
from math import *
from Vector import *
import pygame
import Physics as Phy

class VectorDraw(Vector):
    def __init__(self, vec, x=0, y=0):
        Vector.__init__(self, vec.x, vec.y)
        self.px = x
        self.py = y

    def draw(self, surf, color=pygame.Color(0,0,0)):
        pygame.draw.line(surf, color, (self.px,self.py), 
                         (self.px + self.x, self.py + self.y))
        pygame.draw.circle(surf, color, (self.px + self.x, self.py + self.y), 2)


class Piece:
    def __init__(self, pos=None, mass=10, vel=None, acc=None):
        self.pos = pos or Vector()
        self.vel = vel or Vector()
        self.acc = acc or Vector()
        self.mass = mass
        
    def move(self, t=Phy.CONST_T):
        oldvel = self.vel
        self.vel = self.vel + self.acc * t
        self.pos = self.pos + (self.vel + oldvel) * 0.5 * t

    def draw(self, win):
        raise NoImplementationError("Draw function not implemented")
         

class Ball(Piece):
    def __init__(self, pos, rad=10, vel=None, acc=None, cr=1, fr=1):
        Piece.__init__(self, pos, 1, vel, acc)
        self.rad = rad
        self.color=pygame.Color(255, 0, 0)
        self.cr = cr
        self.fr = fr

    def _checkWallOverlap(self, walls):
        for b in walls:
            n = b.getNorm()             #Normal to the line away from bouncing side
            p = b.getMid()-self.pos     #vector from ball to center of line
            dist = abs(p.dot(n))        #distance from center of ball to the line
            l = p - n*p.dot(n)          #perp = p - proj on normal
            if dist < self.rad and l.mag < ((b.p2-b.p1).mag/2):
                if self.vel.mag != 0:
                    t = abs((self.rad-dist)/n.dot(self.vel))
                    self.pos = self.pos - self.vel*t
                    proj  = n * n.dot(self.vel)
                    perp = self.vel - proj
                    self.vel = perp*self.fr - proj*self.cr
                    self.pos = self.pos + self.vel * (1-t)

    def _checkFutureWall(self, walls):
        for b in walls:
            (x1, y1) = self.pos.rect()
            (u1, v1) = self.vel.rect()
            (x2, y2) = b.getMid().rect()
            (u2, v2) = (b.p1 - b.getMid()).rect()
            det = u2*v1-u1*v2
            if det != 0:
                (dx, dy) = (x2-x1, y2-y1)
                t = (u2*dy-v2*dx)/det
                s = (u1*dy-v1*dx)/det
                if t <= 1 and t >= 0 and abs(s) <= 1:
                    t = t - self.rad/self.vel.dot(b.getNorm())
                    n = b.getNorm()
                    self.pos = self.pos + self.vel*t
                    proj  = n * n.dot(self.vel)
                    perp = self.vel - proj
                    self.vel = perp*self.fr - proj*self.cr
                    self.pos = self.pos + self.vel * (1-t)

    def _overlapOtherBall(self, other):
        pass

    def objectCollision(self, other):
        self._overlap(other)

    def bounderyCheck(self, walls):
        self._checkWallOverlap(walls)
        self._checkFutureWall(walls)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, self.pos.rect(), self.rad)
        vd = VectorDraw(self.vel, self.pos.x, self.pos.y)
        vd.draw(surf)

class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        vec = p2-p1
        vec.setRect(vec.x, -vec.y)
        self.angle = vec.theta
        print(self.angle)

    def getNorm(self):
        v = self.p2-self.p1
        v.setMag(1)
        v.setRect(-v.y, v.x)
        return v

    def getMid(self):
        return (self.p1+self.p2)*0.5
        

    def draw(self, surf, color=pygame.Color(0, 0, 0)):
        pygame.draw.line(surf, color, self.p1.rect(), self.p2.rect())
        mid = (self.p1 + self.p2) * 0.5
        ac = 10
        area = pygame.Rect(mid.x-ac, mid.y-ac, 2*ac, 2*ac)
        pygame.draw.arc(surf, color, area, self.angle-pi, self.angle, 1)
        vd = VectorDraw(self.getNorm()*20, mid.x, mid.y)
        vd.draw(surf)
