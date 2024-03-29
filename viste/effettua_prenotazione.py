import datetime
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate, QDateTime
from Attivita.cliente import *
from Attivita.prenotazione import *
from viste.confermaPrenotazione import VistaConfermaPrenotazione
from Attivita.pagamento import *
import darkdetect


class VistaEffettuaPrenotazione(QMainWindow):
    def __init__(self, user, psw, mezzo):
        super().__init__()
        self.user = user
        self.psw = psw
        self.mezzo = mezzo

        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
            self.central_widget.setStyleSheet("QComboBox{"
                                              "background-color: #303030;"
                                              "}")

        self.central_layout = QGridLayout()

        self.central_layout.setContentsMargins(20, 0, 20, 0)
        self.central_layout.setVerticalSpacing(int(self.width() * 0.04))
        self.central_widget.setLayout(self.central_layout)

        self.title_label = QLabel("Effettua la tua prenotazione ")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.title_label.adjustSize()
        self.central_layout.addWidget(self.title_label, 0, 1, 2, 3)

        self.valori = {}

        inizio_noleggio = QLabel("Data inizio noleggio:")
        inizio_noleggio.setStyleSheet("font-size: 18px")
        self.central_layout.addWidget(inizio_noleggio, 1, 0, alignment=Qt.AlignTop)

        self.campo1 = QDateEdit()
        self.campo1.setCalendarPopup(True)
        self.campo1.lineEdit().setReadOnly(True)
        self.campo1.setMinimumDate(QDate.currentDate())
        self.campo1.setStyleSheet(f"max-width: {self.width() * 0.45}; min-width: {self.width() * 0.45}")
        self.central_layout.addWidget(self.campo1, 1, 3)
        self.campo1.dateChanged.connect(self.update_valori)

        self.oraCampo1 = QComboBox(self)
        if self.verifica_data_corrente():
            for i in range(self.ora_corrente(), 21):
                    if 8 <= i <= 9:
                        self.oraCampo1.addItems([f"0{i}.00"])
                    else:
                        self.oraCampo1.addItems([f"{i}.00"])
        self.central_layout.addWidget(self.oraCampo1, 1, 4)
        self.oraCampo1.currentIndexChanged.connect(self.update_valori)
        self.valori["data_inizio"] = self.campo1.date().toString(Qt.ISODate) + " " + self.oraCampo1.currentText()

        fine_noleggio = QLabel("Data fine noleggio:")
        fine_noleggio.setStyleSheet("font-size: 18px")
        self.central_layout.addWidget(fine_noleggio, 2, 0, alignment=Qt.AlignTop)

        self.campo2 = QDateEdit()
        self.campo2.setCalendarPopup(True)
        self.campo2.lineEdit().setReadOnly(True)
        self.campo2.setMinimumDate(QDate.currentDate().addDays(1))
        self.campo2.setStyleSheet(f"max-width: {self.width() * 0.45}; min-width: {self.width() * 0.45};"
                                  "margin-right: 15px")
        self.central_layout.addWidget(self.campo2, 2, 3)
        self.campo2.dateChanged.connect(self.update_valori)

        self.oraCampo2 = QComboBox(self)
        for i in range(8, 21):
            if i <= 9:
                self.oraCampo2.addItems([f"0{i}.00"])
            else:
                self.oraCampo2.addItems([f"{i}.00"])
        self.central_layout.addWidget(self.oraCampo2, 2, 4)
        self.oraCampo2.setVisible(False)
        self.oraCampo2.currentIndexChanged.connect(self.update_valori)
        self.valori["data_fine"] = self.campo2.date().toString(Qt.ISODate)

        filiale_label = QLabel("Filiale ritiro mezzo:")
        filiale_label.setStyleSheet("font-size: 18px")
        self.central_layout.addWidget(filiale_label, 3, 0)

        self.filiale = QComboBox(self)
        self.filiale.setStyleSheet("margin-right: 15px;"
                                   f"max-width: {self.width() * 0.45}; min-width: {self.width() * 0.45}")
        self.filiale.setPlaceholderText("Scegli:")
        self.filiale.addItems(["Milano, via padova", "Milano, via roma"])
        self.filiale.currentIndexChanged.connect(self.update_valori)
        self.central_layout.addWidget(self.filiale, 3, 3)
        self.valori["filiale"] = self.filiale.currentText()

        assicurazione_label = QLabel("Polizza assicurativa:")
        assicurazione_label.setStyleSheet("font-size: 18px")
        self.central_layout.addWidget(assicurazione_label, 4, 0)

        self.polizza = QComboBox(self)
        self.polizza.setStyleSheet("margin-right: 15px;"
                                   f"max-width: {self.width() * 0.45}; min-width: {self.width() * 0.45}")
        self.polizza.setPlaceholderText("Scegli:")
        self.polizza.addItems(["rca", "kasko"])
        self.central_layout.addWidget(self.polizza, 4, 3)
        self.polizza.currentIndexChanged.connect(self.update_valori)
        self.valori["polizza"] = self.polizza.currentText()

        tariffa = QLabel("Tariffa:")
        tariffa.setStyleSheet(f"font-size: 18px;")
        self.central_layout.addWidget(tariffa, 5, 0)

        self.tariffa = QComboBox(self)
        self.tariffa.setStyleSheet("margin-right: 15px;"
                                   f"max-width: {self.width() * 0.45}; min-width: {self.width() * 0.45}")
        self.tariffa.setPlaceholderText("Scegli:")
        self.tariffa.addItems(["oraria", "giornaliera"])
        self.central_layout.addWidget(self.tariffa, 5, 3)
        self.tariffa.currentIndexChanged.connect(self.update_valori)
        self.valori["tariffa"] = self.tariffa.currentText()

        conferma_button = QPushButton("Conferma")
        conferma_button.setStyleSheet(
            "width: 200px; max-width: 200px; background-color: #6AFE67; border-radius: 15px; color: black; "
            "padding: 10px; margin-right: 40px;")
        conferma_button.clicked.connect(self.conferma_prenotazione)
        self.central_layout.addWidget(conferma_button, 6, 3, alignment=Qt.AlignRight)

        back_button = QPushButton("Annulla")
        back_button.setStyleSheet(
            "width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; "
            "padding: 10px; margin-right: 50px")
        back_button.clicked.connect(self.go_back)
        self.central_layout.addWidget(back_button, 7, 3, alignment=(Qt.AlignRight | Qt.AlignTop))

    def update_valori(self):
        sender = self.sender()  # Identifica quale combobox ha generato il segnale

        # Aggiorna self.valori
        if sender == self.campo1:
            info = self.valori["data_inizio"].split(" ")
            info[0] = sender.date().toString(Qt.ISODate)
            self.valori["data_inizio"] = f"{info[0]} {info[1]}"
            new_start_date = sender.date()
            self.campo2.setMinimumDate(new_start_date.addDays(1))  # Imposta la data minima di campo2 al giorno successivo
            current_end_date = self.campo2.date()
            if current_end_date <= new_start_date:
                # Se la data di fine noleggio è minore o uguale alla data di inizio noleggio più un giorno,
                # imposta la data di fine noleggio un giorno dopo della data di inizio
                self.campo2.setDate(new_start_date.addDays(1))
            if not self.verifica_data_corrente():
                self.oraCampo1.clear()
                for i in range(8, 21):
                    if i <= 9:
                        self.oraCampo1.addItems([f"0{i}.00"])
                    else:
                        self.oraCampo1.addItems([f"{i}.00"])
        elif sender == self.oraCampo1:
            info = self.valori["data_inizio"].split(" ")
            info[1] = sender.currentText()
            self.valori["data_inizio"] = f"{info[0]} {info[1]}"
        elif sender == self.campo2:
            self.valori["data_fine"] = sender.date().toString(Qt.ISODate)
        elif sender == self.oraCampo2:
            info = self.valori["data_fine"].split(" ")
            info[1] = sender.currentText()
            self.valori["data_fine"] = f"{info[0]} {info[1]}"
        elif sender == self.filiale:
            self.valori["filiale"] = sender.currentText()
        elif sender == self.polizza:
            self.valori["polizza"] = sender.currentText()
        else:
            self.valori["tariffa"] = sender.currentText()
            if sender.currentText() == "giornaliera":
                self.oraCampo2.setVisible(True)
                self.valori["data_fine"] = self.campo2.date().toString(Qt.ISODate) + " " + self.oraCampo2.currentText()
            elif sender.currentText() == "oraria":
                self.oraCampo2.setVisible(False)

    def go_back(self):
        from viste.prenotazione import VistaPrenotazione
        self.vista = VistaPrenotazione(self.user, self.psw)
        self.vista.show()
        self.close()

    def conferma_prenotazione(self):
        for value in self.valori.values():
            if not value:
                QMessageBox.warning(self, "Attenzione", "Per favore compila tutti i campi.")
                return

        cliente = Cliente.get_dati(self, self.user, self.psw)
        prenotazione = Prenotazione()
        pagamento = Pagamento()
        c = Cliente()
        prenotazione.aggiungiPrenotazione(cliente, QDate.currentDate().toString(), self.valori["data_inizio"],
                                          self.valori["data_fine"], self.mezzo, self.valori["filiale"],
                                          self.valori["tariffa"], self.valori["polizza"])

        pagamento.aggiungiPagamento("", prenotazione.__dict__, cliente)
        c.set_prenotazioni_cliente(self.user, self.psw, prenotazione.id)
        self.vistaPrenotazione = VistaConfermaPrenotazione(self.user, self.psw, QDate.currentDate().toString(), self.mezzo,
                                                           self.valori["data_inizio"], self.valori["data_fine"], self.valori["tariffa"],
                                                           self.valori["polizza"])
        self.vistaPrenotazione.show()
        self.close()

    def ora_corrente(self):
        now = datetime.now()
        ora = now.hour + 1
        if ora >= 24:
            ora -= 24
        return ora

    def verifica_data_corrente(self):
        data_inserita = self.campo1.date().toString(Qt.ISODate)
        data_corrente = QDate.currentDate().toString(Qt.ISODate)
        return data_inserita == data_corrente
