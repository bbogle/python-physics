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
        pygame.draw.circle(surf, color,
                           (int(self.px + self.x), int(self.py + self.y)), 2)


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
    def __init__(self, pos, rad=10, vel=None, acc=None, coeff_restitution=1, coeff_friction=1):
        Piece.__init__(self, pos, 1, vel, acc)
        self.rad = rad
        self.color=pygame.Color(255, 0, 0)
        self.coeff_restitution = coeff_restitution
        self.coeff_friction = coeff_friction

    def _checkWallOverlap(self, walls):
        for b in walls:
            n = b.getNorm()             #Normal to the line away coeff_frictionom bouncing side
            p = b.getMid()-self.pos     #vector coeff_frictionom ball to center of line
            dist = abs(p.dot(n))        #distance coeff_frictionom center of ball to the line
            l = p - n*p.dot(n)          #perp = p - proj on normal
            if dist < self.rad and l.mag < ((b.p2-b.p1).mag/2):
                if self.vel.mag != 0:
                    t = abs((self.rad-dist)/n.dot(self.vel))
                    self.pos = self.pos - self.vel*t
                    proj  = n * n.dot(self.vel)
                    perp = self.vel - proj
                    self.vel = perp*self.coeff_friction - proj*self.coeff_restitution
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
                    self.vel = perp*self.coeff_friction - proj*self.coeff_restitution
                    self.pos = self.pos + self.vel * (1-t)

    def collide(self, other):
        dp = self.pos - other.pos
        dvel = other.vel - self.vel
        r = self.rad + other.rad
        (dx, dy) = dp.rect()
        (du, dv) = dvel.rect()
        (a, b, c) = (du**2+dv**2, 2*(dx*du+dy*dv), dx**2+dy**2-r**2)
        descoeff_restitutioniminant = b**2 - 4*a*c
        if (descoeff_restitutioniminant >= 0 and a != 0):
            t = (-b+sqrt(descoeff_restitutioniminant))/(2*a)
            t2 = (-b-sqrt(descoeff_restitutioniminant))/(2*a)
            if (dp.mag < r):
                self.pos = self.pos - self.vel*t
                other.pos = other.pos - other.vel*t
                return True
            elif (t >= 0 and t <= 1):
                if t2 > 0: goodt = t2
                else: goodt = t
                self.pos = self.pos + self.vel*t
                other.pos = other.pos + other.vel*t
                return True

    def bounce_off(self, other):
        dp = other.pos - self.pos
        dp.setMag(1)
        u1 = self.vel.dot(dp)
        u2 = other.vel.dot(dp)
        m1 = self.mass
        m2 = other.mass
        coeff_restitution = (self.coeff_restitution + other.coeff_restitution)/2

        v1 = (m1*u1+m2*u2 + coeff_restitution*m2*(u2-u1))/(m1+m2)
        v2 = (m1*u1+m2*u2 + coeff_restitution*m1*(u1-u2))/(m1+m2)

        self.vel = self.vel - dp*u1 + dp*v1
        other.vel = other.vel - dp*u2 + dp*v2

    def boundery_check(self, walls):
        self._checkWallOverlap(walls)
        self._checkFutureWall(walls)

    def draw(self, surf):
        pygame.draw.circle(surf, self.color, (int(self.pos.x), int(self.pos.y)), int(self.rad))
        #vd = VectorDraw(self.vel, self.pos.x, self.pos.y)
        #vd.draw(surf)

class Wall:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        vec = p2-p1
        vec.set_rect(vec.x, -vec.y)
        self.angle = vec.theta

    def getNorm(self):
        v = self.p2-self.p1
        v.setMag(1)
        v.set_rect(-v.y, v.x)
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
