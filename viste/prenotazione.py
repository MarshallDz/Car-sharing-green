from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from viste.prenotazione_auto import VistaPrenotazioneAuto

class VistaPrenotazione(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pagina di prenotazione")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(central_layout)

        self.title_label = QLabel("Scegli il mezzo da prenotare: ")
        self.title_label.setStyleSheet("color: white;")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)

        self.buttons_layout = QVBoxLayout()
        self.buttons_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.auto_button = QPushButton("Prenota auto")
        self.auto_button.setStyleSheet(
            "color: black; width: 700px; background-color: #d9d9d9; border-radius: 15px; padding: 20px;")
        self.auto_button.clicked.connect(self.go_auto)

        self.scooter_button = QPushButton("Prenota scooter")
        self.scooter_button.setStyleSheet(
            "color: black; width: 700px; background-color: #d9d9d9; border-radius: 15px; padding: 20px;")

        self.van_button = QPushButton("Prenota van")
        self.van_button.setStyleSheet(
            "color: black; width: 700px; background-color: #d9d9d9; border-radius: 15px; padding: 20px;")

        self.furgone_button = QPushButton("Prenota furgone")
        self.furgone_button.setStyleSheet(
            "color: black; width: 700px; background-color: #d9d9d9; border-radius: 15px; padding: 20px;")

        self.buttons_layout.addWidget(self.auto_button)
        self.buttons_layout.addWidget(self.scooter_button)
        self.buttons_layout.addWidget(self.van_button)
        self.buttons_layout.addWidget(self.furgone_button)

        self.back_layout = QVBoxLayout()
        self.back_layout.setAlignment(Qt.AlignBottom | Qt.AlignRight)
        self.back_button = QPushButton("Indietro")
        self.back_button.setStyleSheet(
            "width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-right: 60px; margin-bottom: 120px;")
        self.back_button.clicked.connect(self.close_window)
        self.back_layout.addWidget(self.back_button)
        central_layout.addLayout(self.buttons_layout)
        central_layout.addLayout(self.back_layout)

    def close_window(self):
        self.close()

    def go_auto(self):
        self.vista_auto = VistaPrenotazioneAuto()
        self.vista_auto.show()