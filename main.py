from __future__ import division
import pygame
import sys
from GalaxyParts import *
from pygame.locals import *
from random import random
from Vector import *
import Physics as Phy

WIDTH = 640
HEIGHT = 480

pygame.init()

fpsClock = pygame.time.Clock()

white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)

win = pygame.display.set_mode((WIDTH, HEIGHT))

gameobjects = []
pad = 20
walls = [Wall(Vector(pad+400, HEIGHT-pad), Vector(WIDTH-pad, HEIGHT-pad)),
         Wall(Vector(WIDTH-pad, HEIGHT-pad), Vector(WIDTH-pad, pad)),
         Wall(Vector(WIDTH-pad, pad), Vector(pad, pad)),
         Wall(Vector(pad, pad), Vector(pad, pad+200)),
         Wall(Vector(pad, pad+200), Vector(pad+400, HEIGHT-pad)),
         Wall(Vector(200, 200), Vector(WIDTH-pad, 200))]

while True:
    win.fill(white)

    for i in range(0, len(gameobjects)):
        obj = gameobjects[i]
        (x,y) = obj.pos.rect()

        if (x<0 or y<0 or x>WIDTH or y>HEIGHT):
            gameobjects.remove(obj)
            continue

        for j in range(i+1, len(gameobjects)):
            other = gameobjects[j]
            obj.collide(other)

        obj.move()
        obj.bounderyCheck(walls)
        obj.draw(win)

    for obj in walls:
        obj.draw(win)

    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN:
            print("foo")
            (x,y) = event.pos
            tmp = Ball(Vector(x,y), 7)
            tmp.vel.setRect(-3, -10)
            #tmp.acc.setRect(0, 1)
            tmp.cr=0.98
            tmp.fr=1
            gameobjects.append(tmp)

    pygame.display.update()
    fpsClock.tick(30)

