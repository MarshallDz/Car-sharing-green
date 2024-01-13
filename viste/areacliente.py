import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel


class VistaCliente(QMainWindow):
    def __init__(self, c):
        super().__init__()

        self.setWindowTitle("Profilo utente")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(self.layout)

        icona = QLabel()
        foto = QPixmap("Attivita/Icone/boy.png")
        foto.setDevicePixelRatio(3.5)
        icona.setPixmap(foto)
        icona.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(icona)
        self.crea_campo("codice fiscale: %s" % c["codiceFiscale"])
        self.crea_campo("nome: %s" % c["nome"])
        self.crea_campo("cognome: %s" % c["cognome"])
        self.crea_campo("data di nascita: %s" % c["dataNascita"])
        self.crea_campo("e-mail: %s" % c["email"])
        self.crea_campo("password: %s" % c["password"])
        self.crea_campo("cellulare: %s" % c["cellulare"])

        modify_button = QPushButton("Modifica")
        back_button = QPushButton("Torna alla home")
        self.layout.addWidget(modify_button)
        modify_button.setStyleSheet(
            "max-width: 200px; background-color: #edf5f3; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 150px; margin-top: 50px;")
        self.layout.addWidget(back_button)
        back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 175px; margin-top: 10px")
        back_button.clicked.connect(self.close)

    def crea_campo(self, nome):
        campo = QLineEdit()
        campo.setPlaceholderText(nome)
        campo.setReadOnly(True)
        campo.setStyleSheet("max-width: 500px; min-height: 40px; color: grey; background-color: #e3e1dc;")
        self.layout.addWidget(campo)


# app = QApplication(sys.argv)

# window = VistaCliente()
# window.show()

# app.exec_()
