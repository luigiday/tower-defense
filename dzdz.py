from random import randint
import pygame
from time import sleep

def main():
    pygame.init()
    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def color(x, y, color):
        if x < 0 or x >= 120:
            raise IndexError(f"x out of range: must be >= 0 and < 32, got x = {x}")
        if y < 0 or y >= 64:
            raise IndexError(f"y out of range: must be >= 0 and < 32, got y = {y}")
        pygame.draw.rect(screen, color, [x * 16, y * 16, 16, 16])

    def initi():
        for x in range(120):
            for y in range(64):
                if (x + y) % 2 == 0:
                    color(x, y, (80, 200, 104))
                else:
                    color(x, y, (3, 150, 40))
        for i in range(120):
            color(31,i(128,128,128))
            color(32,i(128,128,128))
            color(33,i(128,128,128))

    initi()
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

    pygame.quit()