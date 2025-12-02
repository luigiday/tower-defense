from random import randint
import pygame
from time import sleep


 
def initi():
          for x in range(32):
            for y in range(32):
              if(x+y)%2==0:color(x,y,(80,200,104))
              else:color(x,y,(3,150,40))


pygame.init()
screen = pygame.display.set_mode((1024, 1024))

def color(x, y, color):
    if x < 0 or x >= 32:
        raise IndexError(f"x out of range: must be >= 0 and < 32, got x = {x}")
    if y < 0 or y >= 32:
        raise IndexError(f"y out of range: must be >= 0 and < 32, got y = {y}")
    pygame.draw.rect(screen, color, [x * 16, y * 16, 16, 16])

initi()
    