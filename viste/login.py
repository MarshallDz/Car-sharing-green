from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

class VistaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.campi = {}

        self.setWindowTitle("Pagina di login")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(central_layout)

        self.title_label = QLabel("Accedi")
        self.title_label.setStyleSheet("color: white;")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)

        # layout di tutto il form
        self.form_layout = QVBoxLayout()
        self.form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.crea_campo("email")
        self.crea_campo("password")

        central_layout.addLayout(self.form_layout)

    def crea_campo(self, nome):
        campo = QLineEdit()
        campo.setPlaceholderText(nome)
        campo.setStyleSheet("max-width: 500px; min-height: 60px; background-color: #403F3F; border-radius: 15px;")
        self.campi[nome] = campo
        self.form_layout.addWidget(campo)