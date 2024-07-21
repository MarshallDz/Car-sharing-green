from PyQt5.QtGui import QIcon, QPixmap
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *

from Attivita.pagamento import Pagamento
from Attivita.prenotazione import Prenotazione
from Attivita.cliente import Cliente
import darkdetect
from datetime import datetime


class VistaGestionePrenotazione(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout()

        title_layout = QHBoxLayout()

        self.central_widget.setLayout(self.central_layout)

        back_button = QPushButton()
        back_button.setStyleSheet("max-width: 100px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/back.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        title_layout.addWidget(back_button)

        self.title_label = QLabel("Gestione prenotazioni")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        self.title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(self.title_label)

        ghost_button = QPushButton()
        ghost_button.setStyleSheet("max-width: 100px; border: none")
        title_layout.addWidget(ghost_button)

        self.central_layout.addLayout(title_layout)

        # Aggiungi la barra di ricerca in alto a destra
        self.search_layout = QHBoxLayout()
        self.search_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        search_icon = QLabel()
        icon = QPixmap("viste/Icone/varie/search.png")
        icon.setDevicePixelRatio(10)
        search_icon.setPixmap(icon)
        search_icon.setAlignment(Qt.AlignRight)
        self.search_edit = QLineEdit()
        self.search_edit.setStyleSheet("max-width: 300px; max-height: 40px; border-radius: 15px; ")
        if darkdetect.isDark():
            self.search_edit.setStyleSheet("max-width: 300px; max-height: 40px; border-radius: 15px; "
                                           "background-color: #403F3F")
        self.search_edit.setPlaceholderText("cerca per nome")
        self.search_layout.addWidget(search_icon)
        self.search_layout.addWidget(self.search_edit)
        self.search_edit.textChanged.connect(self.search_prenotazioni)
        self.central_layout.addLayout(self.search_layout)

        scroll_area = QScrollArea()
        scroll_area.setStyleSheet("QScrollBar:vertical {"
                                  "    border: none;"
                                  "    border-radius: 5px;"
                                  "    background: #272626;"
                                  "    width: 10px;"  # Imposta la larghezza della barra di scorrimento
                                  "}"
                                  "QScrollBar::handle:vertical {"
                                  "    background: white;"  # Imposta il colore del cursore
                                  "    border-radius: 5px;"
                                  "    min-height: 20px;"  # Imposta l'altezza minima del cursore
                                  "}"
                                  "QScrollBar::add-line:vertical {"
                                  "    background: none;"
                                  "}"
                                  "QScrollBar::sub-line:vertical {"
                                  "    background: none;"
                                  "}"
                                  "QScrollArea {"
                                  "border: none"
                                  "}"
                                  )

        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.central_layout.addWidget(scroll_area)

        self.aggiungi_box_info()

        aggiungiPrenotazione_button = QPushButton("Aggiungi prenotazione")
        aggiungiPrenotazione_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #6AFE67; border-radius: 15px; "
                                  "color: black; padding: 10px; margin-bottom: 20px")
        aggiungiPrenotazione_button.clicked.connect(self.go_aggiungiPrenotazione)
        self.central_layout.addWidget(aggiungiPrenotazione_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)

    def aggiungi_box_info(self):
        cliente = Cliente()
        clienti_info = cliente.get_dati()
        for client in clienti_info:
            prenotazioniCliente = cliente.get_prenotazione(client['codiceFiscale'])
            if len(prenotazioniCliente) == 0:
                continue
            else:
                for x in prenotazioniCliente:
                    info_box = QGroupBox(f"Informazioni sulla prenotazione codice {x['id']}")
                    info_box.setStyleSheet("QGroupBox{max-height: 200px;}")
                    info_layout = QGridLayout(info_box)

                    data_label = QLabel("Data prenotazione:")

                    data_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(data_label, 1, 0)

                    data_testo = str(x["data_prenotazione"])
                    formato_data_testo = "%a %b %d %Y"
                    data = datetime.strptime(data_testo, formato_data_testo)
                    self.data_edit = QDateEdit(data)
                    self.data_edit.setCalendarPopup(True)
                    self.data_edit.setEnabled(False)
                    info_layout.addWidget(self.data_edit, 1, 1)

                    mezzo_label = QLabel("Mezzo prenotato:")
                    mezzo_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(mezzo_label, 2, 0)

                    self.mezzo_edit = QLineEdit(f"{x['mezzo']['produttore']} {x['mezzo']['modello']}")
                    self.mezzo_edit.setEnabled(False)
                    info_layout.addWidget(self.mezzo_edit, 2, 1)

                    tariffa_label = QLabel("Tariffa selezionata:")
                    tariffa_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(tariffa_label, 3, 0)
                    self.tariffa_edit = QComboBox()
                    self.tariffa_edit.addItems(["oraria", "giornaliera"])
                    self.tariffa_edit.setCurrentText(str(x['tariffa']))
                    self.tariffa_edit.setEnabled(False)
                    info_layout.addWidget(self.tariffa_edit, 3, 1)

                    dataInizio_label = QLabel("Data inizio prenotazione:")
                    dataInizio_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(dataInizio_label, 1, 2)
                    self.dataInizio_edit = QLineEdit(str(x['data_inizio']))
                    self.dataInizio_edit.setEnabled(False)
                    info_layout.addWidget(self.dataInizio_edit, 1, 3)

                    dataFine_label = QLabel("Data fine prenotazione:")
                    dataFine_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(dataFine_label, 2, 2)
                    self.dataFine_edit = QLineEdit(str(x['data_fine']))
                    self.dataFine_edit.setEnabled(False)
                    info_layout.addWidget(self.dataFine_edit, 2, 3)

                    polizza_label = QLabel("Polizza selezionata:")
                    polizza_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(polizza_label, 3, 2)
                    self.polizza_edit = QComboBox()
                    self.polizza_edit.setCurrentText(str(x['polizza']))
                    self.polizza_edit.addItems(["rca", "kasko"])
                    self.polizza_edit.setEnabled(False)
                    info_layout.addWidget(self.polizza_edit, 3, 3)

                    cliente_label = QLabel("Cliente: " + x["cliente"]["nome"] + " " + x["cliente"]["cognome"])

                    cliente_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(cliente_label, 4, 0)

                    buttons_layout = QHBoxLayout()
                    info_layout.addLayout(buttons_layout, 4, 3, alignment= Qt.AlignRight)

                    if self.tariffa_edit.currentText() == "oraria" and self.dataFine_edit.text() == "da definire":
                        fine_prenotazione_button = QPushButton("Termina prenotazione")
                        fine_prenotazione_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #6AFE67; "
                                                    "border-radius: 15px; color: black; padding: 10px;")
                        fine_prenotazione_button.clicked.connect(lambda _, p=x: self.finePrenotazioneOraria(p))
                        buttons_layout.addWidget(fine_prenotazione_button)

                    modify_button = QPushButton("Modifica")
                    modify_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #D9D9D9; "
                                                "border-radius: 15px; color: black; padding: 10px;")
                    modify_button.clicked.connect(
                        lambda _, a=self.data_edit, b=self.mezzo_edit, c=self.tariffa_edit, d=self.dataInizio_edit,
                               e=self.dataFine_edit, f=self.polizza_edit, g=modify_button, nc=cliente_label.text().split()[1:3]: self.modifica_valori_lineedit(a, b, c, d, e, f, g, nc))

                    buttons_layout.addWidget(modify_button)
                    disdici = QPushButton("Disdici")
                    disdici.clicked.connect(lambda _, p=x: self.disdici(p))
                    disdici.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: "
                                          "15px; color: black; padding: 10px;")
                    buttons_layout.addWidget(disdici)

                    self.scroll_layout.addWidget(info_box)

    def go_back(self):
        from viste.viste_amministratore.admin import VistaAmministrazione
        self.vista = VistaAmministrazione()
        self.vista.show()
        self.close()

    def disdici(self, p):
        reply = QMessageBox.warning(self, 'Conferma Disdetta', 'Sei sicuro di voler disdire questa prenotazione?', QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            Prenotazione().eliminaPrenotazione(p)
            QMessageBox.information(self, 'Disdetta Confermata', 'La prenotazione è stata disdetta con successo.', QMessageBox.Ok)

    def modifica_valori_lineedit(self, data_edit, mezzo_edit, tariffa_edit, dataInizio_edit, dataFine_edit, polizza_edit, modify_button, nc):
        # bisogna aggiungere anche la modifica nel file prenotazioni.json
        if modify_button.text() == "Modifica":
            modify_button.setText("Salva")
            data_edit.setEnabled(True)
            mezzo_edit.setEnabled(True)
            tariffa_edit.setEnabled(True)
            dataInizio_edit.setEnabled(True)
            dataFine_edit.setEnabled(True)
            polizza_edit.setEnabled(True)

            # Salva i riferimenti ai campi QLineEdit
            self.modifica_data = data_edit
            self.modifica_mezzo = mezzo_edit
            self.modifica_tariffa = tariffa_edit
            self.modifica_data_inizio = dataInizio_edit
            self.modifica_data_fine = dataFine_edit
            self.modifica_polizza = polizza_edit
            self.nome_cliente = nc
        else:
            modify_button.setText("Modifica")
            data_edit.setEnabled(False)
            mezzo_edit.setEnabled(False)
            tariffa_edit.setEnabled(False)
            dataInizio_edit.setEnabled(False)
            dataFine_edit.setEnabled(False)
            polizza_edit.setEnabled(False)
            self.salva_valori()

    def go_aggiungiPrenotazione(self):
        from viste.viste_amministratore.prenotazioneAmministratore import VistaEffettuaPrenotazioneAmministratore
        self.vista = VistaEffettuaPrenotazioneAmministratore()
        self.vista.show()
        self.close()

    def search_prenotazioni(self, text):
        # Funzione per filtrare le prenotazioni in base al nome del cliente
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if isinstance(item, QLayoutItem):
                widget = item.widget()
                if isinstance(widget, QGroupBox):
                    cliente_labels = widget.findChildren(QLabel)
                    for label in cliente_labels:
                        client_name = label.text()
                        if text.lower() in client_name.lower():
                            widget.show()
                            break
                    else:
                        widget.hide()

    def salva_valori(self):
        # Estrai i valori dai campi QLineEdit e memorizzali nelle variabili di istanza
        self.valore_data = self.modifica_data.date().toString(Qt.ISODate)
        # Parse the date string
        date_obj = datetime.strptime(self.valore_data, "%Y-%m-%d")
        formatted_date = date_obj.strftime("%a %b %d %Y")
        self.valore_mezzo = self.modifica_mezzo.text()
        self.valore_tariffa = self.modifica_tariffa.currentText()
        self.valore_data_inizio = self.modifica_data_inizio.text()
        self.valore_data_fine = self.modifica_data_fine.text()
        self.valore_polizza = self.modifica_polizza.currentText()
        prenotazione = Prenotazione()
        prenotazione.aggiornaValori(self.nome_cliente, formatted_date, self.valore_polizza, self.valore_data_inizio,
                                    self.valore_data_fine, self.valore_mezzo, self.valore_tariffa)
        self.aggiorna_vista()

    def finePrenotazioneOraria(self, p):
        riconsegna = datetime.now().strftime("%Y-%m-%d %H.00")
        prenotazioni = Prenotazione().readData()
        for x in prenotazioni:
            if x["id"] == p["id"]:
                x["data_fine"] = riconsegna
                Prenotazione().writeData(prenotazioni)
                Pagamento().aggiungiPagamento("", x, x["cliente"])
        self.aggiorna_vista()

    def aggiorna_vista(self):
        # Rimuovi tutti i widget dalla scroll_layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Ora puoi chiamare nuovamente il metodo per aggiungere i widget aggiornati
        self.aggiungi_box_info()