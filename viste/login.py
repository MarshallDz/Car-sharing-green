from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Attivita.cliente import Cliente
from viste.home import VistaHome
import darkdetect


class VistaLogin(QMainWindow):
    def __init__(self):
        super().__init__()
        self.campi = {}

        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(central_layout)

        self.title_label = QLabel("Accedi")
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

        invia_button = QPushButton("Invia")
        invia_button.setStyleSheet(
            "max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 150px; margin-top: 10px;")
        back_button = QPushButton("Annulla")
        back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 175px;")
        invia_button.clicked.connect(self.verifica_dati)
        back_button.clicked.connect(self.go_back)
        self.form_layout.addWidget(invia_button)
        self.form_layout.addWidget(back_button)
        central_layout.addLayout(self.form_layout)

    def crea_campo(self, nome):
        campo = QLineEdit()
        if nome == "password":
            campo.setEchoMode(2)
        campo.setPlaceholderText(nome)
        campo.setStyleSheet("max-width: 500px; min-height: 60px; border-radius: 15px; ")
        if darkdetect.isDark():
            campo.setStyleSheet("max-width: 500px; min-height: 60px; border-radius: 15px; "
                                "background-color: #403F3F")
        self.campi[nome] = campo
        self.form_layout.addWidget(campo)

    def verifica_dati(self):
        data_to_match = {}

        for campo_nome, campo_widget in self.campi.items():
            data_to_match[campo_nome] = campo_widget.text()
            if data_to_match[campo_nome] == "":
                QMessageBox.critical(None, "Campi mancanti", "Tutti i campi devono essere compilati.")
                return

        # da risolvere la doppia chiamata alla funzione
        email = Cliente.get_login(self)[0]
        password = Cliente.get_login(self)[1]

        trovato = False
        for e in email:
            if e == data_to_match["email"]:
                i = email.index(e)
                if password[i] == data_to_match["password"]:
                    trovato = True
                    self.vista_home = VistaHome(e, password[i])
                    self.vista_home.show()
                    self.close()
                    break

        if not trovato:
            QMessageBox.warning(None, "Errore", "L'utente o la password sono errati! \nRiprova")
            self.campi["email"].clear()
            self.campi["password"].clear()
            return

    def go_back(self):
        from viste.welcome import WelcomeWindow
        self.vista = WelcomeWindow()
        self.vista.show()
        self.close()