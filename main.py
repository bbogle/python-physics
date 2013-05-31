########################################
# main.py
#
# Main program for physics simulation.
# Author: Syed Zahir Bokhari
########################################

from __future__ import division
import pygame
import sys
from GalaxyParts import *
from pygame.locals import *
from random import random
from Vector import *
import Physics as Phy

# Gravity in simulation
GRAVITY = 1

# Width and height of viewing area
WIDTH = 800
HEIGHT = 600


# pygame setup
pygame.init()
fps_clock = pygame.time.Clock()
white = pygame.Color(255,255,255)
black = pygame.Color(0,0,0)
win = pygame.display.set_mode((WIDTH, HEIGHT))

# List of objects interacting in the simulation
gameobjects = []

# Place walls along edge of scren and slope to test angled deflection
pad = 5             # Distance from window edge to wall
ov = 20             # Overlap of walls
walls = [Wall(Vector(pad-ov, HEIGHT-pad), Vector(WIDTH-pad+ov, HEIGHT-pad)),
         Wall(Vector(WIDTH-pad, HEIGHT-pad+ov), Vector(WIDTH-pad, pad-ov)),
         Wall(Vector(WIDTH-pad+ov, pad), Vector(pad-ov, pad)),
         Wall(Vector(pad, pad-ov), Vector(pad, HEIGHT-pad+ov)),
         Wall(Vector(pad-ov, pad+200), Vector(pad+400, HEIGHT-pad+ov)),
         Wall(Vector(200, 200), Vector(WIDTH-pad, 200))]

# Main game loop
while True:
    win.fill(white)                     # Paint screen white

    # Iterate over every game object (for now they are all balls)
    for i in range(0, len(gameobjects)):
        obj = gameobjects[i]

        # Iterate over every other object
        for j in range(i+1, len(gameobjects)):
            other = gameobjects[j]

            # Check for collision between two objects (and update position and
            # velocity.
            if (obj.collide(other)):
                obj.bounce_off(other)

        obj.acc.set_rect(0,GRAVITY) # Set gravity
        obj.move()                  # Update position and velocity

        obj.boundery_check(walls)   # Check for collision with wall and react

        obj.draw(win)               # Draw ball
        obj.acc = Vector(0, 0)      # Reset acceleration

    # Draw walls
    for obj in walls:
        obj.draw(win)

    # Handle pygame events (quit and mouse click)
    for event in pygame.event.get():
        if event.type == QUIT:              # If the quit signal is sent
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEBUTTONDOWN: # If the mouse button is clicked
            # Produce ball at mouse click position
            (x,y) = event.pos
            mass = random()*5
            tmp = Ball(Vector(x,y), mass*2)

            # Give ball random velocity set friction coefficents, and gravity
            tmp.vel.set_rect(random()*20-10, random()*20-10)
            tmp.acc.set_rect(0, 1)
            tmp.coeff_restitution=0.9
            tmp.coeff_friction=1
            tmp.mass = mass

            # Add ball to objects list
            gameobjects.append(tmp)

    # Step the game foreward
    pygame.display.update()
    fps_clock.tick(45)
