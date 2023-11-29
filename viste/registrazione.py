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

      central_layout = QVBoxLayout()

      title_layout = QVBoxLayout()
      title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

      central_widget.setLayout(central_layout)

      self.title_label = QLabel("Crea il tuo account")
      self.title_label.setStyleSheet("color: white;")
      self.title_font = QFont("Arial", 42, QFont.Bold)
      self.title_label.setFont(self.title_font)
      self.title_label.adjustSize()

      title_layout.addWidget(self.title_label)
      central_layout.addLayout(title_layout)

      #layout di tutto il form
      self.form_layout = QVBoxLayout()
      self.form_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

      #layout di un campo di inserimento con label
      self.campo_layout = QHBoxLayout()

      self.crea_campo("nome")
      #self.crea_campo("cognome")

      self.form_layout.setLayout(self.campo_layout)
      central_layout.addLayout(self.form_layout)
   def crea_campo(self, nome):
      label = QLabel(nome)
      campo = QLineEdit()
      campo.setStyleSheet("max-width: 100px; background-color: #403F3F;")
      self.campo_layout.addWidget(label)
      self.campo_layout.addWidget(campo)
