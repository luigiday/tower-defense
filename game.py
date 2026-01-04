from random import randint
import pygame
from time import sleep
from time import time
import ui_tooling #utilitaire custom pour afficher des fenêtres PyQt6 (par exemple pour sélectionner une tour ou mettre en pause le jeu), correspond au fichier ui_tooling.py


def main(debug_show=False):
    pygame.init()
    pygame.mixer.init()
    vague=1
    chemins=[]
    path=[]
    monstres=[]
    monstres_pv=[]
    monstres_pv_max = []
    tick=0
    pv=100
    arbres=[]
    # Variables de stats
    debut = time()
    depenses = 0
    ennemis_tues = 0

    
    argent = 250 #a modifier
    tower_dict = { "tourlectrique": 250, "sapintueur": 500, "cristalexplosif": 1000} # Ne pas modifier les noms, ca casse la selection de tours (les noms sont les mêmes que ceux dans le dossier assets)
                                                                                    # C'est aussi dans le meme ordre que les boutons de ladite popup
    placed_towers_names = {1: "tourlectrique"}
    placed_towers_coords = [[15,15]]
    placed_towers_range = [[15-3,15+3,15-3,15+3]]  #x_min,x_max,y_min,y_max

    clock = pygame.time.Clock()
    pygame.mixer.music.load("Assets/musique.mp3")
    pygame.mixer.music.set_volume(0.05)  # entre 0 et 1
    pygame.mixer.music.play(-1)  
    dégats = pygame.mixer.Sound("Assets/dégats.mp3")   
    dégats.set_volume(0.1)
    loose=pygame.mixer.Sound("Assets/loose.mp3")   
    loose.set_volume(0.1)
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
            font = pygame.font.SysFont(None, 240)
            image = pygame.image.load("Assets/soldepierre.png").convert_alpha()
        except Exception as e:
            ui_tooling.show_error_popup(e)
            image = None

        if image:
        
            image = pygame.image.load("Assets/soldepierre.png").convert_alpha()
            image = pygame.transform.scale(image, (32,32))  # taille en pixels du chemin
            screen.blit(image, (x*16, y*16))
        else:
            pygame.draw.rect(screen, (255, 0, 255), [x * 16, y * 16, 16, 16])




    def initi():
     y1=randint(10,60)
     x1=randint(10,20)
     chemins.append((0, y1)) 
     
     for s in range(1,x1):
      chemins.append((s,y1))
      x=x1
     chemins.append((x, y1)) 
    
     while x<=95:
       
       add=randint(5,10)
       if y1<30:
        
        for m in range(add):
         y1+=1
         chemins.append((x,y1))
       else:
        
        for m in range(add):
         y1-=1
         chemins.append((x,y1))
       for n in range(randint(10,20)):
            x += 1
            chemins.append((x, y1))
     xfin=120-x
     if y1<32:
      yfin=32-y1
      for k in range(yfin):
       y1+=1
       chemins.append((x,y1))

     else:
      yfin=abs(32-y1)
      for k in range(yfin):
        y1-=1
        chemins.append((x,y1))
     for n in range(xfin):
            x += 1
            chemins.append((x,y1))

    def chateau():
        nonlocal pv
        for m in monstres[:]:
            if m["i"] >= len(chemins) - 2:
                monstre_pv = monstres_pv[monstres.index(m)]
                pv -= 2*monstre_pv
                #monstres_pv.remove(2*monstre_pv)
                dégats.play()
                #monstres.remove(m)

                if pv <= 0:
                    pygame.mixer.music.pause()
                    loose.play()
                 
                 
                 

    def afficher_debug_monstres():
        texte = f"monstres = {monstres}"
        surface = font.render(texte, True, (255, 0, 255))
        screen.blit(surface, (10, 10))
        texte = f"monstres pv = {monstres_pv} && montre_pv_max = {monstres_pv_max}"
        surface = font.render(texte, True, (255, 0, 255))
        screen.blit(surface, (10, 40))
    def afficher_lesticks():
        texte = f"tick: = {tick}"
        surface = font.render(texte, True, (100, 15, 255))
        screen.blit(surface, (10, 70))
    def afficher_pv():
        font = pygame.font.SysFont(None, 30)
        texte = f"Pv:{pv}"
        surface = font.render(texte, True, (255, 0, 0))
        screen.blit(surface, (1850, 415))
    def afficher_perte():
        global vague
        font = pygame.font.SysFont(None, 240)
        texte = f"PERDU!"
        surface = font.render(texte, True, (255, 0, 0))
        if pv<=0:
            screen.blit(surface, (700, 435))
            pygame.display.flip()
            if ui_tooling.gameover(placed_towers_names, depenses, ennemis_tues, time() - debut, vague):
                running = False
                pygame.quit()
                main()
            else:
                running = False
                pygame.quit()
  

    def vagues():
      global vague
      if tick <= 300:
        vague = 1
      elif tick <= 600:
        vague = 2
      elif tick <= 800:
        vague = 3
      elif tick <= 1100:
        vague = 4
      else:
        vague = 4 
      font = pygame.font.SysFont(None, 100)
      texte = f"VAGUE:{vague}"
      surface = font.render(texte, True, (0, 0, 200))
      screen.blit(surface, (830, 10))
    
        
    
    def monstre():
        global vague
        nonlocal ennemis_tues
        nonlocal argent
        if vague==1:
            if tick % 40 == 0:
                             
                monstres.append({"i": 0 })
                pv_monstre_init = randint(5,vague*10)
                monstres_pv.append(pv_monstre_init)
                monstres_pv_max.append(pv_monstre_init) 
        elif vague==2:
            if tick % 30 == 0:
                
                monstres.append({"i": 0 })
                pv_monstre_init = randint(5,vague*10)
                monstres_pv.append(pv_monstre_init)
                monstres_pv_max.append(pv_monstre_init)

        elif vague==3:
            if tick % 20 == 0:
                
                monstres.append({"i": 0 })
                pv_monstre_init = randint(5,vague*10)
                monstres_pv.append(pv_monstre_init)
                monstres_pv_max.append(pv_monstre_init)

        elif vague==4:
            if tick % 10 == 0:
                
                monstres.append({"i": 0 })
                pv_monstre_init = randint(5,vague*10)
                monstres_pv.append(pv_monstre_init)
                monstres_pv_max.append(pv_monstre_init)

        for m in monstres:
            m["i"] += 1
            # EDITED: Get monster coordinates from path for tower range checking (modifié par IA)
            if m["i"] < len(chemins):
                x, y = chemins[m["i"]]
                # EDITED: Check towers and apply damage (modifié par IA)
                for t in placed_towers_range:
                    x_min, x_max, y_min, y_max = t
                    if x_min <= x <= x_max and y_min <= y <= y_max: # Fin de la partie modifié par IA
                        monster_id = monstres.index(m)
                        tower_id = placed_towers_range.index(t)
                        tower_name = placed_towers_names.get(tower_id + 1)
                        if tower_name == "tourlectrique":
                            monstres_pv[monster_id] -= 1
                        elif tower_name == "sapintueur":
                            monstres_pv[monster_id] -= 2
                        elif tower_name == "cristalexplosif":
                            monstres_pv[monster_id] -= 3
        
        for m in monstres[:]:
            if m["i"] >= len(chemins) - 1:
                monster_id = monstres.index(m)
                del monstres_pv[monster_id]
                del monstres_pv_max[monster_id]
                monstres.remove(m)
            elif monstres_pv[monstres.index(m)] <= 0:
                try:
                    monster_id = monstres.index(m)
                    del monstres_pv[monster_id]
                    del monstres_pv_max[monster_id]
                    monstres.remove(m)
                    ennemis_tues += 1
                    argent += 100
                except Exception as e:
                    ui_tooling.show_error_popup(e)

       
        
      
    def afficher_portail():
        x,y=chemins[0]
        texture= pygame.image.load("Assets/portail.png").convert_alpha()
        screen.blit(texture, (x*16,(y*16-60)))

    

            
    def afficher_monstre():
        texture = pygame.image.load("Assets/zombie.png").convert_alpha()
        texture = pygame.transform.scale(texture, (50,50))
        # Debut de la partie modifié par IA
        for m in monstres:
            i = m["i"]
            if i < len(chemins):
                x, y = chemins[i]
                screen.blit(texture, (x*16, (y-1)*16))
                # Fin de la partie modifié par IA
                currentid = monstres.index(m)
                pv_monstre = monstres_pv[currentid]
                pv_max_monstre = monstres_pv_max[currentid]

            
            texture10 = pygame.image.load("Assets/full.png").convert_alpha()  
            texture10 = pygame.transform.scale(texture10, (50,50))

            texture9 = pygame.image.load("Assets/9.png").convert_alpha()
            texture9 = pygame.transform.scale(texture9, (50,50))

            texture8 = pygame.image.load("Assets/8.png").convert_alpha()
            texture8 = pygame.transform.scale(texture8, (50,50))

            texture7 = pygame.image.load("Assets/7.png").convert_alpha()
            texture7 = pygame.transform.scale(texture7, (50,50))

            texture6 = pygame.image.load("Assets/6.png").convert_alpha()
            texture6 = pygame.transform.scale(texture6, (50,50))

            texture5 = pygame.image.load("Assets/5.png").convert_alpha()
            texture5 = pygame.transform.scale(texture5, (50,50))

            texture4 = pygame.image.load("Assets/4.png").convert_alpha()
            texture4 = pygame.transform.scale(texture4, (50,50))

            texture3 = pygame.image.load("Assets/3.png").convert_alpha()
            texture3 = pygame.transform.scale(texture3, (50,50))

            texture2 = pygame.image.load("Assets/2.png").convert_alpha()
            texture2 = pygame.transform.scale(texture2, (50,50))

            texture1 = pygame.image.load("Assets/1..png").convert_alpha()
            texture1 = pygame.transform.scale(texture1, (50,50))

            
            if (pv_monstre/pv_max_monstre)*10 >= 10:
                screen.blit(texture10, (((x)*16-3), ((y-1)*16-6)))  
            elif (pv_monstre/pv_max_monstre)*10 >= 9:
                screen.blit(texture9, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 8:
                screen.blit(texture8, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 7:
                screen.blit(texture7,(((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 6:
                screen.blit(texture6, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 5:
                screen.blit(texture5, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 4:
                screen.blit(texture4, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 3:
                screen.blit(texture3, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 2:
                screen.blit(texture2, (((x)*16-3), ((y-1)*16-6))) 
            elif (pv_monstre/pv_max_monstre)*10 >= 1 or (pv_monstre/pv_max_monstre)*10 <= 1:
                screen.blit(texture1, (((x)*16-3), ((y-1)*16-6))) 


   
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
    

        
    def draw_fleurs():
       texture = pygame.image.load("Assets/fleurs.png").convert_alpha()
       texture = pygame.transform.scale(texture, (410,410)) 
       for x in range(1,1800,320):
        screen.blit(texture, (x, 1))
       for x in range(1,1800,320):
        screen.blit(texture, (x,820))
       for x in range(1,1800,320):
        screen.blit(texture, (x, 410))

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
        draw_fleurs()
        
        for x, y in chemins:
            draw_chemin(x, y)
     
        vagues()
        monstre()
        chateau()
        generearbre()
        afficher_monstre()
        draw_arbre()
        afficher_argent()
        if debug_show:
            afficher_lesticks()
            afficher_debug_monstres()
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
                                placed_towers_range.append([x-3, x+3, y-3, y+3])  # Ajouter la portée de la tour placée
                                try:
                                    new_id = max(placed_towers_names.keys()) + 1
                                except ValueError:
                                    new_id = 1
                                placed_towers_names[new_id] = tour_selectionnee
                                argent -= prix
                                print(f"DEBUG : Tour {tour_selectionnee} placée en {x}, {y} pour {prix} C. Solde restant : {argent} C.")
                                depenses += prix
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


        clock.tick(
           8
        )
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] :
            clock.tick(160)

        
        tick+=1
     
    

    pygame.quit()
#main()
    
# Ne mettez cette ligne que pr vos tests, pensez a comment out avant de commit
