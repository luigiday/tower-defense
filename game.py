from random import randint
import pygame
from time import sleep
import ui_tooling #utilitaire custom pour afficher des fenêtres PyQt6 (par exemple pour sélectionner une tour ou mettre en pause le jeu), correspond au fichier ui_tooling.py


def main():
    pygame.init()
    path=[]
    monstres=[]
    tick=0
    pv=100
    arbres=[]
    argent = 1350 #a modifier
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
        if y < 0 or y >= 70:
            raise IndexError(f"y out of range: must be >= 0 and < 70, got y = {y}")
        pygame.draw.rect(screen, color, [x * 16, y * 16, 16, 16])

    def draw_chemin(x, y):
        image = None
        try:
            image = pygame.image.load("Assets/soldepierre.png").convert_alpha()
        except Exception as e:
            ui_tooling.show_error_popup(e)
            image = None

        if image:
            screen.blit(image, (x * 16, y * 16))
        else:
            pygame.draw.rect(screen, (255, 0, 255), [x * 16, y * 16, 16, 16])



    def initi():
        for x in range(120):
            for y in range(68):
                if (x + y) % 2 == 0:
                    color(x, y, (10,68,23))
                else:
                    color(x, y, (10,68,23))

        for i in range(120):  
          a = (i, 31)
          b = (i, 32)
          c = (i, 33)
          path.append(a)
          path.append(b)
          path.append(c)
          draw_chemin(*a)
          draw_chemin(*b)
          draw_chemin(*c)
    def chateau():
          nonlocal pv
          for m in monstres[:]: 
             x, y = m
             if x>=119:
              pv-=10
             #if pv==0:
                 
                 

    def afficher_debug_monstres():
        texte = f"monstres = {monstres}"
        surface = font.render(texte, True, (255, 0, 255))
        screen.blit(surface, (10, 10))
    def afficher_lesticks():
        texte = f"tick: = {tick}"
        surface = font.render(texte, True, (100, 15, 255))
        screen.blit(surface, (10, 40))
    def afficher_pv():
        font = pygame.font.SysFont(None, 30)
        texte = f"Pv:{pv}"
        surface = font.render(texte, True, (255, 0, 0))
        screen.blit(surface, (1850, 415))
    def afficher_perte():
        font = pygame.font.SysFont(None, 240)
        texte = f"PERDU!"
        surface = font.render(texte, True, (255, 0, 0))
        if pv<=0:
            screen.blit(surface, (700, 435))
  


    
        
    
    def monstre():
       
      if tick % 40 == 0:
        monstres.append([0, 32])



      for m in monstres:
       m[0] += 1
 
      for m in monstres[:]:
        if m[0] >= 120:
         monstres.remove(m)

       
        
      
    def afficher_portail():
        texture= pygame.image.load("Assets/portail.png").convert_alpha()
        screen.blit(texture, (0,450))

    def afficher_monstre():
        texture= pygame.image.load("Assets/zombie.png").convert_alpha()
        texture = pygame.transform.scale(texture, (50,50)) 
        for m in monstres:
           x,y=m
           y=y-1
           screen.blit(texture, (x*16,y*16))
       
   
    def generearbre():
     
        texture = pygame.image.load("Assets/arbre.png").convert_alpha()
        while len(arbres)<35:
           a = randint(0,110)
           b = randint(5,60)
           while b == 20 or b == 21 or b == 22 or b == 23 or b == 24 or b == 25 or b == 26 or b == 27 or b == 28 or b == 29 or b == 30 or b == 31 or b == 32 or b == 33 or b == 34:
                    a=randint(10,110)
                    b=randint(5,60)
           arbres.append((a,b))
        
    def draw_arbre():
       texture = pygame.image.load("Assets/arbre.png").convert_alpha()
       for a,b in arbres:
        screen.blit(texture, (a*16, b*16))
        

        
        


    def draw_chateau():
        texture = pygame.image.load("Assets/chateau.png").convert_alpha()
        texture = pygame.transform.scale(texture, (130,130)) 
        texture2= pygame.image.load("Assets/chateau cassé.png").convert_alpha()
        texture2 = pygame.transform.scale(texture2, (130,130)) 
        texture3= pygame.image.load("Assets/chateau cassé2.png").convert_alpha()
        texture3 = pygame.transform.scale(texture3, (130,130)) 
        texture4= pygame.image.load("Assets/chateau cassé3.png").convert_alpha()
        texture4 = pygame.transform.scale(texture4, (130,130)) 
        texture5= pygame.image.load("Assets/chateau cassé4.png").convert_alpha()
        texture5 = pygame.transform.scale(texture5, (130,130)) 
        texture6= pygame.image.load("Assets/FIN!.png").convert_alpha()
        texture6 = pygame.transform.scale(texture6, (130,130)) 
        if pv<=0:
            screen.blit(texture6, (1834, 440))
        elif pv<=20:
            screen.blit(texture5, (1834, 440))
        elif pv<=40:
            screen.blit(texture4, (1834, 440))
        elif pv<=60:
            screen.blit(texture3, (1834, 440))
        elif pv<=80:
            screen.blit(texture2, (1834, 440))

        else:
 
          screen.blit(texture, (1834, 440))

        
          


    
    
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
       image = pygame.image.load("Assets/Coin.png").convert_alpha()


       image = pygame.transform.scale(image, (60,60)) 


       screen.blit(image, (1855, 5))
       font = pygame.font.SysFont(None, 50)
       texte = f"Argent: {argent} "
       surface = font.render(texte, True, (255, 255, 0))  
      
       screen_width = screen.get_width()
       surface_width = surface.get_width()
       screen.blit(surface, (screen_width - surface_width - 60, 20))
    
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
        chateau()
        generearbre()
        afficher_monstre()
        afficher_debug_monstres()
        draw_arbre()
        afficher_argent()
        afficher_lesticks()
        afficher_perte()
        afficher_pv()
        afficher_portail()
        draw_chateau()
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


        clock.tick(160)
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] :
            clock.tick(160)

        
        tick+=1
     
    

    pygame.quit()
main()
    
# Ne mettez cette ligne que pr vos tests, pensez a comment out avant de commit
