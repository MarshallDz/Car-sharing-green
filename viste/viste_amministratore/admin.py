import darkdetect
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QHBoxLayout, QVBoxLayout, QPushButton, QLabel, \
    QGridLayout, QMessageBox

from viste.viste_amministratore.gestioneClienti import VistaGestioneClienti
from viste.viste_amministratore.gestioneImpiegati import VistaGestioneImpiegati
from viste.viste_amministratore.gestioneMezzi import VistaMezziAmministratore
from viste.viste_amministratore.gestionePagamenti import VistaPagamentiAmministratore
from viste.viste_amministratore.gestionePrenotazioni import VistaGestionePrenotazione


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

        l_layout = QVBoxLayout()
        back_button = QPushButton("Esci")
        back_button.setStyleSheet("max-width: 200px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/logout.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        l_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        l_layout.addWidget(back_button)
        upper_layout.addLayout(l_layout)

        m_layout = QVBoxLayout()
        self.title_label = QLabel("Manutenzione sistema")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        m_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        m_layout.addWidget(self.title_label)
        upper_layout.addLayout(m_layout)

        r_layout = QVBoxLayout()
        power_button = QPushButton("Shut down")
        power_button.setStyleSheet("max-width: 200px; border: none")
        power_button.setIcon(QIcon("viste/Icone/varie/poweroff.png"))
        power_button.setIconSize(QSize(50, 50))
        power_button.clicked.connect(self.shutdown)
        r_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        r_layout.addWidget(power_button)
        upper_layout.addLayout(r_layout)

        form_layout.addLayout(upper_layout)

        options_layout = QGridLayout()
        options_layout.setSpacing(50)
        options_layout.setContentsMargins(10, 0, 10, 50)

        button1 = QPushButton("Impiegati")
        button1.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: "
                              "25px; padding: 10px; font-size: 20px")
        button1.clicked.connect(self.go_GestioneImpiegati)

        button2 = QPushButton("Clienti")
        button2.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: "
                              "25px; padding: 10px; font-size: 20px")
        button2.clicked.connect(self.go_GestioneClienti)

        button3 = QPushButton("Prenotazioni")
        button3.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: "
                              "25px; padding: 10px; font-size: 20px")
        button3.clicked.connect(self.go_GestionePrenotazioni)

        button4 = QPushButton("Pagamenti")
        button4.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: "
                              "25px; padding: 10px; font-size: 20px")
        button4.clicked.connect(self.go_pagamenti)

        button5 = QPushButton("Mezzi")
        button5.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: "
                              "25px; padding: 10px; font-size: 20px")
        button5.clicked.connect(self.go_mezzi)

        button6 = QPushButton("Statistiche")
        button6.setStyleSheet("width: 200px; height: 200px; color: black; background-color: #D9D9D9; border-radius: "
                              "25px; padding: 10px; font-size: 20px")
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
        self.area = VistaGestionePrenotazione()
        self.area.show()
        self.close()

    def go_GestioneClienti(self):
        pass
        self.vista = VistaGestioneClienti()
        self.vista.show()
        self.close()

    def go_pagamenti(self):
        self.vista = VistaPagamentiAmministratore()
        self.vista.show()
        self.close()

    def go_mezzi(self):
        self.vista = VistaMezziAmministratore()
        self.vista.show()
        self.close()

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

    def shutdown(self):
        reply = QMessageBox.warning(self, "Conferma chiusura", "Sei sicuro di voler interrompere il servizio?",
                                    QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()
