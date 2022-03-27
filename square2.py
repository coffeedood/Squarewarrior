import pygame
import sys
from pygame.locals import *
import random

pygame.init()
clock = pygame.time.Clock()

window = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
GRAY = (150, 150, 150)
mainLoop = True

# Initialing Color
color = (255,0,0)
  
rect1 = pygame.Rect(*window.get_rect().center, 0, 0).inflate(75, 75)
rect2 = pygame.Rect(0, 0, 75, 75)
rect3 = pygame.Rect(*window.get_rect().bottomleft, 0, 0).inflate(75, 75)

while mainLoop:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            mainLoop = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                mainLoop = False
    keys = pygame.key.get_pressed()

    rect2.move_ip (keys[pygame.K_d] - keys[pygame.K_a], keys[pygame.K_s] - keys[pygame.K_w])
    window.fill(GRAY)
    pygame.draw.rect(window, color, rect1)
    pygame.draw.rect(window, color, rect2)
    collide = rect1.colliderect(rect2)
    color = (255, 0, 0) if collide else (255, 255, 255)
    collide = rect3.colliderect(rect2)
    color = (255, 0, 0) if collide else (255, 255, 255)

    window.fill(0)
    pygame.draw.rect(window, color, rect1)
    pygame.draw.rect(window, (0, 255, 0), rect2, 6, 1)
    pygame.display.flip()
    clock.tick(120)