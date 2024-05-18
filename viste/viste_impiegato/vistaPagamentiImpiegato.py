from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Attivita.pagamento import Pagamento
from Attivita.cliente import Cliente
from Attivita.prenotazione import Prenotazione
import darkdetect


class VistaPagamentiImpiegato(QMainWindow):
    def __init__(self, user, psw):
        super().__init__()
        self.user = user
        self.psw = psw
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

        self.title_label = QLabel("Lista dei pagamenti")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)
        # Aggiungi la barra di ricerca in alto a destra
        self.search_layout = QHBoxLayout()
        self.search_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)

        self.search_label = QLabel("Cerca per nome cliente:")
        self.search_layout.addWidget(self.search_label)

        self.search_edit = QLineEdit()
        self.search_edit.setPlaceholderText("Inserisci il nome del cliente")
        self.search_layout.addWidget(self.search_edit)

        self.search_edit.textChanged.connect(self.search_pagamenti)

        central_layout.addLayout(self.search_layout)
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
                                  "}")

        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        central_layout.addWidget(scroll_area)

        self.aggiungiPagamento()

        back_button = QPushButton("Indietro")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; "
                                  "padding: 10px; margin-bottom: 20px")
        central_layout.addWidget(back_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)

    def aggiungiPagamento(self):
        pagamenti = Pagamento().get_dati()
        cliente = Cliente()
        clienti = cliente.get_dati()
        prenotazione = Prenotazione()
        prenotazioni = prenotazione.get_dati()

        for x in pagamenti:
            info_box = QGroupBox(f"Informazioni sul pagamento {x['codice']}")
            info_box.setStyleSheet("QGroupBox{max-height: 250px;}")
            info_layout = QGridLayout(info_box)

            prenotazione = QLabel(f"Prenotazione: {x['prenotazione']} ")
            prenotazione.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(prenotazione, 1, 0)

            for i in clienti:
                if i["codiceFiscale"] == x["cliente"]:
                    infoCliente = QLabel(f"Cliente: {i['nome']} {i['cognome']} ")
                    infoCliente.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(infoCliente)
                if x['prenotazione'] in i['prenotazioni']:
                    for s in prenotazioni:
                        if x['prenotazione'] == s['id']:
                            mezzoPrenotato = QLabel(f"Mezzo prenotato: {s['mezzo']['produttore']} {s['mezzo']['modello']}")
                            mezzoPrenotato.setStyleSheet("font-size: 24px; ")
                            info_layout.addWidget(mezzoPrenotato)
            infoTotale = QLabel(f"Totale da pagare: {x['totale']} ")
            infoTotale.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(infoTotale)

            statoPagamento = QLabel(f"Stato pagamento: {x['statoPagamento']} ")
            statoPagamento.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(statoPagamento)
            if x['statoPagamento'] == 'pagato':
                dataPagamento = QLabel(f"data pagamento: {x['dataPagamento']} ")
                dataPagamento.setStyleSheet("font-size: 24px; ")
                info_layout.addWidget(dataPagamento)
            elimina = QPushButton("Elimina")
            elimina.clicked.connect(lambda _, p=x["codice"]: self.eliminaPagamento(p))
            elimina.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; "
                                  "padding: 10px;")
            info_layout.addWidget(elimina, 6, 2)
            self.scroll_layout.addWidget(info_box,)

    def go_back(self):
        from viste.viste_impiegato.pannelloControllo import VistaPannelloControllo
        self.vista = VistaPannelloControllo(self.user, self.psw)
        self.vista.show()
        self.close()

    def search_pagamenti(self, text):
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

    def eliminaPagamento(self, p):
        pagamento = Pagamento()
        reply = QMessageBox.warning(self, 'Conferma eliminazione', 'Sei sicuro di voler eliminare il pagamento?',
                                    QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pagamento.eliminaPagamento(p, self.user, self.psw)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, 'Disdetta Confermata', 'Il pagamento è stato eliminato con successo.', QMessageBox.Ok)
        self.go_back()
