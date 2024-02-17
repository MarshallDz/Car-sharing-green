import sys

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon, QFont
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
        self.crea_campo("codice fiscale", c["codiceFiscale"])
        self.crea_campo("nome", c["nome"])
        self.crea_campo("cognome", c["cognome"])
        self.crea_campo("data di nascita", c["dataNascita"])
        self.email = self.crea_campo("e-mail", c["email"])
        self.password = self.crea_campo("password", c["password"])
        self.cellulare = self.crea_campo("cellulare", c["cellulare"])

        self.modify_button = QPushButton("Modifica")
        self.modify_button.setCheckable(True)
        self.modify_button.clicked.connect(self.modifica)
        self.back_button = QPushButton("Torna alla home")
        self.modify_button.setStyleSheet(
            "max-width: 200px; background-color: #edf5f3; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 150px; margin-top: 50px;")
        self.layout.addWidget(self.modify_button)
        self.layout.addWidget(self.back_button)
        self.back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 175px; margin-top: 10px")
        self.back_button.clicked.connect(self.close)

    def crea_campo(self, nome, valore):
        titolo = QLabel(nome)
        titolo.setStyleSheet("color: white;")
        titolof = QFont("Arial", 12, QFont.Bold)
        titolo.setFont(titolof)
        titolo.adjustSize()
        self.layout.addWidget(titolo)
        campo = QLineEdit()
        campo.setText(valore)
        campo.setReadOnly(True)
        campo.setStyleSheet("max-width: 500px; min-height: 40px; color: grey; background-color: #e3e1dc;")
        self.layout.addWidget(campo)
        return campo

    def modifica(self):
        self.email.setReadOnly(False)
        self.email.setStyleSheet("max-width: 500px; min-height: 40px; color: black; background-color: #e3e1dc;")
        self.password.setReadOnly(False)
        self.password.setStyleSheet("max-width: 500px; min-height: 40px; color: black; background-color: #e3e1dc;")
        self.cellulare.setReadOnly(False)
        self.cellulare.setStyleSheet("max-width: 500px; min-height: 40px; color: black; background-color: #e3e1dc;")
        self.modify_button.setText("Conferma")
        self.modify_button.clicked.connect(self.conferma)
        # self.back_button.clicked.connect()

    def conferma(self):
        pass

# app = QApplication(sys.argv)

# window = VistaCliente()
# window.show()

# app.exec_()
