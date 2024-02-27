from PyQt5.QtWidgets import *
import sys
from viste.welcome import WelcomeWindow
from viste.effettua_prenotazione import VistaEffettuaPrenotazione


def main():
    app = QApplication(sys.argv)
    welcome_window = VistaEffettuaPrenotazione()
    welcome_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()