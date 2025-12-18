from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QMessageBox
import pygame

def _get_app(): #Fontion écrite par chatgpt
    """Return existing QApplication or crash clearly."""
    app = QApplication.instance()
    if app is None:
        raise RuntimeError("QApplication not initialized")
    return app


def select_tower(solde, tower_dict):
    _get_app()

    dialog = QtWidgets.QDialog()
    uic.loadUi("select_tour.ui", dialog)

    dialog.setWindowTitle("Sélection de tour")

    solde_text = dialog.findChild(QtWidgets.QLabel, "label") # Sert a définir quel
    placer_btn = dialog.findChild(QtWidgets.QPushButton, "placer_btn")
    placer_btn.setEnabled(False)
    placer_btn.clicked.connect(dialog.accept)
    cancel_btn = dialog.findChild(QtWidgets.QPushButton, "cancel_btn")
    cancel_btn.clicked.connect(dialog.reject)
    solde_text.setText(f"Solde : {str(solde)} credits")

    def tour_selectionne(nom): #Fonction qui s'assure que le joueur peux payer la tour
        placer_btn.setText(f"Placer ({str(tower_dict[nom])} crédits)")
        if tower_dict[nom] <= solde:
            placer_btn.setEnabled(True) # Active le bouton pour placer
        else:
            placer_btn.setEnabled(False) # Bloque le bouton pour placer

    # Debut de la partie faite par IA (mais comprise)
    tower_buttons = [
        btn for btn in dialog.findChildren(QtWidgets.QAbstractButton)
        if btn.isCheckable() and btn.objectName() in tower_dict
    ]

    for btn in tower_buttons:
        btn.toggled.connect(
            lambda checked, name=btn.objectName(): (
                tour_selectionne(name) if checked else None
            )
        )
    
    result = dialog.exec()
    if result == QtWidgets.QDialog.DialogCode.Accepted:
        for btn in dialog.findChildren(QtWidgets.QAbstractButton):
            if btn.isChecked():
                return btn.objectName()
        return None

    # Fin du code generé par IA

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
