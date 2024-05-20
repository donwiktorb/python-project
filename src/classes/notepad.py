


import os, json
from PyQt6.QtWidgets import QApplication, QMainWindow, QTextEdit, QMessageBox, QVBoxLayout, QWidget, QPushButton, QFileDialog, QMenuBar, QLabel, QStatusBar
from PyQt6.QtGui import QAction, QKeySequence, QShortcut

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
        preferenceAction = QAction('Config', self)
        preferenceAction.triggered.connect(self.pref_window)

        # Create custom menu bar
        menuBar = self.menuBar()
        self.fileMenu = menuBar.addMenu('File')
        self.fileMenu2 = menuBar.addMenu('Preference')


        self.fileMenu.addAction(saveAction)
        self.fileMenu.addAction(createAction)
        self.fileMenu.addAction(readAction)
        
        # Do menu Preference
        self.fileMenu2.addAction(preferenceAction)
        
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
    # Otwieranie okna z config
    def pref_window(self):
        self.w = PrefWindow()
        self.w.show()
        self.close()

#Okno configu 
class PrefWindow(QWidget):
    
    def __init__(self):
        super().__init__()

        self.init_ui()
    
    def init_ui(self):
        self.textEdit = QTextEdit()
        layout = QVBoxLayout()

        self.label1 = QLabel("Jakiś skrót:" )
        layout.addWidget(self.label1)
        self.label2 = QLabel("Jakiś skrót" )
        layout.addWidget(self.label2)
        self.label3 = QLabel("Jakiś skrót" )
        layout.addWidget(self.label3)

        self.button = QPushButton("Zatwierdź zmiany")
        self.button.clicked.connect(self.changes)
        layout.addWidget(self.button)

        self.setLayout(layout)

        self.setGeometry(300, 250, 500, 300)
        self.setWindowTitle('Config')
    
    #powrót do Notatnika
    def changes(self):
        
        self.w=Notepad()
        self.w.show()
        self.close()

