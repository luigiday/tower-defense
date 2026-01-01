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

def gameover(towerdict, depenses, ennemis_tues, duree, vagues):
    _get_app()

    dialog = QtWidgets.QDialog()
    uic.loadUi("gameover.ui", dialog)

    dialog.setWindowTitle("Fin de partie - Tower Defense")

    # defeir les valeurs dans la popup
    tours_label = dialog.findChild(QtWidgets.QLabel, "tours")
    vagues_label = dialog.findChild(QtWidgets.QLabel, "vagues")
    depenses_label = dialog.findChild(QtWidgets.QLabel, "depenses")
    ennemis_tues_label = dialog.findChild(QtWidgets.QLabel, "ennemis_tues")
    duree_label = dialog.findChild(QtWidgets.QLabel, "duree")
    def convertir_duree_en_MMSS(duree):
        m = int(duree // 60)
        s = int(duree % 60)
        return f"{m:02}:{s:02}" # le :02 affiche toujours 2 chiffres pour que le temps soit propre
    tours_label.setText(f"{len(towerdict):02}")
    duree_label.setText(f"{convertir_duree_en_MMSS(duree)}")
    vagues_label.setText(f"{vagues:02}")
    depenses_label.setText(f"{depenses:04} C")
    ennemis_tues_label.setText(f"{ennemis_tues:03}")

    rejouer_btn = dialog.findChild(QtWidgets.QPushButton, "rejouer_btn")
    rejouer_btn.setDefault(True)
    rejouer_btn.clicked.connect(dialog.accept)
    menu_btn = dialog.findChild(QtWidgets.QPushButton, "menu_btn")
    menu_btn.clicked.connect(dialog.reject)
    

    
    result = dialog.exec()
    if result == QtWidgets.QDialog.DialogCode.Accepted:
        return None
    else:
        if QMessageBox.question(None, "Quitter - Tower Defense", "Voulez-vous vraiment retourner au menu principal ?", QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No) == QMessageBox.StandardButton.Yes:
            pygame.quit()

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
