from datetime import datetime

from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Attivita.pagamento import Pagamento
from Attivita.cliente import Cliente
from Attivita.prenotazione import Prenotazione
import darkdetect


class VistaPagamentiAmministratore(QMainWindow):
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

        self.title_label = QLabel("Gestione pagamenti")
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
        self.search_edit.textChanged.connect(self.search_pagamenti)
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

        self.aggiungiPagamento()

    def aggiungiPagamento(self):
        pagamenti = Pagamento().readData()
        cliente = Cliente()
        clienti = cliente.get_dati()
        prenotazione = Prenotazione()
        prenotazioni = prenotazione.readData()

        for x in pagamenti:
            info_box = QGroupBox(f"Informazioni sul pagamento {x['codice']}")
            info_box.setStyleSheet("QGroupBox{max-height: 300px;}")
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
            else:
                effettua_pagamento = QPushButton("Conferma pagamento")
                effettua_pagamento.setStyleSheet("width: 150px; max-width: 150px; background-color: #6AFE67; border-radius: 15px; color: black; ")
                effettua_pagamento.clicked.connect(lambda _, p=x: self.confermaPagamento(p))
                info_layout.addWidget(effettua_pagamento, 5, 2)

            elimina = QPushButton("Elimina")
            elimina.clicked.connect(lambda _, p=x: self.eliminaPagamento(p))
            elimina.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; "
                                  "color: black; padding: 10px;")
            info_layout.addWidget(elimina, 6, 2)
            self.scroll_layout.addWidget(info_box)

    def go_back(self):
        from viste.viste_amministratore.admin import VistaAmministrazione
        self.vista = VistaAmministrazione()
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
                                    QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pagamento.eliminaPagamento(p)
            QMessageBox.information(self, 'Disdetta Confermata', 'Il pagamento è stato eliminato con successo.', QMessageBox.Ok)

    def confermaPagamento(self, p):
        pagamento = Pagamento()
        reply = QMessageBox.question(self, 'Conferma pagamento', 'Sei sicuro di voler confermare il pagamento?',
                                     QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            pagamento.verificaPagamento(p)
            QMessageBox.information(self, 'Pagamento Confermato', 'Il pagamento è stato confermato con successo.', QMessageBox.Ok)
            self.aggiornaVista()

    def aggiornaVista(self):
        # Clear the current layout
        for i in reversed(range(self.scroll_layout.count())):
            self.scroll_layout.itemAt(i).widget().setParent(None)

        # Reload the payments
        self.aggiungiPagamento()