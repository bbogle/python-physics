from __future__ import division
from math import *
from Vector import *
import pygame
import Physics as Phy

class VectorDraw(Vector):
    """Simple drawable arrow Vector class"""

    def __init__(self, vec, x=0, y=0):
        Vector.__init__(self, vec.x, vec.y)
        self.pos = Vector(x, y)

    def draw(self, surf, color=pygame.Color(0,0,0)):
        pygame.draw.line(surf, color, 
                         (self.pos.x, self.pos.y), 
                         (self.pos.x + self.x, self.pos.y + self.y))
        pygame.draw.circle(surf, color, (self + self.pos).int_coords(), 2)

class Piece:
    """This is an abstract class that is meant to hold all the
    general properties of all physics objects."""

    def __init__(self, pos=None, mass=10, vel=None, acc=None):
        self.pos = pos or Vector()
        self.vel = vel or Vector()
        self.acc = acc or Vector()
        self.mass = mass
        
    def move(self, t=Phy.CONST_T):
        """Updates the position and velocity of the Piece"""
        oldvel = self.vel
        self.vel = self.vel + self.acc * t
        self.pos = self.pos + (self.vel + oldvel) * 0.5 * t

    def draw(self, win):
        """Draws the Piece on the supplied surface.
           To be implemented by the child class"""
        raise NoImplementationError("Draw function not implemented")
         

class Ball(Piece):
    """A BallPiece class that can bounce of other BallPieces and WallsPieces"""

    def __init__(self, pos, rad=10, vel=None, acc=None, cr=1, fr=1):
        Piece.__init__(self, pos, 1, vel, acc)
        self.rad = rad
        self.color=pygame.Color(255, 0, 0)
        self.cr = cr
        self.fr = fr

    def _checkWallOverlap(self, walls):
        """Checks whether this ball is overlapping one of the walls
           in the supplied list"""
        for b in walls:
            n = b.getNorm()             #Normal to the line away from bouncing side
            p = b.getMid()-self.pos     #vector from ball to center of line
            dist = abs(p.dot(n))        #distance from center of ball to the line
            l = p - n*p.dot(n)          #perp = p - proj on normal
            if (dist < self.rad and 
                l.mag < ((b.p2-b.p1).mag/2) and
                self.vel.mag != 0):
               t = abs((self.rad-dist)/n.dot(self.vel))
               self.pos = self.pos - self.vel*t
               proj  = n * n.dot(self.vel)
               perp = self.vel - proj
               self.vel = perp*self.fr - proj*self.cr
               self.pos = self.pos + self.vel * (1-t)

    def _checkFutureWall(self, walls):
        """Checks whether this ball will cross a wall in the supplied list
           in the nect time step"""
        for b in walls:
            (x1, y1) = self.pos.coords()
            (u1, v1) = self.vel.coords()
            (x2, y2) = b.getMid().coords()
            (u2, v2) = (b.p1 - b.getMid()).coords()
            det = u2*v1-u1*v2
            if det != 0:
                (dx, dy) = (x2-x1, y2-y1)
                t = (u2*dy-v2*dx)/det
                s = (u1*dy-v1*dx)/det
                if t <= 1 and t >= 0 and abs(s) <= 1:
                    t = t - self.rad/self.vel.dot(b.getNorm())
                    print(t)
                    n = b.getNorm()
                    self.pos = self.pos + self.vel*t
                    proj  = n * n.dot(self.vel)
                    perp = self.vel - proj
                    self.vel = perp*self.fr - proj*self.cr
                    self.pos = self.pos + self.vel * (1-t)

    def collide(self, other):
        """Checks if this ball is colliding or will collide with the other ball
           supplied"""
        dp = self.pos - other.pos
        dvel = other.vel - self.vel
        r = self.rad + other.rad
        (dx, dy) = dp.coords()
        (du, dv) = dvel.coords()
        (a, b, c) = (du**2+dv**2, 2*(dx*du+dy*dv), dx**2+dy**2-r**2)
        descriminant = b**2 - 4*a*c
        if (descriminant >= 0 and a != 0):
            t = (-b+sqrt(descriminant))/(2*a)
            t2 = (-b-sqrt(descriminant))/(2*a)
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

    def bounceOff(self, other):
        """Adjust the speed of this ball and the other as if they were colliding"""
        dp = other.pos - self.pos
        dp.mag = 1
        u1 = self.vel.dot(dp)
        u2 = other.vel.dot(dp)
        m1 = self.mass
        m2 = other.mass
        cr = (self.cr + other.cr)/2

        v1 = (m1*u1+m2*u2 + cr*m2*(u2-u1))/(m1+m2)
        v2 = (m1*u1+m2*u2 + cr*m1*(u1-u2))/(m1+m2)

        self.vel = self.vel - dp*u1 + dp*v1
        other.vel = other.vel - dp*u2 + dp*v2

    def bounderyCheck(self, walls):
        """Function used to check if this ball makes a collision with a wall
        in the supplied list"""
        self._checkWallOverlap(walls)
        self._checkFutureWall(walls)

    def draw(self, surf):
        """Draws the Ball"""
        pygame.draw.circle(surf, self.color, 
            (int(self.pos.x), int(self.pos.y)), int(self.rad))

class Wall:
    """General wall object used to set up boundries and platforms
       in the simulation world"""

    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2
        vec = p2-p1
        (vec.x, vec.y) = (vec.x, -vec.y)
        self.angle = vec.theta

    def getNorm(self):
        """Return a vector normal to the line"""
        v = self.p2-self.p1
        v.mag = 1
        (v.x, v.y) = (-v.y, v.x)
        return v

    def getMid(self):
        """Returns a vector representing the midpoint of the line"""
        return (self.p1+self.p2)*0.5
        

    def draw(self, surf, color=pygame.Color(0, 0, 0)):
        """Draws the line"""
        pygame.draw.line(surf, color, self.p1.coords(), self.p2.coords())
        mid = (self.p1 + self.p2) * 0.5
        ac = 10
        area = pygame.Rect(mid.x-ac, mid.y-ac, 2*ac, 2*ac)
        pygame.draw.arc(surf, color, area, self.angle-pi, self.angle, 1)
        vd = VectorDraw(self.getNorm()*20, mid.x, mid.y)
        vd.draw(surf)
