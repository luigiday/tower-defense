import sys
from PyQt6 import QtWidgets, uic
from PyQt6.QtWidgets import QApplication, QWidget, QCheckBox, QVBoxLayout, QGroupBox, QPushButton, QMessageBox
def select_tower(solde):
    # DO NOT create a new QApplication here!
    # Your main launcher already created it.

    dialog = QtWidgets.QDialog()
    uic.loadUi("select_tour.ui", dialog)

    # OPTIONAL: If you want the solde to appear in the UI
    if hasattr(dialog, "solde_label"):
        dialog.solde_label.setText(str(solde))

    # Run UI as a modal dialog
    result = dialog.exec_()

    # RETURN something depending on UI (placeholder)
    # You must replace this with your actual selection logic.
    if result == QtWidgets.QDialog.Accepted:
        # Example: return the value of a QListWidget
        if hasattr(dialog, "tower_list"):
            return dialog.tower_list.currentItem().text()
        return True  # fallback
    return None


def show_error_popup(e):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Icon.Critical)
        msg.setWindowTitle("Erreur - Tower Defense")
        msg.setText("Une erreur est survenue durant l'exécution du jeu Tower Def !")
        msg.setInformativeText(f"> {str(e)}\n\nSi cette erreur arrive plusieurs fois, nous te conseillons de rapporter l'erreur aux développeurs du jeu.\n\nTu peux essayer de continuer si tu pense que l'erreur n'est pas critique, mais la stabilitée du jeu pourra être affectée.")
        

        # Ajouter les trois boutons
        
        continuer_btn = msg.addButton("Continuer", QMessageBox.ButtonRole.AcceptRole)
        quitter_btn = msg.addButton("Quitter", QMessageBox.ButtonRole.RejectRole)


        msg.exec()

        # Gérer la réponse
        if msg.clickedButton() == quitter_btn:
            pygame.quit()

        elif msg.clickedButton() == continuer_btn:
            pass