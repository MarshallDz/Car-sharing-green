from PyQt5.QtWidgets import *
import sys
from viste.welcome import WelcomeWindow
import json


def main():
    app = QApplication(sys.argv)
    welcome_window = WelcomeWindow()
    welcome_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()