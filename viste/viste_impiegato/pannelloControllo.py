from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from viste.viste_impiegato.areaImpiegato import VistaImpiegato
from viste.viste_impiegato.gestionePrenotazioni import VistaGestionePrenotazione
from viste.viste_impiegato.gestioneClienti import VistaGestioneClienti
from viste.viste_impiegato.gestionePagamenti import VistaPagamentiImpiegato
from viste.viste_impiegato.gestioneMezzi import VistaMezziImpiegato
import darkdetect


class VistaPannelloControllo(QMainWindow):
    def __init__(self, impiegato):
        super().__init__()
        self.impiegato = impiegato
        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        form_layout = QHBoxLayout()
        self.central_widget.setLayout(form_layout)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        cliente_button = QPushButton("Area utente")
        cliente_button.setStyleSheet("max-width: 200px; border: none")
        cliente_button.setIcon(QIcon("viste/Icone/varie/boy.png"))
        cliente_button.setIconSize(QSize(50, 50))
        cliente_button.clicked.connect(self.area_impiegati)
        left_layout.addWidget(cliente_button)
        form_layout.addLayout(left_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignTop)
        self.title_label = QLabel("Pannello di controllo")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        center_layout.addWidget(self.title_label)

        options_layout = QVBoxLayout()
        button1 = QPushButton("Prenotazioni")
        button1.setStyleSheet(
            "width: 500px; height: 100px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; "
            "margin-top: 100px; font-size: 20px;")
        button1.clicked.connect(self.go_GestionePrenotazioni)
        button2 = QPushButton("Clienti")
        button2.setStyleSheet(
            "width: 500px; height: 100px; background-color: #D9D9D9; border-radius: 25px; color: black; padding: "
            "10px; font-size: 20px")
        button2.clicked.connect(self.go_GestioneClienti)
        button3 = QPushButton("Pagamenti")
        button3.setStyleSheet(
            "width: 500px; height: 100px; background-color: #D9D9D9; border-radius: 25px; color: black; padding: "
            "10px; font-size: 20px")
        button3.clicked.connect(self.go_pagamenti)
        button4 = QPushButton("Mezzi")
        button4.setStyleSheet(
            "width: 500px; height: 100px; background-color: #D9D9D9; border-radius: 25px; color: black; padding: "
            "10px; font-size: 20px")
        button4.clicked.connect(self.go_mezzi)
        options_layout.addWidget(button1)
        options_layout.addWidget(button2)
        options_layout.addWidget(button3)
        options_layout.addWidget(button4)
        options_layout.setSpacing(30)
        center_layout.addLayout(options_layout)
        form_layout.addLayout(center_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        back_button = QPushButton("Esci")
        back_button.setStyleSheet("max-width: 200px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/logout.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        right_layout.addWidget(back_button)
        form_layout.addLayout(right_layout)

    def area_impiegati(self):
        self.area = VistaImpiegato(self.impiegato)
        self.area.show()
        self.close()

    def go_GestionePrenotazioni(self):
        self.area = VistaGestionePrenotazione(self.impiegato)
        self.area.show()
        self.close()

    def go_GestioneClienti(self):
        self.vista = VistaGestioneClienti(self.impiegato)
        self.vista.show()
        self.close()

    def go_back(self):
        from viste.login import VistaLogin
        self.vista = VistaLogin()
        self.vista.show()
        self.close()

    def go_pagamenti(self):
        self.vista = VistaPagamentiImpiegato(self.impiegato)
        self.vista.show()
        self.close()

    def go_mezzi(self):
        self.vista = VistaMezziImpiegato(self.impiegato)
        self.vista.show()
        self.close()
