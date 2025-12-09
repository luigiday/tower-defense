from random import randint
import pygame
from time import sleep
import ui_tooling #utilitaire custom pour afficher des fenêtres PyQt6 (par exemple pour sélectionner une tour ou mettre en pause le jeu), correspond au fichier ui_tooling.py
path=[]
monstres=[]
argent = 0 #a modifier

def main():
    pygame.init()
    clock = pygame.time.Clock()
    frozen = False
    running = True
    clock.tick(8)
    

    screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)

    def color(x, y, color):
        if x < 0 or x >= 120:
            raise IndexError(f"x out of range: must be >= 0 and < 120, got x = {x}")
        if y < 0 or y >= 67:
            raise IndexError(f"y out of range: must be >= 0 and < 70, got y = {y}")
        pygame.draw.rect(screen, color, [x * 16, y * 16, 16, 16])

    def initi():
        for x in range(120):
            for y in range(66):
                if (x + y) % 2 == 0:
                    color(x, y, (80, 200, 104))
                else:
                    color(x, y, (3, 150, 40))

        for i in range(120):  
          a = (i, 31)
          b = (i, 32)
          c = (i, 33)
          path.append(a)
          path.append(b)
          path.append(c)
          color(*a, (128, 128, 128))
          color(*b, (128, 128, 128))
          color(*c, (128, 128, 128))
    def monstre():
        for i in range(1,len(path),3):
           for y in range(120):
            a=(i,32)
            monstres.append(a)
            color(*monstres[y], (200,0,0))




#bon déja g fais un chemin de base parce que blc çççççççççççççç
    initi()
    monstre()
    
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
           
                
            pygame.display.flip()


            clock.tick(8)

    pygame.quit()
main()
    
# Ne mettez cette ligne que pr vos tests, pensez a comment out avant de commit