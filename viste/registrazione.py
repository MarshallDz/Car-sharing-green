from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Attivita.cliente import Cliente
import darkdetect


class VistaRegistrazione(QMainWindow):
    def __init__(self):
        super().__init__()
        # dizionario in cui salvi i campi del form
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

        self.title_label = QLabel("Crea il tuo account")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)

        # layout di tutto il form
        self.form_layout = QVBoxLayout()
        self.form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.crea_campo("codice fiscale")
        self.crea_campo("nome")
        self.crea_campo("cognome")
        self.crea_campo("data di nascita")
        self.crea_campo("e-mail")
        self.crea_campo("password")
        self.crea_campo("cellulare")

        # creo i bottoni invia e indietro
        invia_button = QPushButton("Invia")
        invia_button.setStyleSheet(
            "max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 35px; margin-top: 100px;")
        back_button = QPushButton("Indietro")
        back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 60px;")
        invia_button.clicked.connect(self.invio_dati)
        back_button.clicked.connect(self.go_back)
        self.form_layout.addWidget(invia_button)
        self.form_layout.addWidget(back_button)

        central_layout.addLayout(self.form_layout)

    def crea_campo(self, nome):
        if nome == "data di nascita":
            layout = QHBoxLayout()  # Layout orizzontale per posizionare la label accanto al campo
            label = QLabel("Data di nascita:")
            label.setStyleSheet("color: #a0a0a0")
            campo = QDateEdit()
            campo.setCalendarPopup(True)
            campo.setStyleSheet("color: black; background-color: white;")
            campo.setDate(QDate.currentDate())
            layout.addWidget(label)
            layout.addWidget(campo)
            self.form_layout.addLayout(layout)
        else:
            campo = QLineEdit()
            campo.setPlaceholderText(nome)
            campo.setStyleSheet("max-width: 300px; min-height: 40px; border-radius: 15px;")
            if darkdetect.isDark():
                campo.setStyleSheet("max-width: 300px; min-height: 40px; border-radius: 15px; "
                                    "background-color: #403f3f")
            self.form_layout.addWidget(campo)

        self.campi[nome] = campo

    def invio_dati(self):
        data_to_save = {}

        # Extracting data from fields and formatting for JSON
        for campo_nome, campo_widget in self.campi.items():
            if isinstance(campo_widget, QLineEdit):
                data_to_save[campo_nome] = campo_widget.text()
                if data_to_save[campo_nome] == "":
                    QMessageBox.critical(None, "Campi mancanti", "Tutti i campi devono essere compilati.")
                    return
            elif isinstance(campo_widget, QDateEdit):
                data_to_save[campo_nome] = campo_widget.date().toString(Qt.ISODate)
        if data_to_save["codice fiscale"].__len__() != 16:
            QMessageBox.warning(None, "CF non valido", "Il codice fiscale inserito non è valido.")
            return
        if not data_to_save["cellulare"].isdigit() or data_to_save["cellulare"].__len__() != 10:
            QMessageBox.warning(None, "Cellulare non valido", "Il numero di cellulare deve essere composto da 10 "
                                                              "cifre.")
            return
        cliente = Cliente()
        if cliente.aggiungiCliente(data_to_save["codice fiscale"], data_to_save["nome"], data_to_save["cognome"], data_to_save["data di nascita"], data_to_save["e-mail"], data_to_save["password"], data_to_save["cellulare"]):
            self.close()

    def go_back(self):
        from viste.welcome import WelcomeWindow
        self.vista = WelcomeWindow()
        self.vista.show()
        self.close()
