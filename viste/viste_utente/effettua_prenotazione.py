from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from Attivita.cliente import *
from Attivita.prenotazione import *
from viste.viste_utente.confermaPrenotazione import VistaConfermaPrenotazione
from Attivita.pagamento import *
import darkdetect


class VistaEffettuaPrenotazione(QMainWindow):
    def __init__(self, cliente, mezzo):
        super().__init__()
        self.cliente = cliente
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

        self.page_layout = QVBoxLayout()
        self.central_widget.setLayout(self.page_layout)

        self.title_label = QLabel("Effettua la tua prenotazione ")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.setStyleSheet("max-height: 100px")
        self.title_label.setAlignment(Qt.AlignHCenter)
        self.title_label.adjustSize()
        self.page_layout.addWidget(self.title_label)

        self.valori = {}

        self.central_layout = QHBoxLayout()
        form_layout = QGridLayout()
        form_layout.setHorizontalSpacing(200)
        buttons_layout = QVBoxLayout()

        filiale_label = QLabel("Filiale ritiro mezzo:")
        filiale_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(filiale_label, 0, 0)

        assicurazione_label = QLabel("Polizza assicurativa:")
        assicurazione_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(assicurazione_label, 1, 0)

        tariffa_label = QLabel("Tariffa:")
        tariffa_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(tariffa_label, 2, 0)

        inoleggio_label = QLabel("Data inizio noleggio:")
        inoleggio_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(inoleggio_label, 3, 0)

        fnoleggio_label = QLabel("Data fine noleggio:")
        fnoleggio_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(fnoleggio_label, 4, 0)

        self.filiale = QComboBox(self)
        self.filiale.setStyleSheet("max-width: 300px; max-height: 50px")
        self.filiale.setPlaceholderText("Scegli:")
        self.filiale.addItems(["Milano, via padova", "Milano, via roma"])
        self.filiale.currentIndexChanged.connect(self.update_valori)
        form_layout.addWidget(self.filiale, 0, 1)
        self.valori["filiale"] = self.filiale.currentText()

        self.polizza = QComboBox(self)
        self.polizza.setStyleSheet("max-width: 300px; max-height: 50px")
        self.polizza.setPlaceholderText("Scegli:")
        self.polizza.addItems(["rca", "kasko"])
        form_layout.addWidget(self.polizza, 1, 1)
        self.polizza.currentIndexChanged.connect(self.update_valori)
        self.valori["polizza"] = self.polizza.currentText()

        self.tariffa = QComboBox(self)
        self.tariffa.setStyleSheet("max-width: 300px; max-height: 50px")
        self.tariffa.setPlaceholderText("Scegli:")
        self.tariffa.addItems(["oraria", "giornaliera"])
        form_layout.addWidget(self.tariffa, 2, 1)
        self.tariffa.currentIndexChanged.connect(self.update_valori)
        self.valori["tariffa"] = self.tariffa.currentText()

        dlayout1 = QHBoxLayout()
        self.datacampo1 = QDateEdit()
        self.datacampo1.setCalendarPopup(True)
        self.datacampo1.lineEdit().setReadOnly(True)
        self.datacampo1.setMinimumDate(QDate.currentDate())
        dlayout1.addWidget(self.datacampo1)
        self.datacampo1.dateChanged.connect(self.update_valori)

        self.oracampo1 = QComboBox(self)
        if self.verifica_data_corrente():
            for i in range(self.ora_corrente(), 21):
                if 8 <= i <= 9:
                    self.oracampo1.addItems([f"0{i}.00"])
                else:
                    self.oracampo1.addItems([f"{i}.00"])
        dlayout1.addWidget(self.oracampo1)
        self.oracampo1.currentIndexChanged.connect(self.update_valori)
        self.valori["data_inizio"] = self.datacampo1.date().toString(Qt.ISODate) + " " + self.oracampo1.currentText()
        form_layout.addLayout(dlayout1, 3, 1)

        dlayout2 = QHBoxLayout()
        self.datacampo2 = QDateEdit()
        self.datacampo2.setCalendarPopup(True)
        self.datacampo2.lineEdit().setReadOnly(True)
        self.datacampo2.setMinimumDate(QDate.currentDate().addDays(1))
        dlayout2.addWidget(self.datacampo2)
        self.datacampo2.dateChanged.connect(self.update_valori)

        self.oracampo2 = QComboBox(self)
        for i in range(8, 21):
            if i <= 9:
                self.oracampo2.addItems([f"0{i}.00"])
            else:
                self.oracampo2.addItems([f"{i}.00"])
        dlayout2.addWidget(self.oracampo2)
        self.oracampo2.currentIndexChanged.connect(self.update_valori)
        self.valori["data_fine"] = self.datacampo2.date().toString(Qt.ISODate) + " " + self.oracampo2.currentText()
        form_layout.addLayout(dlayout2, 4, 1)

        self.central_layout.addLayout(form_layout)

        conferma_button = QPushButton("Conferma")
        conferma_button.setStyleSheet(
            "max-width: 200px; max-height: 50px; background-color: #6AFE67; border-radius: 15px; color: black; "
            "padding: 10px")
        conferma_button.clicked.connect(self.conferma_prenotazione)
        buttons_layout.addWidget(conferma_button)

        back_button = QPushButton("Annulla")
        back_button.setStyleSheet(
            "max-width: 150px; max-height: 30px; background-color: #F85959; border-radius: 15px; color: black; "
            "padding: 10px")
        back_button.clicked.connect(self.go_back)
        buttons_layout.addWidget(back_button)

        self.central_layout.addLayout(buttons_layout)

        self.page_layout.addLayout(self.central_layout)

        bottom_layout = QHBoxLayout()

        image = QPixmap(mezzo["immagine"])
        self.label = QLabel()
        self.label.setStyleSheet("margin-left: 20px")
        self.label.setPixmap(image.scaled(600, 800, Qt.KeepAspectRatio))
        self.label.setAlignment(Qt.AlignCenter)
        bottom_layout.addWidget(self.label)

        self.alt = QLabel("La tua scelta: \n\n" + mezzo["produttore"] + " " + mezzo["modello"] + " " + mezzo["cavalli"] + " cv")
        self.alt.setStyleSheet("font-size: 25px")
        bottom_layout.addWidget(self.alt)

        self.page_layout.addLayout(bottom_layout)

    def update_valori(self):
        sender = self.sender()  # Identifica quale widget ha generato il segnale

        if sender == self.datacampo1:
            info = self.valori["data_inizio"].split(" ")
            info[0] = sender.date().toString(Qt.ISODate)
            self.valori["data_inizio"] = f"{info[0]} {info[1]}"
            new_start_date = sender.date()
            self.datacampo2.setMinimumDate(new_start_date)
            current_end_date = self.datacampo2.date()
            if current_end_date <= new_start_date:
                self.datacampo2.setDate(new_start_date)

            # Ripopola oracampo1
            if not self.verifica_data_corrente():
                self.oracampo1.clear()
                for i in range(8, 21):
                    if i <= 9:
                        self.oracampo1.addItems([f"0{i}.00"])
                    else:
                        self.oracampo1.addItems([f"{i}.00"])

        elif sender == self.oracampo1:
            info = self.valori["data_inizio"].split(" ")
            info[1] = sender.currentText()
            self.valori["data_inizio"] = f"{info[0]} {info[1]}"

        elif sender == self.datacampo2:
            if self.tariffa == "giornaliera":
                self.valori["data_fine"] = sender.date().toString(Qt.ISODate)
            else:
                self.valori["data_fine"] = sender.date().toString(Qt.ISODate) + " " + self.oracampo2.currentText()
                info = self.valori["data_fine"].split(" ")
                info[0] = sender.date().toString(Qt.ISODate)
                self.valori["data_fine"] = f"{info[0]} {info[1]}"

        elif sender == self.oracampo2:
            info = self.valori["data_fine"].split(" ")
            info[1] = sender.currentText()
            self.valori["data_fine"] = f"{info[0]} {info[1]}"

        elif sender == self.filiale:
            self.valori["filiale"] = sender.currentText()

        elif sender == self.polizza:
            self.valori["polizza"] = sender.currentText()

        elif sender == self.tariffa:
            self.valori["tariffa"] = sender.currentText()
            if sender.currentText() == "oraria":
                self.oracampo2.setVisible(True)
                self.valori["data_fine"] = self.datacampo2.date().toString(Qt.ISODate) + " " + self.oracampo2.currentText()
            elif sender.currentText() == "giornaliera":
                self.oracampo2.setVisible(False)
                info = self.valori["data_fine"].split()
                self.valori["data_fine"] = info[0]

    def go_back(self):
        from viste.viste_utente.vistaPrenotazione import VistaPrenotazione
        self.vista = VistaPrenotazione(self.cliente)
        self.vista.show()
        self.close()

    def conferma_prenotazione(self):
        for value in self.valori.values():
            if not value:
                QMessageBox.warning(self, "Attenzione", "Per favore compila tutti i campi.")
                return

        prenotazione = Prenotazione()
        pagamento = Pagamento()
        c = Cliente()
        v, dI, dF = prenotazione.controllo_assegnamento_mezzo(self.mezzo, self.valori["data_inizio"], self.valori["data_fine"])
        if v:
            prenotazione.aggiungiPrenotazione(self.cliente, datetime.now().strftime("%a %b %d %Y"), self.valori["data_inizio"],
                                              self.valori["data_fine"], self.mezzo, self.valori["filiale"],
                                              self.valori["tariffa"], self.valori["polizza"])
    
            pagamento.aggiungiPagamento("", prenotazione.__dict__, self.cliente)
            c.set_prenotazioni_cliente(self.cliente, prenotazione.id)
            self.vistaPrenotazione = VistaConfermaPrenotazione(self.cliente, QDate.currentDate().toString(), self.mezzo,
                                                               self.valori["data_inizio"], self.valori["data_fine"], self.valori["tariffa"],
                                                               self.valori["polizza"])
            self.vistaPrenotazione.show()
            self.close()
        else:
            QMessageBox.warning(self, "prenotazione", f"Il mezzo è già stato prenotato da {dI} a {dF}")

    def ora_corrente(self):
        now = datetime.now()
        ora = now.hour + 1
        if ora >= 24:
            ora -= 24
        return ora

    def verifica_data_corrente(self):
        data_inserita = self.datacampo1.date().toString(Qt.ISODate)
        data_corrente = QDate.currentDate().toString(Qt.ISODate)
        return data_inserita == data_corrente
