


import os
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMenuBar
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
        readAction = QAction('Read', self)
        readAction.triggered.connect(self.readFile)

        # Create custom menu bar
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu('File')



        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(readAction)

        self.setGeometry(100, 100, 800, 600)
        self.setWindowTitle('Notepad')
        self.setStyleSheet(self.readStyleSheet())
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

