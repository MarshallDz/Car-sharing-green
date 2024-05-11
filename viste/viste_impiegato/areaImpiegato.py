import json

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, \
    QMessageBox, QHBoxLayout
from Attivita.impiegato import Impiegato
import darkdetect


class VistaImpiegato(QMainWindow):
    def __init__(self, user, psw):
        super().__init__()

        self.user = user
        self.psw = psw
        impiegato = Impiegato()
        self.impiegato = impiegato.get_dati(self.user, self.psw)
        self.campi = {}
        self.setWindowTitle("CarGreen")
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
        foto = QPixmap("viste/Icone/varie/boy.png")
        foto.setDevicePixelRatio(3.5)
        icona.setPixmap(foto)
        icona.setAlignment(Qt.AlignCenter)
        self.layout.addWidget(icona)
        self.crea_campo("codice fiscale", self.impiegato["codiceFiscale"])
        self.crea_campo("nome", self.impiegato["nome"])
        self.crea_campo("cognome", self.impiegato["cognome"])
        self.crea_campo("data di nascita", self.impiegato["dataNascita"])
        self.email = self.crea_campo("e-mail", self.impiegato["email"])
        self.password = self.crea_campo("password", self.impiegato["password"])
        self.cellulare = self.crea_campo("cellulare", self.impiegato["cellulare"])

        self.modify_button = QPushButton("Modifica")
        self.modify_button.clicked.connect(self.modifica)
        self.back_button = QPushButton("Torna alla home")
        self.modify_button.setStyleSheet(
            "max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 200px; margin-top: 20px;")
        self.layout.addWidget(self.modify_button)
        self.layout.addWidget(self.back_button)
        self.back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 225px; margin-top: 10px")
        self.back_button.clicked.connect(self.go_back)

    def crea_campo(self, nome, valore):
        layout = QHBoxLayout()
        titolo = QLabel(nome)
        titolof = QFont("Arial", 12, QFont.Bold)
        titolo.setFont(titolof)
        titolo.adjustSize()
        titolo.setStyleSheet("max-width: 100px; margin-left: 150px")
        layout.addWidget(titolo)
        campo = QLineEdit()
        campo.setText(valore)
        campo.setReadOnly(True)
        campo.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; background-color: #e3e1dc; color: black;")
        if nome == "e-mail" or nome == "password" or nome == "cellulare":
            self.campi[nome] = campo
        layout.addWidget(campo)
        self.layout.addLayout(layout)
        return campo

    def modifica(self):
        self.email.setReadOnly(False)
        self.email.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; border-radius: 10px; background-color: #c0e3fc;")
        self.password.setReadOnly(False)
        self.password.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; border-radius: 10px; background-color: #c0e3fc;")
        self.cellulare.setReadOnly(False)
        self.cellulare.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; border-radius: 10px; background-color: #c0e3fc;")
        self.modify_button.setText("Conferma")
        self.modify_button.clicked.connect(self.conferma)
        self.back_button.setText("Annulla")
        self.back_button.clicked.connect(self.annulla)

    def annulla(self):
        self.email.setReadOnly(True)
        self.email.setStyleSheet("max-width: 500px; min-height: 40px; background-color: #e3e1dc;")
        self.password.setReadOnly(True)
        self.password.setStyleSheet(
            "max-width: 500px; min-height: 40px; background-color: #e3e1dc;")
        self.cellulare.setReadOnly(True)
        self.cellulare.setStyleSheet(
            "max-width: 500px; min-height: 40px; background-color: #e3e1dc;")
        self.modify_button.setText("Modifica")
        self.modify_button.clicked.connect(self.modifica)
        self.back_button.setText("Torna alla home")
        self.back_button.clicked.connect(self.go_back)

    def conferma(self):
        login = {}
        for campo_nome, campo_widget in self.campi.items():
            login[campo_nome] = campo_widget.text()
        if not login["cellulare"].isdigit() or login["cellulare"].__len__() != 10:
                QMessageBox.warning(None, "Cellulare non valido", "Il numero di cellulare deve essere composto da 10 "
                                                        "cifre.")
                return

        message_box = QMessageBox()
        message_box.setIcon(QMessageBox.Question)
        message_box.setText("Sei sicuro di voler modificare i tuoi dati personali?")
        message_box.setWindowTitle("Salvataggio")
        message_box.setStandardButtons(QMessageBox.Save | QMessageBox.Cancel)

        risposta = message_box.exec_()

        if risposta == QMessageBox.Save:
            with open("dati/impiegati.json", "r") as file:
                data = json.load(file)

            # Cerca il cliente specifico usando il suo codice fiscale
            for c in data["impiegati"]:
                if c["codiceFiscale"] == self.cliente["codiceFiscale"]:
                    # Aggiorno i dati del cliente
                    c["email"] = login["e-mail"]
                    c["password"] = login["password"]
                    c["cellulare"] = login["cellulare"]
                    break

            # Scrivi i dati aggiornati nel file JSON
            with open("dati/impiegati.json", "w") as file:
                json.dump(data, file, indent=4)

            # Aggiorno i dati della variabile cliente
            self.cliente["email"] = login["e-mail"]
            self.cliente["password"] = login["password"]
            self.cliente["cellulare"] = login["cellulare"]
            QMessageBox.information(None, "Success", "Dati modificati correttamente!")
            from viste.viste_impiegato.pannelloControllo import VistaPannelloControllo
            self.vista = VistaPannelloControllo(self.impiegato["email"], self.impiegato["password"])
            self.vista.show()
            self.close()

    def go_back(self):
        from viste.viste_impiegato.pannelloControllo import VistaPannelloControllo
        self.vista = VistaPannelloControllo(self.user, self.psw)
        self.vista.show()
        self.close()
