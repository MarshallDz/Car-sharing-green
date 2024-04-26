from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Attivita.pagamento import Pagamento
from Attivita.cliente import Cliente
from Attivita.prenotazione import Prenotazione
import darkdetect


class VistaPagamenti(QMainWindow):
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

        self.title_label = QLabel("Lista dei tuoi pagamenti")
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        central_layout.addLayout(title_layout)

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
        clienteCorrente = cliente.get_dati(self.user, self.psw)
        prenotazione = Prenotazione()
        prenotazioni = prenotazione.get_dati()

        for x in pagamenti:
            if clienteCorrente['codiceFiscale'] == x['cliente']:
                info_box = QGroupBox(f"Informazioni sul pagamento {x['codice']}")
                info_box.setStyleSheet("QGroupBox{max-height: 250px;}")
                info_layout = QGridLayout(info_box)

                prenotazione = QLabel(f"Prenotazione: {x['prenotazione']} ")
                prenotazione.setStyleSheet("font-size: 24px; ")
                info_layout.addWidget(prenotazione, 1, 0)

                infoCliente = QLabel(f"Cliente: {clienteCorrente['nome']} {clienteCorrente['cognome']} ")
                infoCliente.setStyleSheet("font-size: 24px; ")
                info_layout.addWidget(infoCliente)
                if x['prenotazione'] in clienteCorrente['prenotazioni']:
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
                self.scroll_layout.addWidget(info_box)

    def go_back(self):
        from viste.home import VistaHome
        self.vista = VistaHome(self.user, self.psw)
        self.vista.show()
        self.close()
