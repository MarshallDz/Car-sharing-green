import sys

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *


class VistaHome(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Home")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        form_layout = QHBoxLayout()
        self.central_widget.setLayout(form_layout)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        cliente_button = QPushButton("Area clienti")
        cliente_button.setStyleSheet("color: white;")
        # per i file esterni bisogna mettere il percorso completo rispetto al programma che avvia l'app (main)
        cliente_button.setIcon(QIcon("viste/Icone/boy.png"))
        cliente_button.setIconSize(QSize(50, 50))
        cliente_button.clicked.connect(self.area_clienti)
        left_layout.addWidget(cliente_button)
        form_layout.addLayout(left_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignTop)
        self.title_label = QLabel("Home")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("color: white;")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        center_layout.addWidget(self.title_label)

        options_layout = QGridLayout()
        button1 = QPushButton("Nuova \nprenotazione")
        button1.setStyleSheet(
            "max-width: 150px; background-color: #74b1fc; border-radius: 55px; color: black; padding: 100px; "
            "margin-top: 100px;")
        button2 = QPushButton("Storico \nnoleggi")
        button2.setStyleSheet(
            "max-width: 150px; background-color: #74b1fc; border-radius: 55px; color: black; padding: 100px; "
            "margin-top: 100px;")
        button3 = QPushButton("Cancella \nuna prenotazione")
        button3.setStyleSheet(
            "max-width: 150px; background-color: #74b1fc; border-radius: 55px; color: black; padding: 100px;")
        button4 = QPushButton("Gestisci \npagamenti")
        button4.setStyleSheet(
            "max-width: 150px; background-color: #74b1fc; border-radius: 55px; color: black; padding: 100px;")
        options_layout.addWidget(button1, 0, 0)
        options_layout.addWidget(button2, 0, 1)
        options_layout.addWidget(button3, 1, 0)
        options_layout.addWidget(button4, 1, 1)
        options_layout.setSpacing(50)
        center_layout.addLayout(options_layout)
        form_layout.addLayout(center_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        back_button = QPushButton("Esci")
        back_button.setStyleSheet("color: white;")
        back_button.setIcon(QIcon("viste/Icone/logout.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.close)
        right_layout.addWidget(back_button)
        form_layout.addLayout(right_layout)

    def area_clienti(self):
        print("ok")