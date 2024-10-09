import darkdetect
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QHBoxLayout, \
    QLineEdit, QMessageBox
from Noleggio.auto import Auto
from Noleggio.furgone import Furgone
from Noleggio.moto import Moto
from Noleggio.van import Van


class VistaAggiungiMezzo(QMainWindow):
    def __init__(self, t):
        super().__init__()

        # dizionario in cui salvi i campi del form
        self.campi = {}
        self.tipo = t.lower()

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

        self.title_label = QLabel("Aggiungi " + self.tipo)
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)

        # layout di tutto il form
        self.form_layout = QVBoxLayout()
        self.form_layout.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.crea_campo("URL Immagine")
        self.crea_campo("Telaio")
        self.crea_campo("Produttore")
        self.crea_campo("Modello")
        self.crea_campo("Cavalli")
        self.crea_campo("Cilindrata")
        self.crea_campo("Anno")
        self.crea_campo("Alimentazione")
        self.crea_campo("Cambio")
        self.crea_campo("Numero di posti")
        self.crea_campo("Tariffa oraria")

        # creo i bottoni invia e indietro
        invia_button = QPushButton("Invia")
        invia_button.setStyleSheet(
            "max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 35px; margin-top: 50px;")
        back_button = QPushButton("Annulla")
        back_button.setStyleSheet(
            "max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-left: 60px;")
        invia_button.clicked.connect(self.invio_dati)
        back_button.clicked.connect(self.go_back)
        self.form_layout.addWidget(invia_button)
        self.form_layout.addWidget(back_button)

        central_layout.addLayout(self.form_layout)

    def crea_campo(self, nome):
        campo = QLineEdit()
        campo.setPlaceholderText(nome)
        if nome == "URL Immagine":
            campo.setText(f"viste/Icone/{self.tipo}/")
        campo.setStyleSheet("max-width: 300px; min-height: 40px; border-radius: 15px;")
        if darkdetect.isDark():
            campo.setStyleSheet("max-width: 300px; min-height: 40px; border-radius: 15px; "
                                "background-color: #403f3f")
        self.form_layout.addWidget(campo)

        self.campi[nome] = campo

    def invio_dati(self):
        data_to_save = {}

        # estraggo i dati dai campi
        for campo_nome, campo_widget in self.campi.items():
            data_to_save[campo_nome] = campo_widget.text()
            if data_to_save[campo_nome] == "":
                QMessageBox.critical(None, "Campi mancanti", "Tutti i campi devono essere compilati.")
                return
        if self.tipo == "auto":
            mezzo = Auto()
            mezzo.aggiungiAuto(data_to_save["URL Immagine"], data_to_save["Telaio"], data_to_save["Produttore"], data_to_save["Modello"], data_to_save["Cavalli"], data_to_save["Cilindrata"], data_to_save["Anno"], data_to_save["Alimentazione"], data_to_save["Cambio"], data_to_save["Numero di posti"], data_to_save["Tariffa oraria"])
        if self.tipo == "moto":
            mezzo = Moto()
            mezzo.aggiungiMoto(data_to_save["URL Immagine"], data_to_save["Telaio"], data_to_save["Produttore"], data_to_save["Modello"], data_to_save["Cavalli"], data_to_save["Cilindrata"], data_to_save["Anno"], data_to_save["Alimentazione"], data_to_save["Cambio"], data_to_save["Numero di posti"], data_to_save["Tariffa oraria"])
        if self.tipo == "van":
            mezzo = Van()
            mezzo.aggiungiVan(data_to_save["URL Immagine"], data_to_save["Telaio"], data_to_save["Produttore"], data_to_save["Modello"], data_to_save["Cavalli"], data_to_save["Cilindrata"], data_to_save["Anno"], data_to_save["Alimentazione"], data_to_save["Cambio"], data_to_save["Numero di posti"], data_to_save["Tariffa oraria"])
        if self.tipo == "furgone":
            mezzo = Furgone()
            mezzo.aggiungiFurgone(data_to_save["URL Immagine"], data_to_save["Telaio"], data_to_save["Produttore"], data_to_save["Modello"], data_to_save["Cavalli"], data_to_save["Cilindrata"], data_to_save["Anno"], data_to_save["Alimentazione"], data_to_save["Cambio"], data_to_save["Numero di posti"], data_to_save["Tariffa oraria"])
        self.go_back()

    def go_back(self):
        from viste.viste_amministratore.gestioneMezzi import VistaMezziAmministratore
        self.vista = VistaMezziAmministratore()
        self.vista.show()
        self.close()
