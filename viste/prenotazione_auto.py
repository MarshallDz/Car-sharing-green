from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class VistaPrenotazioneAuto(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pagina di registrazione")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(central_layout)

        self.title_label = QLabel("Prenota la tua auto: ")
        self.title_label.setStyleSheet("color: white;")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)