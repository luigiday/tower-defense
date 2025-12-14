#le code de l'ui pr le launcher et tt ce qui est textuel...
try:
    import pygame
    import game
    #from tkinter import messagebox
    #import tkinter as tk
    from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout, QGroupBox, QPushButton, QMessageBox
    import sys
    from PyQt6 import QtWidgets, uic


except ImportError:
    print('''ImportError : TowerDefense ne peux pas s'initialiser !\nAssurez vous d'avoir les modules necessaire a son fonctionement installés : 
   - pygame
   - tkinter
   - PyQT 6
Pour tout installer d'un coup, executer dans un terminal (bash/CMD) (pour linux, vous aurez besoin d'installer un environement virtuel) : 
   > pip install pygame PyQt6''')

features = {"one": 1, "two": 2}

class SnakeLauncher(QtWidgets.QMainWindow): #la classe a été en pertie (50% a peu pres, ) generée a l'aide d'outils d'intelligence atificielle, nous comprenons néemoins le code
    def __init__(self):
        super().__init__()

        uic.loadUi("ui_launcher.ui", self)
        
        # Créer un bouton de lancement
        self.start_button.clicked.connect(self.maingame_load)
        self.exitbtn.clicked.connect(sys.exit)

        #self.lives_checkbox.setEnabled(False)
        #self.timer_checkbox.setEnabled(False)
        #self.speed_checkbox.setEnabled(False)


    def update_lives(self, state):
        """Met à jour la variable lives_enabled selon l'état de la checkbox"""
        try:
            features[2] = state == 2  # 2 signifie "coché" en Qt6
            print(f"DEBUG : Deplacement de fruits: {features[0]}")
        except Exception as e:
            self.show_error_popup(e)
        
    def update_timer(self, state):
        """Met à jour la variable timer_enabled selon l'état de la checkbox"""
        try:
            features[1] = state == 2  # 2 signifie "coché" en Qt6
            print(f"DEBUG : Temps limite activé: {features[1]}")
        except Exception as e:
            self.show_error_popup(e)
    
    def update_degrade(self, state):
        """Met à jour la variable degrade selon l'état de la checkbox"""
        try:
            features[3] = state == 2  # 2 signifie "coché" en Qt6
            print(f"DEBUG : Degradé activé : {features[1]}")
        except Exception as e:
            self.show_error_popup(e)

    def show_error_popup(self, e):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erreur - Tower Defense")
        msg.setText("Une erreur est survenue durant l'exécution du jeu Tower Def !")
        if debug_allow:
            msg.setInformativeText(f"> {str(e)}\n\nSi cette erreur arrive plusieurs fois, nous te conseillons de rapporter l'erreur aux développeurs du jeu.\n\nTu peux essayer de continuer si tu pense que l'erreur n'est pas critique, mais la stabilitée du jeu pourra être affectée.")
        else:
            msg.setInformativeText(f"> {str(e)}\n\nTu peux nous envoyer un rapport d'erreur anonyme contenant le texte de l'erreur ainsi que des infos sur ton appareil si tu est d'accord, cela nous permet de patcher les bugs du jeu.")

        # Ajouter les trois boutons
        
        if debug_allow:
            continuer_btn = msg.addButton("Continuer", QMessageBox.ButtonRole.AcceptRole)
            quitter_btn = msg.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)
        else:
            quitter_btn = msg.addButton("Ne pas envoyer", QMessageBox.ButtonRole.RejectRole)
        rapporter_btn = msg.addButton("Envoyer le rapport", QMessageBox.ButtonRole.ActionRole)

        msg.exec()

        # Gérer la réponse
        if msg.clickedButton() == quitter_btn:
            pygame.quit()

        elif msg.clickedButton() == rapporter_btn:
            # Exemple : ouvrir un lien vers un formulaire de bug ou copier le message
            pygame.quit()
            QMessageBox.information(self, "Tower Defense", "Fonction non implementée actuellement.")
            # Ou tu peux faire autre chose ici


    def maingame_load(self):
        self.hide()
        #root = tk.Tk()
        #root.withdraw()
        #game.main()
        try:
            game.main()
        except Exception as e:
            if not str(e) == "video system not initialized":
                self.show_error_popup(e)
        #root.destroy()
        self.show()

if __name__ == "__main__":
    debug_allow = False
    app = QApplication(sys.argv)
    launcher = SnakeLauncher()
    launcher.show()
    sys.exit(app.exec())
