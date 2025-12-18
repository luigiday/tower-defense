from random import randint
import pygame
from time import sleep
import ui_tooling #utilitaire custom pour afficher des fenêtres PyQt6 (par exemple pour sélectionner une tour ou mettre en pause le jeu), correspond au fichier ui_tooling.py
path=[]
monstres=[]
argent = 350 #a modifier
tower_dict = { "tourlectrique": 200, "sapintueur": 300, "cristalexplosif": 500} # Ne pas modifier les noms, ca casse la selection de tours (les noms sont les mêmes que ceux dans le dossier assets)
                                                                                # C'est aussi dans le meme ordre que les boutons de ladite popup
placed_towers_names = {1: "tourlecrique"}
placed_towers_coords = [[15,15]]


def main():
    pygame.init()
    clock = pygame.time.Clock()
    frozen = False
    running = True
    clock.tick(8)
    ui_select_lock = False
    
    screen = pygame.display.set_mode((1920, 1080), pygame.SCALED) #On peux pas mettre full plein ecran parce que sinon ca bug qd on place 1 tour



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
         if len(monstres) == 0:
               monstres.append((0, 32))  
        
         x, y = monstres[0]     
         x += 1                    
         monstres.insert(0, (x, y)) 
         monstres.pop()

    def afficher_monstre():
      for x, y in monstres: 
        color(x, y, (200, 0, 0))

    def draw_towers(coords, dico):
        tournb = 1
        for i in coords:
            if dico[tournb] == "tourlecrique":
                couleur = (0, 4, 241)
            x = i[0]
            y = i[1]
            color(x, y, couleur)
            color((x+1), y, couleur)
            color((x), y+1, couleur)
            color((x+1), y+1, couleur)
            tournb += 1
    
    def add_tower(name, coords):
        placed_towers_coords.append(coords)
        #placed_towers_names


#bon déja g fais un chemin de base parce que
    initi()
    #monstre()
    #monstre()
    draw_towers(placed_towers_coords, placed_towers_names)
    
    pygame.display.update()

    

    running = True
    while running:
      initi()
      #monstre()
      #afficher_monstre()
      for event in pygame.event.get():
            if event.type == pygame.MOUSEBUTTONUP and not ui_select_lock:
                ui_select_lock = True
                pygame.event.set_blocked(None)
                try:
                    tour_selectionnee = ui_tooling.select_tower(argent, tower_dict) # Cette fonction prend le solde actuel du joueur et un dictionnaire des tours, et retounrne celle séléctionnée par le joueur
                except Exception as e:
                    ui_tooling.show_error_popup(e)
                finally:
                    pygame.event.set_allowed(None)
                    ui_select_lock = False
                    pygame.event.clear()

            if event.type == pygame.QUIT:
                if ui_tooling.ask_for_exit():
                    running = False
           
                
    pygame.display.flip()


    clock.tick(8)

    pygame.quit()
main()
    
# Ne mettez cette ligne que pr vos tests, pensez a comment out avant de commit
