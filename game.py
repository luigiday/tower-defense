from random import randint
import pygame
from time import sleep
import ui_tooling #utilitaire custom pour afficher des fenêtres PyQt6 (par exemple pour sélectionner une tour ou mettre en pause le jeu), correspond au fichier ui_tooling.py


def main():
    pygame.init()
    path=[]
    monstres=[]
    argent = 350 #a modifier
    tower_dict = { "tourlectrique": 200, "sapintueur": 300, "cristalexplosif": 500} # Ne pas modifier les noms, ca casse la selection de tours (les noms sont les mêmes que ceux dans le dossier assets)
                                                                                    # C'est aussi dans le meme ordre que les boutons de ladite popup
    placed_towers_names = {1: "tourlectrique"}
    placed_towers_coords = [[15,15]]

    clock = pygame.time.Clock()
    frozen = False
    running = True
    font = pygame.font.SysFont(None, 24)
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

    def afficher_debug_monstres():
        texte = f"monstres = {monstres}"
        surface = font.render(texte, True, (255, 255, 255))
        screen.blit(surface, (10, 10))

    def monstre():
        if len(monstres) == 0:
            monstres.append((0, 32))
            return
        x, y = monstres[0]
        if x < 119:
          monstres[0] = (x + 1, y)
        else:
            monstres.pop(0)
      

    def afficher_monstre():
        for x, y in monstres: 
            color(x, y, (200, 0, 0))

    def draw_towers(coords, dico):
        for idx, i in enumerate(coords, start=1):
            name = dico.get(idx)
            image = None
            try:
                if name == "tourlectrique":
                    image = pygame.image.load("Assets/tourlectrique.png").convert_alpha()
                elif name == "sapintueur":
                    image = pygame.image.load("Assets/sapintueur.png").convert_alpha()
                elif name == "cristalexplosif":
                    image = pygame.image.load("Assets/cristalexplosif.png").convert_alpha()
            except Exception as e:
                ui_tooling.show_error_popup(e)
                image = None

            x = i[0]
            y = i[1]
            if image:
                screen.blit(image, (x * 16, y * 16))
            else:
                # Fallback: draw a visible placeholder if image missing or unknown
                pygame.draw.rect(screen, (255, 0, 255), [x * 16, y * 16, 16, 16])
    def afficher_argent():
       texte = f"Argent: {argent} C"
       surface = font.render(texte, True, (255, 255, 0))  #
      
       screen_width = screen.get_width()
       surface_width = surface.get_width()
       screen.blit(surface, (screen_width - surface_width - 10, 10))
    
    def add_tower(name, coords):
        placed_towers_coords.append(coords)
        #placed_towers_names


#bon déja g fais un chemin de base parce que
    initi()
    
    
    pygame.display.update()

    

    running = True
    while running:
        initi()
        monstre()
        afficher_monstre()
        afficher_debug_monstres()
        afficher_argent()
        draw_towers(placed_towers_coords, placed_towers_names)
        for event in pygame.event.get():
                if event.type == pygame.MOUSEBUTTONUP and not ui_select_lock:
                    ui_select_lock = True
                    pygame.event.set_blocked(None)
                    coords = event.pos
                    x = coords[0] // 16
                    y = coords[1] // 16
                    print(f"DEBUG : Clic détecté en {x}, {y}")
                    try:
                        tour_selectionnee = ui_tooling.select_tower(argent, tower_dict) # Cette fonction prend le solde actuel du joueur et un dictionnaire des tours, et retounrne celle séléctionnée par le joueur
                        if tour_selectionnee is not None:
                            prix = tower_dict[tour_selectionnee]
                            if argent >= prix:
                                placed_towers_coords.append([x, y])
                                # add new mapping instead of overwriting the dict
                                try:
                                    new_id = max(placed_towers_names.keys()) + 1
                                except ValueError:
                                    new_id = 1
                                placed_towers_names[new_id] = tour_selectionnee
                                argent -= prix
                                print(f"DEBUG : Tour {tour_selectionnee} placée en {x}, {y} pour {prix} C. Solde restant : {argent} C.")
                            else:
                                print(f"DEBUG : Fonds insuffisants pour placer la tour {tour_selectionnee} (coût : {prix} C, solde : {argent} C).")
                        else:
                            print("DEBUG : Aucune tour sélectionnée.")
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
#main()
    
# Ne mettez cette ligne que pr vos tests, pensez a comment out avant de commit
