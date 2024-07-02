import json

from PyQt5.QtCore import *
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QLabel, \
    QMessageBox, QHBoxLayout
from Attivita.impiegato import Impiegato
import darkdetect


class VistaImpiegato(QMainWindow):
    def __init__(self, impiegato):
        super().__init__()

        self.impiegato = impiegato
        self.campi = {}
        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        title_layout = QHBoxLayout()
        back_button = QPushButton()
        back_button.setStyleSheet("max-width: 100px; border: none; margin-bottom: 100px")
        back_button.setIcon(QIcon("viste/Icone/varie/back.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)

        title_layout.addWidget(back_button)
        icona = QLabel()
        foto = QPixmap("viste/Icone/varie/boy.png")
        foto.setDevicePixelRatio(3.5)
        icona.setPixmap(foto)
        icona.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(icona)
        ghost_button = QPushButton()
        ghost_button.setStyleSheet("max-width: 100px; border: none")
        title_layout.addWidget(ghost_button)
        self.layout.addLayout(title_layout)

        self.crea_campo("codice fiscale", self.impiegato["codiceFiscale"])
        self.crea_campo("nome", self.impiegato["nome"])
        self.crea_campo("cognome", self.impiegato["cognome"])
        self.crea_campo("data di nascita", self.impiegato["dataNascita"])
        self.email = self.crea_campo("e-mail", self.impiegato["email"])
        self.password = self.crea_campo("password", self.impiegato["password"])
        self.cellulare = self.crea_campo("cellulare", self.impiegato["cellulare"])

        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter)
        self.modify_button = QPushButton("Modifica")
        self.modify_button.clicked.connect(self.modifica)
        self.modify_button.setStyleSheet(
            "width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px;"
            "margin-top: 20px")
        self.cancel_button = QPushButton("Annulla")
        self.cancel_button.clicked.connect(self.annulla)
        self.cancel_button.setStyleSheet(
            "width: 200px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-top: 10px")
        self.cancel_button.hide()
        buttons_layout.addWidget(self.modify_button)
        buttons_layout.addWidget(self.cancel_button)
        self.layout.addLayout(buttons_layout)

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
        campo.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; background-color: #e3e1dc; color: black")
        if nome == "e-mail" or nome == "password" or nome == "cellulare":
            self.campi[nome] = campo
        layout.addWidget(campo)
        layout.setAlignment(Qt.AlignCenter)
        self.layout.addLayout(layout)
        return campo

    def modifica(self):
        self.modify_button.clicked.disconnect(self.modifica)
        self.modify_button.clicked.connect(self.conferma)
        self.cancel_button.show()
        self.email.setReadOnly(False)
        self.email.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; border-radius: 10px; "
                                 "background-color: #c0e3fc;")
        self.password.setReadOnly(False)
        self.password.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; border-radius: 10px; "
                                    "background-color: #c0e3fc;")
        self.cellulare.setReadOnly(False)
        self.cellulare.setStyleSheet("margin-right: 200px; max-width: 200px; min-height: 40px; border-radius: 10px; "
                                     "background-color: #c0e3fc;")
        self.modify_button.setText("Conferma")

    def annulla(self):
        self.modify_button.clicked.disconnect(self.conferma)
        self.cancel_button.hide()
        self.email.setReadOnly(True)
        self.email.setStyleSheet(
            "margin-right: 200px; max-width: 200px; min-height: 40px; background-color: #e3e1dc; color: black")
        self.password.setReadOnly(True)
        self.password.setStyleSheet(
            "margin-right: 200px; max-width: 200px; min-height: 40px; background-color: #e3e1dc; color: black")
        self.cellulare.setReadOnly(True)
        self.cellulare.setStyleSheet(
            "margin-right: 200px; max-width: 200px; min-height: 40px; background-color: #e3e1dc; color: black")
        self.modify_button.setText("Modifica")
        self.modify_button.clicked.connect(self.modifica)

    def conferma(self):
        self.modify_button.clicked.disconnect(self.conferma)
        self.modify_button.clicked.connect(self.modifica)

        login = {}
        for campo_nome, campo_widget in self.campi.items():
            login[campo_nome] = campo_widget.text()
        if not login["cellulare"].isdigit() or login["cellulare"].__len__() != 10:
            QMessageBox.warning(None, "Cellulare non valido", "Il numero di cellulare deve essere composto da 10 cifre.")
            return

        reply = QMessageBox.warning(self, 'Conferma Modifica', 'Sei sicuro di voler modificare i tuoi dati?',
                                    QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            impiegato = Impiegato()
            # Cerca l'impiegato specifico usando il suo codice fiscale
            data = impiegato.readData("dati/impiegati.json")
            for c in data:
                if c["codiceFiscale"] == self.impiegato["codiceFiscale"]:
                    # Aggiorno i dati del cliente
                    c["email"] = login["e-mail"]
                    c["password"] = login["password"]
                    c["cellulare"] = login["cellulare"]

            # Scrivi i dati aggiornati nel file JSON
            impiegato.writeData("dati/impiegati.json", data)
            QMessageBox.information(self, 'Modifica confermata', 'I dati sono stai aggiornati con successo.',
                                    QMessageBox.Ok)

            # Aggiorno i dati della variabile cliente
            self.impiegato["email"] = login["e-mail"]
            self.impiegato["password"] = login["password"]
            self.impiegato["cellulare"] = login["cellulare"]

            from viste.viste_impiegato.pannelloControllo import VistaPannelloControllo
            self.vista = VistaPannelloControllo(self.impiegato)
            self.vista.show()
            self.close()
        else:
            return

    def go_back(self):
        from viste.viste_impiegato.pannelloControllo import VistaPannelloControllo
        self.vista = VistaPannelloControllo(self.impiegato)
        self.vista.show()
        self.close()
