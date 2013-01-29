from __future__ import division
import pygame
import sys
from GalaxyParts import *
from pygame.locals import *
from random import random
from Vector import *
import Physics as Phy

WIDTH = 800
HEIGHT = 600

pygame.init()

fpsClock = pygame.time.Clock()

white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

win = pygame.display.set_mode((WIDTH, HEIGHT))

gameobjects = []
pad = 5
ov = 0
walls = [Wall(Vector(pad-ov, HEIGHT-pad), Vector(WIDTH-pad+ov, HEIGHT-pad)),
         Wall(Vector(WIDTH-pad, HEIGHT-pad+ov), Vector(WIDTH-pad, pad-ov)),
         Wall(Vector(WIDTH-pad+ov, pad), Vector(pad-ov, pad)),
         Wall(Vector(pad, pad-ov), Vector(pad, HEIGHT-pad+ov))]
#         Wall(Vector(pad-ov, pad+200), Vector(pad+400, HEIGHT-pad+ov))
#         Wall(Vector(200, 200), Vector(WIDTH-pad, 200))]

#for i in range(1,7):
#    for j in range(1,5):
#        r = random()*10
#        tmp = Ball(Vector(20+i*70, 20+j*70), 
#                   r/2, Vector(0, 0), Vector(0, 0), 0.9, 1)
#        tmp.mass=r
#        gameobjects.append(tmp)


while True:
    win.fill(white)

    for i in range(0, len(gameobjects)):
        obj = gameobjects[i]
        (x,y) = obj.pos.coords()

        for j in range(i+1, len(gameobjects)):
            other = gameobjects[j]
            if (obj.collide(other)):
                obj.bounceOff(other)
            gforce1 = Phy.forceOfGravity(obj.pos, other.pos, obj.mass, other.mass)
            tpos1 = Phy.nextPos(obj.pos, obj.vel, gforce1)
            tpos2 = Phy.nextPos(other.pos, other.vel, gforce1*(-1))
            gforce2 = Phy.forceOfGravity(tpos1, tpos2, obj.mass, other.mass)
            gforce = (gforce1+gforce2)*0.5
            obj.acc += gforce*(1/obj.mass)
            other.acc += gforce*(-1/other.mass)

        obj.move()
        obj.bounderyCheck(walls)
        obj.draw(win)
        obj.acc = Vector(0, 0)

    for obj in walls:
        obj.draw(win)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            (x,y) = event.pos
            tm = random()*2 + 1
            tmp = Ball(Vector(x,y), tm*3)
            (tmp.x, tmp.y) = (0, 0)#random()*20-10, random()*20-10)
            #tmp.acc.setRect(0, 1)
            tmp.cr=0.9
            tmp.fr=1
            tmp.mass = tm
            gameobjects.append(tmp)

    pygame.display.update()
    fpsClock.tick(45)

