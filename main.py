from PyQt5.QtWidgets import *
import sys
from viste.welcome import WelcomeWindow
import qdarktheme


def main():
    app = QApplication(sys.argv)
    qdarktheme.setup_theme("auto")
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()