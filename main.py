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
    from PyQt6.QtGui import QDesktopServices
    from PyQt6.QtCore import pyqtSignal, QUrl
    import threading
    import urllib.request as urlreq
    import json
    import re
    

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

# Current local version of the launcher/game. Update this when releasing a new version.
# Use the same tag format as your GitHub releases (for example: "v1.2.3" or "1.2.3").
__version__ = "v1.0.1"


def _normalize_version(tag: str) -> str:
    """Strip leading 'v' or other non-numeric prefix and return a plain numeric version string."""
    if not tag:
        return "0"
    # remove leading non-digit characters (like 'v')
    tag = re.sub(r"^[^0-9]+", "", str(tag))
    return tag


def _parse_version_parts(version: str):
    """Return a tuple of ints for numeric comparison. Non-numeric parts will be treated as 0."""
    parts = version.split(".")
    nums = []
    for p in parts:
        m = re.match(r"^(\d+)", p)
        nums.append(int(m.group(1)) if m else 0)
    # pad to 3 parts for simple semver-like compare
    while len(nums) < 3:
        nums.append(0)
    return tuple(nums[:3])


def is_version_newer(latest_tag: str, current_tag: str) -> bool:
    """Return True if latest_tag represents a newer semantic version than current_tag."""
    latest = _normalize_version(latest_tag)
    current = _normalize_version(current_tag)
    return _parse_version_parts(latest) > _parse_version_parts(current)


def fetch_latest_release(owner: str, repo: str, timeout: float = 5.0):
    """Query GitHub API for the latest release. Returns dict or None on error.

    Uses the public API endpoint: https://api.github.com/repos/{owner}/{repo}/releases/latest
    No external dependencies required.
    """
    api = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"
    try:
        with urlreq.urlopen(api, timeout=timeout) as resp:
            if resp.status != 200:
                return None
            data = resp.read().decode("utf-8")
            return json.loads(data)
    except Exception:
        return None

class SnakeLauncher(QtWidgets.QMainWindow): #la classe a été en pertie (50% a peu pres, ) generée a l'aide d'outils d'intelligence atificielle, nous comprenons néemoins le code
    # signal emitted when an update is available: (latest_tag, release_url, release_notes)
    update_available = pyqtSignal(str, str, str)

    def __init__(self):
        super().__init__()

        uic.loadUi("ui_launcher.ui", self)
        
        self.start_button.clicked.connect(self.maingame_load)
        self.exitbtn.clicked.connect(sys.exit)
        QShortcut(QKeySequence("Ctrl+D"), self).activated.connect(self.enable_debug_mode) #Ctrl+D pour activer le mode debug
        QShortcut(QKeySequence("Ctrl+E"), self).activated.connect(self.launch_no_error_handle)

        # connect update signal -> UI slot and start background check
        try:
            self.update_available.connect(self.show_update_dialog)
            # start the background thread that queries GitHub for latest release
            threading.Thread(target=self._check_updates_worker, daemon=True).start()
        except Exception:
            # if signals or threading are not available for any reason, ignore silently
            pass

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
            if not str(e).startswith("pygame"): #ignorer les erreurs pygame car elles arrivent en gereral a la fermeture du jeu a cause de la maniere dont pygame gere sa boucle principale
                self.show_error_popup(e)
        self.show()


    def _check_updates_worker(self):
        """Background worker: queries GitHub API and emits update_available if there's a newer release.

        Change `owner` and `repo` below if your repository is different.
        """
        owner = "luigiday"
        repo = "tower-defense"
        info = fetch_latest_release(owner, repo)
        if not info:
            return
        latest_tag = info.get("tag_name") or info.get("name")
        html_url = info.get("html_url") or f"https://github.com/{owner}/{repo}/releases"
        release_notes = info.get("body", "") or ""
        if latest_tag and is_version_newer(latest_tag, __version__):
            try:
                # emit signal to show dialog on main thread (include release notes)
                self.update_available.emit(latest_tag, html_url, release_notes)
            except Exception:
                return


    def show_update_dialog(self, latest_tag: str, release_url: str, release_notes: str):
        """Run on the main thread (slot): show a QMessageBox offering to open the release page.

        The release notes are shown in the expandable 'details' area via setDetailedText().
        """
        msg = QMessageBox(self)
        msg.setIcon(QMessageBox.Icon.Information)
        msg.setWindowTitle("Mise à jour disponible")
        msg.setText(f"Nouvelle version disponible : {latest_tag}\nVous utilisez : {__version__}")
        msg.setInformativeText("Voulez-vous ouvrir la page des releases pour télécharger la nouvelle version ?")
        # put release notes into the detailed text (expandable) area
        if release_notes:
            msg.setDetailedText(f"Nouveautées de la version {latest_tag} :\n{release_notes}")
        open_btn = msg.addButton("Télecharger", QMessageBox.ButtonRole.AcceptRole)
        ignore_btn = msg.addButton("Plus tard", QMessageBox.ButtonRole.RejectRole)
        msg.exec()
        if msg.clickedButton() == open_btn:
            # open release page in user's default browser
            QDesktopServices.openUrl(QUrl(release_url))

if __name__ == "__main__":
    debug_allow = False
    app = QApplication(sys.argv)
    launcher = SnakeLauncher()
    launcher.show()
    sys.exit(app.exec())
