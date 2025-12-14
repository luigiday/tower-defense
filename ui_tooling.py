from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMessageBox
import pygame
#Ce code a été patché (presence de bugs) avec ChatGPT, neanmoins le code original avait été écrit par nous

tower_dict = {"sapintueur": 300, "cristalexplosif": 500, "tourlectrique": 200}

def _get_app(): #Fontion écrite par chatgpt
    """Return existing QApplication or crash clearly."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication not initialized")
    return app


def select_tower(solde):
    _get_app()  # ensure Qt is alive

    dialog = QtWidgets.QDialog()
    uic.loadUi("select_tour.ui", dialog)

    dialog.setWindowTitle("Sélection de tour")

    

    #for btn in dialog.findChildren(QtWidgets.QAbstractButton):
    #    print(f"{btn.objectName()}.clicked.connect(update_text({btn.objectName()}))")

    #for btn in dialog.findChildren(QtWidgets.QAbstractButton):
    #    btn.clicked.connect(print(btn.objectName()))

    #start_button.clicked.connect(self.maingame_load)

    result = dialog.exec()  # IMPORTANT

    for btn in dialog.findChildren(QtWidgets.QAbstractButton):
        if btn.isChecked():
            return btn.objectName()
    return None

ERROR = '''Traceback (most recent call last):
  File "/home/flare/Lycee/1ere/Documents/NSI/Projets/projet-NSI-tower-defense/main.py", line 97, in maingame_load
    game.main()
    ~~~~~~~~~^^
  File "/home/flare/Lycee/1ere/Documents/NSI/Projets/projet-NSI-tower-defense/game.py", line 74, in main
    ui_tooling.select_tower(argent)
    ~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^
  File "/home/flare/Lycee/1ere/Documents/NSI/Projets/projet-NSI-tower-defense/ui_tooling.py", line 30, in select_tower
    btn.clicked.connect(print(btn.objectName()))
    ~~~~~~~~~~~~~~~~~~~^^^^^^^^^^^^^^^^^^^^^^^^^
TypeError: argument 1 has unexpected type 'NoneType'
Abandon                    (core dumped)/bin/python /home/flare/Lycee/1ere/Documents/NSI/Projets/projet-NSI-tower-defense/main.py
'''

def show_error_popup(e):
    _get_app()

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Critical)
    msg.setWindowTitle("Erreur - Tower Defense")
    msg.setText("Une erreur est survenue durant l'exécution du jeu Tower Def !")
    msg.setInformativeText(str(e))

    continuer_btn = msg.addButton("Continuer", QMessageBox.ButtonRole.AcceptRole)
    quitter_btn = msg.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)

    msg.exec()

    if msg.clickedButton() == quitter_btn:
        pygame.quit()
        raise SystemExit


def ask_for_exit():
    _get_app()

    msg = QMessageBox()
    msg.setIcon(QMessageBox.Icon.Question)
    msg.setWindowTitle("Quitter - Tower Defense")
    msg.setText("Voulez-vous vraiment abandonner votre partie ?")
    msg.setInformativeText("Votre score et vos dépenses ne seront pas sauvegardés")

    giveup_btn = msg.addButton("Abandonner", QMessageBox.ButtonRole.AcceptRole)
    continue_btn = msg.addButton("Reprendre", QMessageBox.ButtonRole.RejectRole)

    msg.exec()

    if msg.clickedButton() == giveup_btn:
        pygame.quit()
        raise SystemExit
        return True
    return False
