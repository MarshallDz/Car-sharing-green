import json

import darkdetect
from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QGridLayout, \
    QComboBox, QDateEdit, QPushButton, QMessageBox

from datetime import datetime
from Attivita.cliente import Cliente
from Attivita.pagamento import Pagamento
from Attivita.prenotazione import Prenotazione


class VistaEffettuaPrenotazioneAmministratore(QMainWindow):
    def __init__(self):
        super().__init__()

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

        self.title_label = QLabel("Aggiungi prenotazione per un cliente")
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

        cliente_label = QLabel("Seleziona cliente: ")
        cliente_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(cliente_label, 0, 0)

        cliente = Cliente()
        listaClienti = cliente.get_dati()
        self.sceltaCliente = QComboBox()
        self.sceltaCliente.setPlaceholderText("Seleziona cliente")
        for c in listaClienti:
            self.sceltaCliente.addItem(c["codiceFiscale"])
        form_layout.addWidget(self.sceltaCliente, 0, 1)

        categoria_label = QLabel("Seleziona categoria mezzo:")
        categoria_label.setStyleSheet("font-size: 18px; max-width: 215px; max-height: 50px")
        form_layout.addWidget(categoria_label, 1, 0)

        self.categoriaBox = QComboBox()
        self.categoriaBox.setPlaceholderText("--Categoria--")
        self.categoriaBox.addItems(["auto", "moto", "van", "furgone"])
        form_layout.addWidget(self.categoriaBox, 1, 1)

        # Aggiungi la seconda combobox inizialmente nascosta
        self.scelta_mezzo_combobox = QComboBox()
        self.scelta_mezzo_combobox.setPlaceholderText("")
        self.scelta_mezzo_combobox.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        self.scelta_mezzo_combobox.hide()  # Nascondi la combobox inizialmente
        form_layout.addWidget(self.scelta_mezzo_combobox, 1, 2)

        # Connetti il segnale currentIndexChanged della combobox della categoria
        self.categoriaBox.currentIndexChanged.connect(self.mostra_scelta_mezzo)

        inoleggio_label = QLabel("Data inizio noleggio:")
        inoleggio_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(inoleggio_label, 2, 0)

        fnoleggio_label = QLabel("Data fine noleggio:")
        fnoleggio_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(fnoleggio_label, 3, 0)

        filiale_label = QLabel("Filiale ritiro mezzo:")
        filiale_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(filiale_label, 4, 0)

        assicurazione_label = QLabel("Polizza assicurativa:")
        assicurazione_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(assicurazione_label, 5, 0)

        tariffa_label = QLabel("Tariffa:")
        tariffa_label.setStyleSheet("font-size: 18px; max-width: 200px; max-height: 50px")
        form_layout.addWidget(tariffa_label, 6, 0)

        dlayout1 = QHBoxLayout()
        self.datacampo1 = QDateEdit()
        self.datacampo1.setCalendarPopup(True)
        self.datacampo1.lineEdit().setReadOnly(True)
        self.datacampo1.setMinimumDate(QDate.currentDate())
        self.datacampo1.setStyleSheet("max-width: 300px; max-height: 50px;")
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
        form_layout.addLayout(dlayout1, 2, 1)

        dlayout2 = QHBoxLayout()
        self.datacampo2 = QDateEdit()
        self.datacampo2.setCalendarPopup(True)
        self.datacampo2.lineEdit().setReadOnly(True)
        self.datacampo2.setMinimumDate(QDate.currentDate().addDays(1))
        self.datacampo2.setStyleSheet("max-width: 300px; max-height: 50px")
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
        self.valori["data_fine"] = self.datacampo2.date().toString(Qt.ISODate)
        form_layout.addLayout(dlayout2, 3, 1)

        self.filiale = QComboBox(self)
        self.filiale.setStyleSheet("max-width: 300px; max-height: 50px")
        self.filiale.setPlaceholderText("Scegli:")
        self.filiale.addItems(["Milano, via padova", "Milano, via roma"])
        self.filiale.currentIndexChanged.connect(self.update_valori)
        form_layout.addWidget(self.filiale, 4, 1)
        self.valori["filiale"] = self.filiale.currentText()

        self.polizza = QComboBox(self)
        self.polizza.setStyleSheet("max-width: 300px; max-height: 50px")
        self.polizza.setPlaceholderText("Scegli:")
        self.polizza.addItems(["rca", "kasko"])
        form_layout.addWidget(self.polizza, 5, 1)
        self.polizza.currentIndexChanged.connect(self.update_valori)
        self.valori["polizza"] = self.polizza.currentText()

        self.tariffa = QComboBox(self)
        self.tariffa.setStyleSheet("max-width: 300px; max-height: 50px")
        self.tariffa.setPlaceholderText("Scegli:")
        self.tariffa.addItems(["oraria", "giornaliera"])
        form_layout.addWidget(self.tariffa, 6, 1)
        self.tariffa.currentIndexChanged.connect(self.update_valori)
        self.valori["tariffa"] = self.tariffa.currentText()

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

    def update_valori(self):
        sender = self.sender()  # Identifica quale combobox ha generato il segnale

        # Aggiorna self.valori
        if sender == self.datacampo1:
            info = self.valori["data_inizio"].split(" ")
            info[0] = sender.date().toString(Qt.ISODate)
            self.valori["data_inizio"] = f"{info[0]} {info[1]}"
            new_start_date = sender.date()
            self.datacampo2.setMinimumDate(new_start_date.addDays(1))  # Imposta la data minima di campo2 al giorno successivo
            current_end_date = self.datacampo2.date()
            if current_end_date <= new_start_date:
                # Se la data di fine noleggio è minore o uguale alla data di inizio noleggio più un giorno,
                # imposta la data di fine noleggio un giorno dopo della data di inizio
                self.datacampo2.setDate(new_start_date.addDays(1))
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
            self.valori["data_fine"] = sender.date().toString(Qt.ISODate)
        elif sender == self.oracampo2:
            info = self.valori["data_fine"].split(" ")
            info[1] = sender.currentText()
            self.valori["data_fine"] = f"{info[0]} {info[1]}"
        elif sender == self.filiale:
            self.valori["filiale"] = sender.currentText()
        elif sender == self.polizza:
            self.valori["polizza"] = sender.currentText()
        elif sender == self.sceltaCliente:
            self.valori["cliente"] = sender.currentText()
        else:
            self.valori["tariffa"] = sender.currentText()
            if sender.currentText() == "giornaliera":
                self.oracampo2.setVisible(True)
                self.valori["data_fine"] = self.datacampo2.date().toString(Qt.ISODate) + " " + self.oracampo2.currentText()
            elif sender.currentText() == "oraria":
                self.oracampo2.setVisible(False)

    def go_back(self):
        from viste. viste_amministratore.gestionePrenotazioni import VistaGestionePrenotazione
        self.vista = VistaGestionePrenotazione()
        self.vista.show()
        self.close()

    def conferma_prenotazione(self):
        for value in self.valori.values():
            if not value or not self.sceltaCliente.currentText():
                QMessageBox.warning(self, "Attenzione", "Per favore compila tutti i campi.")
                return

        prenotazione = Prenotazione()
        pagamento = Pagamento()
        cliente = Cliente()
        c = self.cercaClienteByCF()
        mezzo = self.cercaMezzo()
        prenotazione.aggiungiPrenotazione(c, datetime.now().strftime("%a %b %d %Y"), self.valori["data_inizio"],
                                          self.valori["data_fine"], mezzo, self.valori["filiale"],
                                          self.valori["tariffa"], self.valori["polizza"])

        pagamento.aggiungiPagamento("", prenotazione.__dict__, c)
        cliente.set_prenotazioni_cliente(c["email"], c["password"], prenotazione.id)
        QMessageBox.information(None, "Prenotazione fatta", "Prenotazione salvata")

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

    def mostra_scelta_mezzo(self):
        # Mostra la seconda combobox solo se è stata selezionata una categoria valida
        self.scelta_mezzo_combobox.clear()  # Pulisci la combobox
        # Popola la seconda combobox in base alla categoria selezionata
        if self.categoriaBox.currentText() == "auto":
            from Servizio.auto import Auto
            lista_auto = Auto().get_dati()
            for auto in lista_auto:
                self.scelta_mezzo_combobox.addItem(auto["produttore"] + " " + auto["modello"])
        elif self.categoriaBox.currentText() == "moto":
            from Servizio.moto import Moto
            lista_moto = Moto().get_dati()
            for moto in lista_moto:
                self.scelta_mezzo_combobox.addItem(moto["produttore"] + " " + moto["modello"])
        elif self.categoriaBox.currentText() == "van":
            from Servizio.van import Van
            lista_van = Van().get_dati()
            for van in lista_van:
                self.scelta_mezzo_combobox.addItem(van["produttore"] + " " + van["modello"])
        else:
            from Servizio.furgone import Furgone
            lista_f = Furgone().get_dati()
            for f in lista_f:
                self.scelta_mezzo_combobox.addItem(f["produttore"] + " " + f["modello"])
        self.scelta_mezzo_combobox.show()
        self.valori["mezzo"] = self.scelta_mezzo_combobox.currentText()

    def cercaClienteByCF(self):
        with open("dati/clienti.json") as f:
            data = json.load(f)
            clienti = data.get("clienti", [])
            for i in clienti:
                if self.sceltaCliente.currentText() == i["codiceFiscale"] :
                    return i

    def cercaMezzo(self):
        if self.categoriaBox.currentText() == "auto":
            with open("dati/auto.json") as f:
                data = json.load(f)
                for i in data:
                    if self.scelta_mezzo_combobox.currentText() == i["produttore"] + " " + i["modello"]:
                        return i
        elif self.categoriaBox.currentText() == "moto":
            with open("dati/moto.json") as f:
                data = json.load(f)
                for i in data:
                    if self.scelta_mezzo_combobox.currentText() == i["produttore"] + " " + i["modello"]:
                        return i
        elif self.categoriaBox.currentText() == "van":
            with open("dati/van.json") as f:
                data = json.load(f)
                for i in data:
                    if self.scelta_mezzo_combobox.currentText() == i["produttore"] + " " + i["modello"]:
                        return i
        else:
            with open("dati/furgoni.json") as f:
                data = json.load(f)
                for i in data:
                    if self.scelta_mezzo_combobox.currentText() == i["produttore"] + " " + i["modello"]:
                        return i
