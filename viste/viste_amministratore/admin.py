import darkdetect
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, \
    QGridLayout

from viste.viste_amministratore.gestioneImpiegati import VistaGestioneImpiegati


class VistaAmministrazione(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        form_layout = QVBoxLayout()
        self.central_widget.setLayout(form_layout)

        upper_layout = QHBoxLayout()

        back_button = QPushButton("Esci")
        back_button.setStyleSheet("max-width: 200px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/logout.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        upper_layout.addWidget(back_button)

        self.title_label = QLabel("Manutenzione sistema")
        self.title_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        upper_layout.addWidget(self.title_label)

        power_button = QPushButton("Spegnimento")
        power_button.setStyleSheet("max-width: 200px; border: none")
        power_button.setIcon(QIcon("viste/Icone/varie/poweroff.png"))
        power_button.setIconSize(QSize(50, 50))
        upper_layout.addWidget(power_button)

        form_layout.addLayout(upper_layout)

        options_layout = QGridLayout()

        button1 = QPushButton("Gestisci impiegati")
        button1.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; font-size: 30px")
        button1.clicked.connect(self.go_GestioneImpiegati)

        button2 = QPushButton("Gestisci prenotazioni")
        button2.setStyleSheet(
            "width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; font-size: 30px")
        button2.clicked.connect(self.go_GestionePrenotazioni)

        button3 = QPushButton("Gestisci clienti")
        button3.setStyleSheet(
            "width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; font-size: 30px")
        button3.clicked.connect(self.go_GestioneClienti)

        button4 = QPushButton("Pagamenti")
        button4.setStyleSheet(
            "width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; font-size: 30px")
        button4.clicked.connect(self.go_pagamenti)

        button5 = QPushButton("Mezzi")
        button5.setStyleSheet(
            "width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; font-size: 30px")
        button5.clicked.connect(self.go_mezzi)

        button6 = QPushButton("Statistiche")
        button6.setStyleSheet(
            "width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: 25px; padding: 10px; font-size: 30px")
        button6.clicked.connect(self.go_statistiche)

        options_layout.addWidget(button1, 0, 0)
        options_layout.addWidget(button2, 0, 1)
        options_layout.addWidget(button3, 0, 2)
        options_layout.addWidget(button4, 1, 0)
        options_layout.addWidget(button5, 1, 1)
        options_layout.addWidget(button6, 1, 2)

        form_layout.addLayout(options_layout)

    def go_GestioneImpiegati(self):
        self.vista = VistaGestioneImpiegati()
        self.vista.show()
        self.close()

    def go_GestionePrenotazioni(self):
        pass
        # self.area = VistaGestionePrenotazione(self.user, self.psw)
        # self.area.show()
        # self.close()

    def go_GestioneClienti(self):
        pass
        # self.vista = VistaGestioneClienti(self.user, self.psw)
        # self.vista.show()
        # self.close()

    def go_pagamenti(self):
        pass
        # self.vista = VistaPagamentiImpiegato(self.user, self.psw)
        # self.vista.show()
        # self.close()

    def go_mezzi(self):
        pass
        # self.vista = VistaMezziImpiegato(self.user, self.psw)
        # self.vista.show()
        # self.close()

    def go_statistiche(self):
        pass
        # self.vista = VistaStatistiche(self.user, self.psw)
        # self.vista.show()
        # self.close()

    def go_back(self):
        from viste.login import VistaLogin
        self.vista = VistaLogin()
        self.vista.show()
        self.close()
