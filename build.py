import sys
import os
import subprocess
from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QLabel, QPushButton, QVBoxLayout,
    QFileDialog, QCheckBox, QComboBox, QWidget, QMessageBox,
    QDialog, QProgressBar, QTextEdit, QHBoxLayout
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont


class BuildThread(QThread):
    build_complete = pyqtSignal(bool)
    output_updated = pyqtSignal(str)
    progress_updated = pyqtSignal(int)

    def __init__(self, command):
        super().__init__()
        self.command = command
        self._is_running = True
        self._was_stopped = False

    def stop(self):
        self._is_running = False
        self._was_stopped = True
        if hasattr(self, 'process'):
            try:
                self.process.terminate()
            except:
                pass

    def was_stopped(self):
        return self._was_stopped

    def run(self):
        try:
            # Split command for subprocess
            if os.name == 'nt':  # Windows
                self.process = subprocess.Popen(
                    self.command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1,
                    creationflags=subprocess.CREATE_NO_WINDOW
                )
            else:  # Unix-like systems
                self.process = subprocess.Popen(
                    self.command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    universal_newlines=True,
                    bufsize=1,
                    executable='/bin/bash'
                )

            # Read output line by line
            last_line = ""
            progress = 0

            while self._is_running and self.process.poll() is None:
                line = self.process.stdout.readline()
                if line:
                    last_line = line.strip()
                    self.output_updated.emit(last_line)

                    # Simple progress detection based on common PyInstaller output
                    if "Analyzing" in last_line:
                        progress = 25
                    elif "Processing" in last_line:
                        progress = 50
                    elif "Building" in last_line:
                        progress = 75
                    elif "completed successfully" in last_line.lower():
                        progress = 100
                    elif "writing" in last_line.lower():
                        progress = 85

                    self.progress_updated.emit(progress)

            # Read any remaining output
            if self._is_running:
                remaining_output, _ = self.process.communicate()
                if remaining_output:
                    lines = remaining_output.strip().split('\n')
                    for line in lines:
                        if line.strip():
                            self.output_updated.emit(line.strip())

            exit_code = self.process.returncode
            success = (exit_code == 0) and self._is_running
            self.build_complete.emit(success)

        except Exception as e:
            self.output_updated.emit(f"Error: {str(e)}")
            self.build_complete.emit(False)


class BuildDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Building Executable...")
        self.setGeometry(150, 150, 600, 250)
        self.setModal(True)

        # Apply dark theme
        self.setStyleSheet("""
            QDialog {
                background-color: #232629;
                color: #eff0f1;
            }
            QLabel {
                color: #eff0f1;
                padding: 2px;
            }
            QProgressBar {
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                text-align: center;
                background-color: #31363b;
                color: #eff0f1;
            }
            QProgressBar::chunk {
                background-color: #3daee9;
                border-radius: 3px;
            }
            QPushButton {
                background-color: #31363b;
                color: #eff0f1;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px 15px;
                min-width: 80px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border: 1px solid #3daee9;
            }
            QPushButton:pressed {
                background-color: #3daee9;
                color: #232629;
            }
            QLabel#outputLabel {
                background-color: #31363b;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 8px;
                color: #eff0f1;
                font-family: 'Courier New', monospace;
            }
        """)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setContentsMargins(15, 15, 15, 15)

        # Progress bar
        progress_label = QLabel("Progress:")
        progress_label.setFont(QFont("Segoe UI", 10))
        layout.addWidget(progress_label)

        self.progress_bar = QProgressBar()
        self.progress_bar.setRange(0, 100)
        self.progress_bar.setValue(0)
        self.progress_bar.setFont(QFont("Segoe UI", 9))
        layout.addWidget(self.progress_bar)

        # Last output line
        output_title = QLabel("Last output line:")
        output_title.setFont(QFont("Segoe UI", 10))
        layout.addWidget(output_title)

        self.output_label = QLabel("Starting build process...")
        self.output_label.setWordWrap(True)
        self.output_label.setObjectName("outputLabel")
        self.output_label.setMinimumHeight(60)
        self.output_label.setFont(QFont("Courier New", 9))
        layout.addWidget(self.output_label)

        # Cancel button
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel Build")
        self.cancel_button.setFont(QFont("Segoe UI", 10))
        self.cancel_button.clicked.connect(self.cancel_build)
        button_layout.addStretch()
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)

        self.setLayout(layout)

        self.build_thread = None

    def set_build_thread(self, build_thread):
        self.build_thread = build_thread
        build_thread.progress_updated.connect(self.update_progress)
        build_thread.output_updated.connect(self.update_output)
        build_thread.build_complete.connect(self.build_finished)

    def update_progress(self, value):
        self.progress_bar.setValue(value)

    def update_output(self, output):
        self.output_label.setText(output)
        # Auto-scroll to ensure we see the latest output
        QApplication.processEvents()

    def cancel_build(self):
        if self.build_thread and self.build_thread.isRunning():
            reply = QMessageBox.question(
                self,
                "Confirm Cancel",
                "Are you sure you want to cancel the build?",
                QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                QMessageBox.StandardButton.No
            )
            if reply == QMessageBox.StandardButton.Yes:
                self.build_thread.stop()
                self.cancel_button.setEnabled(False)
                self.cancel_button.setText("Cancelling...")
                self.output_label.setText("Cancelling build process...")

    def build_finished(self, success):
        if success:
            self.progress_bar.setValue(100)
            self.output_label.setText("Build completed successfully!")
            self.cancel_button.setText("Close")
            self.cancel_button.setEnabled(True)
            try:
                os.remove('build')
            except Exception as e:
                print(e)
            QTimer.singleShot(1500, self.accept)  # Close after 1.5 seconds on success
        else:
            if self.build_thread.was_stopped():
                self.output_label.setText("Build cancelled by user")
                self.cancel_button.setText("Close")
                self.cancel_button.setEnabled(True)
            else:
                self.output_label.setText("Build failed - check output for details")
                self.cancel_button.setText("Close")
                self.cancel_button.setEnabled(True)


class PyInstallerGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Utilitaire de build PyInstaller")
        self.setGeometry(100, 100, 600, 400)

        # Apply dark theme to main window
        self.setStyleSheet("""
            QMainWindow {
                background-color: #232629;
                color: #eff0f1;
            }
            QLabel {
                color: #eff0f1;
            }
            QPushButton {
                background-color: #31363b;
                color: #eff0f1;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 8px 15px;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #4d4d4d;
                border: 1px solid #3daee9;
            }
            QPushButton:disabled {
                background-color: #2a2e32;
                color: #6d6d6d;
                border: 1px solid #3d3d3d;
            }
            QComboBox {
                background-color: #31363b;
                color: #eff0f1;
                border: 1px solid #4d4d4d;
                border-radius: 4px;
                padding: 5px;
                min-width: 150px;
            }
            QComboBox:disabled {
                background-color: #2a2e32;
                color: #6d6d6d;
            }
            QCheckBox {
                color: #eff0f1;
                spacing: 5px;
            }
            QCheckBox::indicator {
                width: 16px;
                height: 16px;
            }
            QCheckBox::indicator:unchecked {
                border: 1px solid #4d4d4d;
                background-color: #31363b;
                border-radius: 2px;
            }
            QCheckBox::indicator:checked {
                border: 1px solid #3daee9;
                background-color: #3daee9;
                border-radius: 2px;
            }
            QCheckBox:disabled {
                color: #6d6d6d;
            }
        """)

        # Initialize paths
        self.script_path = ""
        self.files_and_folders = []
        self.output_folder = ""
        self.icon_path = ""

        # Main layout
        main_layout = QVBoxLayout()
        main_layout.setSpacing(10)
        main_layout.setContentsMargins(20, 20, 20, 20)

        # Script selection
        self.script_label = QLabel("Sélectionnez un script Python à build : ")
        main_layout.addWidget(self.script_label)

        self.select_script_button = QPushButton("Choisir un script")
        self.select_script_button.clicked.connect(self.select_script)
        main_layout.addWidget(self.select_script_button)

        # Files selection
        self.files_label = QLabel("Sélectionner des fichiers supplémentaires à inclure : ")
        main_layout.addWidget(self.files_label)

        self.select_files_button = QPushButton("Choisir des fichiers")
        self.select_files_button.clicked.connect(self.select_files)
        main_layout.addWidget(self.select_files_button)

        # Output folder selection
        self.output_label = QLabel("Sélectionner le dossier de sortie : ")
        main_layout.addWidget(self.output_label)

        self.select_output_button = QPushButton("Choisir le dossier")
        self.select_output_button.clicked.connect(self.select_output_folder)
        main_layout.addWidget(self.select_output_button)

        # Icon selection
        self.icon_label = QLabel("Aucune icône sélectionnée")
        main_layout.addWidget(self.icon_label)

        self.select_icon_button = QPushButton("Choisir une icône (.ico)")
        self.select_icon_button.clicked.connect(self.select_icon)
        main_layout.addWidget(self.select_icon_button)

        # Dropdown for mode
        self.mode_label = QLabel("Mode de l'application : ")
        main_layout.addWidget(self.mode_label)

        self.mode_dropdown = QComboBox()
        self.mode_dropdown.addItem("Console")
        self.mode_dropdown.addItem("Windowed")
        main_layout.addWidget(self.mode_dropdown)

        # Onefile option
        self.onefile_checkbox = QCheckBox("Empaqueter en un seul fichier")
        main_layout.addWidget(self.onefile_checkbox)

        # Build button
        self.build_button = QPushButton("Construire l'exécutable")
        self.build_button.clicked.connect(self.build_executable)
        main_layout.addWidget(self.build_button)

        # Status label
        self.status_label = QLabel("Créé par colin524 pour le projet Smoothgressi")
        self.status_label.setStyleSheet("color: #7f8c8d; font-style: italic;")
        main_layout.addWidget(self.status_label)

        # Set main widget
        container = QWidget()
        container.setLayout(main_layout)
        self.setCentralWidget(container)

    def select_script(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Python Script", "", "Python Files (*.py)")
        if file_path:
            self.script_path = file_path
            self.script_label.setText(f"Script sélectionné: {os.path.basename(file_path)}")

    def select_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select Files and Folders")
        if files:
            self.files_and_folders.extend(files)
            self.files_label.setText("Fichiers/dossiers sélectionnés: " + ", ".join([os.path.basename(f) for f in self.files_and_folders]))

    def select_output_folder(self):
        folder_path = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder_path:
            self.output_folder = folder_path
            self.output_label.setText(f"Dossier de sortie: {self.output_folder}")

    def select_icon(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Select Icon", "", "Icon Files (*.ico)")
        if file_path:
            self.icon_path = file_path
            self.icon_label.setText(f"Icône sélectionnée: {os.path.basename(file_path)}")

    def build_executable(self):
        if not self.script_path or not self.output_folder:
            QMessageBox.warning(self, "Erreur", "Veuillez sélectionner le script et le dossier de sortie.")
            return

        self.set_ui_enabled(False)
        self.setWindowTitle("Construction - Utilitaire de build PyInstaller")

        # Base command
        command = f"python3 -m pyinstaller --distpath \"{self.output_folder}\" "

        if self.onefile_checkbox.isChecked():
            command += "--onefile "

        if self.mode_dropdown.currentText() == "Windowed":
            command += "--noconsole "

        # Ajout de l'icône si sélectionnée
        if self.icon_path:
            command += f"--icon \"{self.icon_path}\" "

        for item in self.files_and_folders:
            command += f"--add-data \"{item};.\" "

        command += f"\"{self.script_path}\""
        print(command)

        self.status_label.setText("Construction en cours, veuillez patienter...")
        QApplication.processEvents()

        # Create and show build dialog
        self.build_dialog = BuildDialog(self)
        self.build_thread = BuildThread(command)
        self.build_dialog.set_build_thread(self.build_thread)

        # Start the build process
        self.build_thread.start()

        # Show the dialog and wait for it to close
        result = self.build_dialog.exec()

        # Handle the result after dialog closes
        self.on_build_complete()

    def on_build_complete(self):
        self.set_ui_enabled(True)
        self.setWindowTitle("Utilitaire de build PyInstaller")

        if self.build_thread.was_stopped():
            self.status_label.setText("Build annulé par l'utilisateur")
        elif self.build_thread.isFinished():
            # Check if build was successful
            if self.build_thread.exitCode() == 0:
                QMessageBox.information(self, "Succès", "Le build a été complété avec succès!")
                self.status_label.setText("Build réussi! ✅")
            else:
                QMessageBox.critical(self, "Erreur", "Le build a échoué. Veuillez vérifier l'output pour plus d'informations.")
                self.status_label.setText("❌ Erreur lors du build")

    def set_ui_enabled(self, enabled):
        self.build_button.setDisabled(not enabled)
        self.select_files_button.setDisabled(not enabled)
        self.select_output_button.setDisabled(not enabled)
        self.select_script_button.setDisabled(not enabled)
        self.select_icon_button.setDisabled(not enabled)
        self.mode_dropdown.setDisabled(not enabled)
        self.onefile_checkbox.setDisabled(not enabled)


if __name__ == "__main__":
    print("Utilitaire de compilation PyInstaller, crée par colin524 pour Smoothgressi")
    app = QApplication(sys.argv)
    window = PyInstallerGUI()
    window.show()
    sys.exit(app.exec())
