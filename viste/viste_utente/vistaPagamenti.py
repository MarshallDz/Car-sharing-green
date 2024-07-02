from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Attivita.pagamento import Pagamento
from Attivita.cliente import Cliente
from Attivita.prenotazione import Prenotazione
import darkdetect


class VistaPagamenti(QMainWindow):
    def __init__(self, cliente):
        super().__init__()
        self.cliente = cliente
        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        page_layout = QVBoxLayout()
        button_layout = QVBoxLayout()

        title_layout = QHBoxLayout()
        back_button = QPushButton()
        back_button.setStyleSheet("max-width: 100px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/back.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        title_layout.addWidget(back_button)

        self.title_label = QLabel("I tuoi pagamenti")
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

        page_layout.addLayout(title_layout)
        page_layout.addLayout(button_layout)

        self.central_widget.setLayout(page_layout)

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

        page_layout.addWidget(scroll_area)

        self.aggiungiPagamento()

    def aggiungiPagamento(self):
        pagamenti = Pagamento().readData()
        prenotazioni = Prenotazione().readData()

        for x in pagamenti:
            if self.cliente['codiceFiscale'] == x['cliente']:
                info_box = QGroupBox(f"Informazioni sul pagamento {x['codice']}")
                info_box.setStyleSheet("QGroupBox{max-height: 250px;}")
                info_layout = QGridLayout(info_box)

                prenotazione = QLabel(f"Prenotazione: {x['prenotazione']} ")
                prenotazione.setStyleSheet("font-size: 24px; ")
                info_layout.addWidget(prenotazione, 1, 0)

                infoCliente = QLabel(f"Cliente: {self.cliente['nome']} {self.cliente['cognome']} ")
                infoCliente.setStyleSheet("font-size: 24px; ")
                info_layout.addWidget(infoCliente)
                if x['prenotazione'] in self.cliente['prenotazioni']:
                    for s in prenotazioni:
                        if x['prenotazione'] == s['id']:
                            mezzoPrenotato = QLabel(f"Mezzo prenotato: {s['mezzo']['produttore']} {s['mezzo']['modello']}")
                            mezzoPrenotato.setStyleSheet("font-size: 24px; ")
                            info_layout.addWidget(mezzoPrenotato)
                infoTotale = QLabel(f"Totale da pagare: {x['totale']} €")
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
        from viste.viste_utente.home import VistaHome
        self.vista = VistaHome(self.cliente)
        self.vista.show()
        self.close()
