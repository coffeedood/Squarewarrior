import pygame
import sys
from pygame.locals import *

pygame.init()

surface = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GRAY = (150, 150, 150)
mainLoop = True

# Initialing Color
color = (255,0,0)
  
# Drawing Rectangle
pygame.draw.rect(surface, color, pygame.Rect(30, 30, 60, 60))
pygame.display.flip()

xlocation = 0
ylocation = 0

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mainLoop = False
    keys = pygame.key.get_pressed()

    xlocation += keys[pygame.K_RIGHT] - keys[pygame.K_LEFT]      
    ylocation += keys[pygame.K_DOWN] - keys[pygame.K_UP]  
     
    # Drawing Rectangle
    surface.fill(GRAY)
    pygame.draw.rect(surface, color, pygame.Rect(xlocation, ylocation, 60, 60))
    pygame.draw.rect(surface, color, pygame.Rect(600, 600, 60, 60))
    pygame.display.flip()
    clock.tick(120)