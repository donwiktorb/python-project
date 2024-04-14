


from PyQt6.QtWidgets import QApplication 
import sys

from classes.notepad import Notepad

def main():
    app = QApplication(sys.argv)
    notepad = Notepad()


    sys.exit(app.exec())

if __name__ == '__main__':
    main()
