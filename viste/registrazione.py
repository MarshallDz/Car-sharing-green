import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class VistaRegistrazione(QMainWindow):
   def __init__(self):
      super().__init__()
      self.setWindowTitle("Pagina di registrazione")
      self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
      self.setStyleSheet("background-color: #121212;")

      central_widget = QWidget()
      self.setCentralWidget(central_widget)

      layout = QVBoxLayout()
      layout.setAlignment(Qt.AlignHCenter | Qt.AlignTop)
      central_widget.setLayout(layout)

