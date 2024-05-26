


import os, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMenuBar, QLabel, QStatusBar
from PyQt6.QtGui import QAction, QKeySequence, QShortcut, QTextCursor

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
        infoAction = QAction('Shortcuts', self)
        infoAction.triggered.connect(self.info_window)

        # Create custom menu bar
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu('File')
        self.fileMenu2 = menuBar.addMenu('Info')


        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(createAction)
        self.fileMenu.addAction(readAction)
        
        # Do menu info
        self.fileMenu2.addAction(infoAction)
        
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
        self.load_shortcuts()
        self.load_words()

    
    def load_words(self):
        try:
            current_dir = os.getcwd()
            absolutePath = os.path.join(current_dir, "data/shortcuts.json")
            with open(absolutePath, 'r') as f:
                self.words = json.load(f)
        except Exception as e:
            print(f"Failed to load words: {e}")

    def load_shortcuts(self):
        try:
            current_dir = os.getcwd()
            absolutePath = os.path.join(current_dir, "data/config.json")
            with open(absolutePath, 'r') as f:
                shortcuts = json.load(f)
                for action, key in shortcuts.items():
                    self.create_shortcut(key, getattr(self, action))
        except Exception as e:
            print(f"Failed to load shortcuts: {e}")

    def create_shortcut(self, key_sequence, callback):
        shortcut = QShortcut(QKeySequence(key_sequence), self)
        shortcut.activated.connect(callback)

    def expand_shortcut(self):
        cursor = self.textEdit.textCursor()
        cursor.select(cursor.SelectionType.WordUnderCursor)
        txt = cursor.selectedText().strip()
        if txt in self.words:
            cursor.beginEditBlock()
            cursor.insertText(self.words[txt])
            cursor.endEditBlock()



    def go_to_previous_blank_line(self):
        cursor = self.textEdit.textCursor()
        moved = cursor.movePosition(cursor.MoveOperation.Up)
        cursor.movePosition(cursor.MoveOperation.StartOfLine)
        while moved and cursor.block().text().strip() != "":
            moved = cursor.movePosition(cursor.MoveOperation.Up)
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
        self.textEdit.setTextCursor(cursor)

    def go_to_next_blank_line(self):
        cursor = self.textEdit.textCursor()
        moved = cursor.movePosition(cursor.MoveOperation.Down)
        cursor.movePosition(cursor.MoveOperation.StartOfLine)
        while moved and cursor.block().text().strip() != "":
            moved = cursor.movePosition(cursor.MoveOperation.Down)
            cursor.movePosition(cursor.MoveOperation.StartOfLine)
        self.textEdit.setTextCursor(cursor)



    def go_to_previous_sentence(self):
        cursor = self.textEdit.textCursor()
        while not cursor.atStart() and cursor.document().characterAt(cursor.position() - 1) != '.':
            cursor.movePosition(cursor.MoveOperation.PreviousCharacter)
        cursor.movePosition(cursor.MoveOperation.PreviousCharacter)
        self.textEdit.setTextCursor(cursor)

    def go_to_next_sentence(self):
        cursor = self.textEdit.textCursor()
        while not cursor.atEnd() and cursor.document().characterAt(cursor.position()) != '.':
            cursor.movePosition(cursor.MoveOperation.NextCharacter)
        cursor.movePosition(cursor.MoveOperation.NextCharacter)
        self.textEdit.setTextCursor(cursor)

    def go_to_top(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.Start)
        self.textEdit.setTextCursor(cursor)

    def go_to_bottom(self):
        cursor = self.textEdit.textCursor()
        cursor.movePosition(cursor.MoveOperation.End)
        self.textEdit.setTextCursor(cursor)

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
    # Otwieranie okna z shortcut
    def info_window(self):
        self.w = infoWindow()
        self.w.show()

#Okno info 
class infoWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        self.textEdit = QTextEdit()
        layout = QVBoxLayout()

        self.label1 = QLabel("Skróty:\nCtrl+Up - poprzednia pusta linia\nCtrl+Down - następna pusta linia\nAlt+Left - poprzednie zdanie\nAlt+Right - następne zdanie\nCtrl+Home - na góre\nCtrl+End - na dół\nAlt+1 - szybkie stawienie słowa" )
        layout.addWidget(self.label1)
        self.label2 = QLabel("Słowa do szybkiego stawiania:\n re - requirements\n he - hello\n wi - windows\n wo - word")
        layout.addWidget(self.label2)
        self.setLayout(layout)

        self.setGeometry(300, 250, 500, 300)
        self.setWindowTitle('Shortcuts')
