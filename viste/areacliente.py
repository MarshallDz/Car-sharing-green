import json

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, QMessageBox
from Attivita.cliente import Cliente
import darkdetect


class VistaCliente(QMainWindow):
    def __init__(self, user, psw):
        super().__init__()

        self.user = user
        self.psw = psw
        self.cliente = Cliente.get_dati(self, self.user, self.psw)
        self.campi = {}
        self.setWindowTitle("Profilo utente")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)
        self.central_widget.setLayout(self.layout)

        icona = QLabel()
        foto = QPixmap("Attivita/Icone/varie/boy.png")
        foto.setDevicePixelRatio(3.5)
        icona.setPixmap(foto)
        icona.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(icona)
        self.crea_campo("codice fiscale", self.cliente["codiceFiscale"])
        self.crea_campo("nome", self.cliente["nome"])
        self.crea_campo("cognome", self.cliente["cognome"])
        self.crea_campo("data di nascita", self.cliente["dataNascita"])
        self.email = self.crea_campo("e-mail", self.cliente["email"])
        self.password = self.crea_campo("password", self.cliente["password"])
        self.cellulare = self.crea_campo("cellulare", self.cliente["cellulare"])

        self.modify_button = QPushButton("Modifica")
        self.modify_button.setCheckable(True)
        self.modify_button.clicked.connect(self.modifica)
        self.back_button = QPushButton("Torna alla home")
        self.modify_button.setStyleSheet(
            "max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 150px; margin-top: 50px;")
        self.layout.addWidget(self.modify_button)
        self.layout.addWidget(self.back_button)
        self.back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 175px; margin-top: 10px")
        self.back_button.clicked.connect(self.go_back)

    def crea_campo(self, nome, valore):
        titolo = QLabel(nome)
        titolof = QFont("Arial", 12, QFont.Bold)
        titolo.setFont(titolof)
        titolo.adjustSize()
        self.layout.addWidget(titolo)
        campo = QLineEdit()
        campo.setText(valore)
        campo.setReadOnly(True)
        campo.setStyleSheet("max-width: 500px; min-height: 40px; background-color: #e3e1dc; color: black;")
        if nome == "e-mail" or nome == "password":
            self.campi[nome] = campo
        self.layout.addWidget(campo)
        return campo

    def modifica(self):
        self.email.setReadOnly(False)
        self.email.setStyleSheet("max-width: 500px; min-height: 40px;background-color: #e3e1dc;")
        self.password.setReadOnly(False)
        self.password.setStyleSheet("max-width: 500px; min-height: 40px;background-color: #e3e1dc;")
        self.cellulare.setReadOnly(False)
        self.cellulare.setStyleSheet("max-width: 500px; min-height: 40px; background-color: #e3e1dc;")
        self.modify_button.setText("Conferma")
        self.modify_button.toggled.connect(self.conferma)
        self.back_button.setText("Annulla")

    def conferma(self):
        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Question)
        message_box.setText("Sei sicuro di voler modificare i tuoi dati di accesso?")
        message_box.setWindowTitle("Salvataggio")
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)

        risposta = message_box.exec_()

        if risposta == QMessageBox.Save:
            login = {}
            for campo_nome, campo_widget in self.campi.items():
                login[campo_nome] = campo_widget.text()
            with open("dati/clienti.json", "r") as file:
                data = json.load(file)

            # Cerca il cliente specifico usando il suo codice fiscale
            for c in data["clienti"]:
                if c["codiceFiscale"] == self.cliente["codiceFiscale"]:
                    # Aggiungi il codice della nuova prenotazione alla lista delle prenotazioni del cliente
                    c["email"] = login["e-mail"]
                    c["password"] = login["password"]
                    break

            # Scrivi i dati aggiornati nel file JSON
            with open("dati/clienti.json", "w") as file:
                json.dump(data, file, indent=4)

            self.cliente["email"] = login["e-mail"]
            self.cliente["password"] = login["password"]
            QMessageBox.information(None, "Success", "Dati modificati correttamente!")
            from viste.home import VistaHome
            self.vista = VistaHome(self.cliente["email"], self.cliente["password"])
            self.vista.show()
            self.close()

    def go_back(self):
        from viste.home import VistaHome
        self.vista = VistaHome(self.user, self.psw)
        self.vista.show()
        self.close()
