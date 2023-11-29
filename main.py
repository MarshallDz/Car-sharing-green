from PyQt5.QtWidgets import *
import sys
from viste.welcome import WelcomeWindow
from viste.registrazione import VistaRegistrazione

def main():
    app = QApplication(sys.argv)
    welcome_window = VistaRegistrazione()
    welcome_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()