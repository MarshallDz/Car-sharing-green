import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from viste.registrazione import VistaRegistrazione
from viste.login import VistaLogin
import darkdetect

class WelcomeWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Benvenuto")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if(darkdetect.isDark()):
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Aggiungi un layout verticale al widget centrale
        central_layout = QVBoxLayout()
        central_layout.setAlignment(Qt.AlignJustify)
        central_widget.setLayout(central_layout)

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop)

        self.title_label = QLabel("Benvenuto, accedi oppure registrati", self)
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)

        # Aggiungi un layout orizzontale per allineare i pulsanti
        buttons_layout = QVBoxLayout()
        buttons_layout.setAlignment(Qt.AlignCenter | Qt.AlignTop)

        self.accedi_button = QPushButton("Accedi")
        self.accedi_button.setStyleSheet("background-color: #6AFE67; color: black; border-radius: 15px; padding: "
                                         "20px; width: 500px; border-style: inset")
        self.accedi_button.setFont(QFont("Arial", 16))
        self.accedi_button.setCheckable(True)
        self.accedi_button.clicked.connect(self.go_login)
        self.accedi_button.adjustSize()
        buttons_layout.addWidget(self.accedi_button)
        self.registrati_button = QPushButton("Registrati")
        self.registrati_button.setStyleSheet("background-color: #d9d9d9; color: black; border-radius: 15px; padding: "
                                             "20px;")
        self.registrati_button.setFont(QFont("Arial", 16))
        self.registrati_button.setCheckable(True)
        self.registrati_button.clicked.connect(self.go_registrazione)
        self.registrati_button.adjustSize()
        buttons_layout.addWidget(self.registrati_button)
        central_layout.addLayout(buttons_layout)

    def go_registrazione(self):
        self.vista_registrazione = VistaRegistrazione()
        self.vista_registrazione.show()
        self.close()

    def go_login(self):
        self.vista_login = VistaLogin()
        self.vista_login.show()
        self.close()
