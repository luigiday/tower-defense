#le code de l'ui pr le launcher et tt ce qui est textuel...
try:
    import pygame
    import game
    #from tkinter import messagebox
    #import tkinter as tk
    from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout, QGroupBox, QPushButton, QMessageBox
    import sys
    from PyQt6 import QtWidgets, uic
    from PyQt6.QtGui import QKeySequence, QShortcut
    

except ImportError:
    print('''ImportError : TowerDefense ne peux pas s'initialiser !\nAssurez vous d'avoir les modules necessaire a son fonctionement installés : 
   - pygame
   - tkinter
   - PyQT 6
Pour tout installer d'un coup, executer dans un terminal (bash/CMD) (pour linux, vous aurez besoin d'installer un environement virtuel) : 
   > pip install pygame PyQt6''')
    rep = input("Voulez-vous tenter de les installer automatiquement ? (O/N) : ")
    if rep == "o" or rep == "O":
        import os
        try:
            os.system("pip install PyQt6 pygame")
        except Exception as e:
            print(f"Erreur : {e}")
        finally:
            print("Veuillez relancer pour appliquer")
    else:
        print("Abandon")
        exit()
    
features = {"one": 1, "two": 2}
debug_show = False

class SnakeLauncher(QtWidgets.QMainWindow): #la classe a été en pertie (50% a peu pres, ) generée a l'aide d'outils d'intelligence atificielle, nous comprenons néemoins le code
    def __init__(self):
        super().__init__()

        uic.loadUi("ui_launcher.ui", self)
        
        self.start_button.clicked.connect(self.maingame_load)
        self.exitbtn.clicked.connect(sys.exit)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.enable_debug_mode) #Ctrl+D pour activer le mode debug
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(self.launch_no_error_handle)

    def enable_debug_mode(self):
        global debug_show
        debug_show = True
        QMessageBox.information(self, "Mode Debug Activé", "Le mode debug a été activé. Les messages de debogage s'afficheront sur la carte du jeu. Pour desactiver, quitter et relancer le jeu.")

    def launch_no_error_handle(self):
        global debug_show
        if QMessageBox.question(self, "Lancer le jeu - Tower Defense", "Voulez-vous lancer le jeu Tower Defense sans gestion des erreurs ?\nCela peut causer des plantages du jeu sans message d'erreur.", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            self.hide()
            game.main(debug_show)
            self.show()
    def show_error_popup(self, e):
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erreur - Tower Defense")
        msg.setText("Une erreur est survenue durant l'exécution du jeu Tower Def !")
        if debug_allow:
            msg.setInformativeText(f"> {str(e)}\n\nSi cette erreur arrive plusieurs fois, nous te conseillons de rapporter l'erreur aux développeurs du jeu.\n\nTu peux essayer de continuer si tu pense que l'erreur n'est pas critique, mais la stabilitée du jeu pourra être affectée.")
        else:
            msg.setInformativeText(f"> {str(e)}\n\nTu peux nous envoyer un rapport d'erreur anonyme contenant le texte de l'erreur ainsi que des infos sur ton appareil si tu est d'accord, cela nous permet de patcher les bugs du jeu.")
        
        if debug_allow:
            continuer_btn = msg.addButton("Continuer", QMessageBox.ButtonRole.AcceptRole)
            quitter_btn = msg.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)
        else:
            quitter_btn = msg.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)

        msg.exec()

        if msg.clickedButton() == quitter_btn:
            pygame.quit()

        


    def maingame_load(self):
        global debug_show
        self.hide()
        #game.main()
        try:
            game.main(debug_show)
        except Exception as e:
            if not str(e) == "video system not initialized":
                self.show_error_popup(e)
        self.show()

if __name__ == "__main__":
    debug_allow = False
    app = QApplication(sys.argv)
    launcher = SnakeLauncher()
    launcher.show()
    sys.exit(app.exec())
