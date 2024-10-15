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
        self.showMaximized()
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

        self.crea_campo("Codice Fiscale")
        self.crea_campo("Nome")
        self.crea_campo("Cognome")
        self.crea_campo("Data di nascita")
        self.crea_campo("E-mail")
        self.crea_campo("Password")
        self.crea_campo("Cellulare")

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
        if nome == "Data di nascita":
            layout = QHBoxLayout()  # Layout orizzontale per posizionare la label accanto al campo
            label = QLineEdit()
            label.setPlaceholderText(nome)
            label.setStyleSheet("max-width: 100px; min-height: 40px; border-radius: 15px;")
            label.setReadOnly(True)
            campo = QDateEdit()
            campo.setCalendarPopup(True)
            campo.setStyleSheet("max-width: 200px; color: black; background-color: white;")
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
        cliente = Cliente()
        for campo_nome, campo_widget in self.campi.items():
            if isinstance(campo_widget, QLineEdit):
                data_to_save[campo_nome] = campo_widget.text()
                if data_to_save[campo_nome] == "":
                    QMessageBox.critical(None, "Campi mancanti", "Tutti i campi devono essere compilati.")
                    return
            elif isinstance(campo_widget, QDateEdit):
                data_to_save[campo_nome] = campo_widget.date().toString(Qt.ISODate)
        clienti = cliente.get_dati()

        # controllo univocita
        for user in clienti:
            if user["email"] == data_to_save["E-mail"]:
                QMessageBox.information(None, "attenzione", "Email già registrata")
                return
        if data_to_save["Codice Fiscale"].__len__() != 16:
            QMessageBox.warning(None, "CF non valido", "Il codice fiscale inserito non è valido.")
            return
        if not data_to_save["Cellulare"].isdigit() or data_to_save["Cellulare"].__len__() != 10:
            QMessageBox.warning(None, "Cellulare non valido", "Il numero di cellulare deve essere composto da 10 "
                                                              "cifre.")
            return
            # Controllo che l'utente sia almeno diciottenne
        data_nascita = QDate.fromString(data_to_save["Data di nascita"], Qt.ISODate)
        eta = QDate.currentDate().year() - data_nascita.year()
        if eta < 18 or (eta == 18 and QDate.currentDate() < data_nascita.addYears(18)):
            QMessageBox.warning(None, "Età non valida", "Devi avere almeno 18 anni per registrarti.")
            return
        if len(data_to_save["Password"])<8:
            QMessageBox.warning(None, "Password non valida", "La password deve contenere almeno 8 caratteri!")
            return
        if cliente.aggiungiCliente(data_to_save["Codice Fiscale"], data_to_save["Nome"], data_to_save["Cognome"], data_to_save["Data di nascita"], data_to_save["E-mail"], data_to_save["Password"], data_to_save["Cellulare"]):
            QMessageBox.information(None, "Success", "Account registrato correttamente!")
        else: QMessageBox.warning(None, "Cliente esistente", "Il cliente esiste già.")
        self.go_back()

    def go_back(self):
        from viste.welcome import WelcomeWindow
        self.vista = WelcomeWindow()
        self.vista.show()
        self.close()

