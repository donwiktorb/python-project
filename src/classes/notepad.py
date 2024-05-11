


import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMenuBar, QLabel, QStatusBar
from PyQt6.QtGui import QAction
class Notepad(QMainWindow):
    def __init__(self):
        super().__init__()

        self.init_ui()

    def init_ui(self):
        self.textEdit = QTextEdit()
        self.setCentralWidget(self.textEdit)

        saveAction= QAction('Save', self)
        saveAction.triggered.connect(self.saveFile)
        createAction = QAction('Save as', self)
        createAction.triggered.connect(self.createFile)
        readAction = QAction('Read', self)
        readAction.triggered.connect(self.readFile)

        # Create custom menu bar
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu('File')



        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(createAction)
        self.fileMenu.addAction(readAction)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Notepad')
        self.setStyleSheet(self.readStyleSheet())

        #Status bar
        self.statusBar().showMessage("")
        self.statusBar().setStyleSheet("border :0px solid black;")
        
        #Liczenie słów
        self.word_count_label = QLabel("Słowa: 0", self)
        self.word_count_label.setStyleSheet("border :0px solid white; margin-right :3px; margin-left :3px;")   #
        self.statusBar().addPermanentWidget(self.word_count_label)

        def update_word_count():
            word_count = len(self.textEdit.toPlainText().split())
            self.word_count_label.setText(f"Słowa: {word_count}   ")
        
        self.textEdit.textChanged.connect(update_word_count)
        
        #Liczenie znaków
        self.char_count_label = QLabel("Znaki: 0", self)
        self.char_count_label.setStyleSheet("border :0px solid white; margin-right :3px; margin-left :3px;")   #
        self.statusBar().addPermanentWidget(self.char_count_label)

        def update_char_count():
            char_count = len(self.textEdit.toPlainText())
            self.char_count_label.setText(f"Znaki: {char_count}")
        
        self.textEdit.textChanged.connect(update_char_count)
        
        self.show()

    def readStyleSheet(self, filePath="styles/style.css"):
        current_dir = os.getcwd()
        absolutePath = os.path.join(current_dir, filePath)
        try:
            with open(absolutePath, 'r') as file:
                return file.read()
        except Exception as e:
            QMessageBox.critical(self, 'Error', f'An error occurred while the stylesheet: {str(e)}')
            return ''

    def saveFile(self):
        filePath, _ = QFileDialog.getSaveFileName(self, 'Save File')
        if filePath:
            try:
                with open(filePath, 'w') as file:
                    file.write(self.textEdit.toPlainText())
                QMessageBox.information(self, 'Success', 'File saved successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'An error occurred while saving the file: {str(e)}')

    def readFile(self):
        filePath, _ = QFileDialog.getOpenFileName(self, 'Read File')
        if filePath:
            try:
                with open(filePath, 'r') as file:
                    self.textEdit.setPlainText(file.read())
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'An error occurred while opening the file: {str(e)}')

    def createFile(self):
        filePath, _ = QFileDialog.getSaveFileName(self, 'Create File', filter="Text files (*.txt)")
        if filePath:
            try:
                # Dodanie rozszerzenia .txt, jeśli nie zostało podane ręcznie przez użytkownika
                if not filePath.endswith(".txt"):
                    filePath += ".txt"

                # Tworzenie nowego pliku tekstowego
                with open(filePath, 'w') as file:
                    pass  # Plik jest tworzony pusty
                QMessageBox.information(self, 'Success', 'File created successfully!')
            except Exception as e:
                QMessageBox.critical(self, 'Error', f'An error occurred while creating the file: {str(e)}')
