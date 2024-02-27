import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class VistaEffettuaPrenotazione(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Schermata di prenotazione")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(self.central_layout)

        self.title_label = QLabel("Effettua la tua prenotazione ")
        self.title_label.setStyleSheet("color: white;")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        self.central_layout.addLayout(title_layout)

        form_layout = QGridLayout()
        form_layout.setAlignment(Qt.AlignTop)
        form_layout.setVerticalSpacing(100)

        inizio_noleggio = QLabel("Data inizio noleggio:")
        inizio_noleggio.setStyleSheet("color: white; font-size: 18px")
        form_layout.addWidget(inizio_noleggio, 0, 0)

        fine_noleggio = QLabel("Data fine noleggio:")
        fine_noleggio.setStyleSheet("color: white; font-size: 18px")
        form_layout.addWidget(fine_noleggio, 2, 0)

        filiale = QLabel("Filiale ritiro mezzo:")
        filiale.setStyleSheet("color: white; font-size: 18px")
        form_layout.addWidget(filiale, 3, 0)

        assicurazione = QLabel("Polizza assicurativa:")
        assicurazione.setStyleSheet("color: white; font-size: 18px")
        form_layout.addWidget(assicurazione, 4, 0)

        tariffa = QLabel("Tariffa:")
        tariffa.setStyleSheet("color: white; font-size: 18px; margin-bottom: 150px")
        form_layout.addWidget(tariffa, 5, 0)
        self.central_layout.addLayout(form_layout)
