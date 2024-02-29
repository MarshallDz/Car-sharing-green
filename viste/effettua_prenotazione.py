import json
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDate


class VistaEffettuaPrenotazione(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Schermata di prenotazione")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QGridLayout()
        self.central_layout.setContentsMargins(20, 0, 20, 0)
        self.central_layout.setVerticalSpacing(100)
        self.central_widget.setLayout(self.central_layout)

        self.title_label = QLabel("Effettua la tua prenotazione ")
        self.title_label.setStyleSheet("color: white;")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.title_label.adjustSize()
        self.central_layout.addWidget(self.title_label, 0, 1)

        inizio_noleggio = QLabel("Data inizio noleggio:")
        inizio_noleggio.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(inizio_noleggio, 1, 0, alignment=Qt.AlignTop)

        campo1 = QDateEdit()
        campo1.setCalendarPopup(True)
        campo1.setMinimumDate(QDate.currentDate())
        campo1.setStyleSheet("color: black; background-color: white; max-width: 1000px; min-width: 800px")
        campo1.setDate(QDate.currentDate())
        self.central_layout.addWidget(campo1, 1, 3)

        fine_noleggio = QLabel("Data fine noleggio:")
        fine_noleggio.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(fine_noleggio, 2, 0, alignment=Qt.AlignTop)

        campo2 = QDateEdit()
        campo2.setCalendarPopup(True)
        campo2.setMinimumDate(QDate.currentDate())
        campo2.setStyleSheet("color: black; background-color: white; max-width: 1000px; min-width: 800px; margin-right: 15px")
        campo2.setDate(QDate.currentDate())
        self.central_layout.addWidget(campo2, 2, 3)

        filiale_label = QLabel("Filiale ritiro mezzo:")
        filiale_label.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(filiale_label, 3, 0)

        filiale = QComboBox(self)
        filiale.setStyleSheet("background-color: white; margin-right: 15px")
        filiale.setPlaceholderText(" ")
        filiale.addItems(["Milano, via padova", "Milano, via roma"])
        self.central_layout.addWidget(filiale, 3, 3)

        assicurazione_label = QLabel("Polizza assicurativa:")
        assicurazione_label.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(assicurazione_label, 4, 0)

        polizza = QComboBox(self)
        polizza.setStyleSheet("background-color: white; margin-right: 15px; color: black")
        polizza.setPlaceholderText(" ")
        polizza.addItems(["rca", "kasko"])
        self.central_layout.addWidget(polizza, 4, 3)

        tariffa = QLabel("Tariffa:")
        tariffa.setStyleSheet(f"color: white; font-size: 18px;")
        self.central_layout.addWidget(tariffa, 5, 0)

        tariffa = QComboBox(self)
        tariffa.setStyleSheet(f"background-color: white; margin-right: 15px;")
        tariffa.setPlaceholderText(" ")
        tariffa.addItems(["oraria", "giornaliera"])
        self.central_layout.addWidget(tariffa, 5, 3)

        conferma_button = QPushButton("Conferma")
        conferma_button.setStyleSheet(
            "width: 200px; max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px; margin-right: 40px;")
        self.central_layout.addWidget(conferma_button, 6, 3, alignment=Qt.AlignRight)

        back_button = QPushButton("Indietro")
        back_button.setStyleSheet(
            "width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px; margin-right: 50px")
        self.central_layout.addWidget(back_button, 7, 3, alignment=(Qt.AlignRight|Qt.AlignTop))
