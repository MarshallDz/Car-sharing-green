from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from Attivita.prenotazione import Prenotazione
from Attivita.cliente import Cliente
import darkdetect
from datetime import datetime
class VistaGestionePrenotazione(QMainWindow):
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

        self.central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(self.central_layout)

        self.title_label = QLabel("Gestisci prenotazioni")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        self.central_layout.addLayout(title_layout)

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

        self.central_layout.addWidget(scroll_area)

        self.aggiungi_box_info()
        aggiungiPrenotazione_button = QPushButton("Aggiungi prenotazione")
        aggiungiPrenotazione_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #6AFE67; border-radius: 15px; "
                                  "color: black; padding: 10px; margin-bottom: 20px")
        #aggiungiPrenotazione_button.clicked.connect()
        self.central_layout.addWidget(aggiungiPrenotazione_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        back_button = QPushButton("Indietro")
        back_button.clicked.connect(self.go_back)
        back_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; "
                                  "color: black; padding: 10px; margin-bottom: 20px")
        self.central_layout.addWidget(back_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)

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
                    data_edit = QDateEdit(data)
                    data_edit.setCalendarPopup(True)
                    data_edit.setEnabled(False)

                    info_layout.addWidget(data_edit, 1, 1)

                    mezzo_label = QLabel("Mezzo prenotato:")
                    mezzo_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(mezzo_label, 2, 0)
                    mezzo_edit = QLineEdit(f"{x['mezzo']['produttore']} {x['mezzo']['modello']}")
                    mezzo_edit.setEnabled(False)
                    info_layout.addWidget(mezzo_edit, 2, 1)

                    tariffa_label = QLabel("Tariffa selezionata:")
                    tariffa_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(tariffa_label, 3, 0)
                    tariffa_edit = QComboBox()
                    tariffa_edit.addItems(["oraria", "giornaliera"])
                    tariffa_edit.setCurrentText(str(x['tariffa']))
                    tariffa_edit.setEnabled(False)
                    info_layout.addWidget(tariffa_edit, 3, 1)

                    dataInizio_label = QLabel("Data inizio prenotazione:")
                    dataInizio_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(dataInizio_label, 1, 2)
                    dataInizio_edit = QLineEdit(str(x['data_inizio']))
                    dataInizio_edit.setEnabled(False)
                    info_layout.addWidget(dataInizio_edit, 1, 3)

                    dataFine_label = QLabel("Data fine prenotazione:")
                    dataFine_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(dataFine_label, 2, 2)
                    dataFine_edit = QLineEdit(str(x['data_fine']))
                    dataFine_edit.setEnabled(False)
                    info_layout.addWidget(dataFine_edit, 2, 3)

                    polizza_label = QLabel("Polizza selezionata:")
                    polizza_label.setStyleSheet("font-size: 24px; ")
                    info_layout.addWidget(polizza_label, 3, 2)
                    polizza_edit = QComboBox()
                    polizza_edit.setCurrentText(str(x['polizza']))
                    polizza_edit.addItems(["rca", "kasko"])
                    polizza_edit.setEnabled(False)
                    info_layout.addWidget(polizza_edit, 3, 3)

                    buttons_layout = QHBoxLayout()
                    info_layout.addLayout(buttons_layout, 4, 2, alignment=Qt.AlignRight)
                    modify_button = QPushButton("Modifica")
                    modify_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #D9D9D9; border-radius: 15px; color: black; "
                                   "padding: 10px;")
                    modify_button.clicked.connect(
                        lambda _, a=data_edit, b=mezzo_edit, c=tariffa_edit, d=dataInizio_edit,
                               e=dataFine_edit, f=polizza_edit, g=modify_button: self.modifica_valori_lineedit(a, b, c, d, e, f, g))

                    buttons_layout.addWidget(modify_button)
                    disdici = QPushButton("Disdici")
                    disdici.clicked.connect(lambda _, p=x: self.disdici(p))
                    disdici.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; "
                                          "padding: 10px;")
                    buttons_layout.addWidget(disdici)

                    self.scroll_layout.addWidget(info_box)

    def go_back(self):
        self.close()
        from viste.viste_impiegato.pannelloControllo import VistaPannelloControllo
        self.vista = VistaPannelloControllo(self.user, self.psw)
        self.vista.show()

    def disdici(self, p):
        reply = QMessageBox.warning(self, 'Conferma Disdetta', 'Sei sicuro di voler disdire questa prenotazione?',
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            Prenotazione().eliminaPrenotazione(p)
        if reply == QMessageBox.Yes:
            QMessageBox.information(self, 'Disdetta Confermata', 'La prenotazione è stata disdetta con successo.', QMessageBox.Ok)
            self.go_back()

    def modifica_valori_lineedit(self, data_edit, mezzo_edit, tariffa_edit, dataInizio_edit, dataFine_edit, polizza_edit, modify_button):
        if modify_button.text() == "Modifica":
            modify_button.setText("Salva")
            data_edit.setEnabled(True)
            mezzo_edit.setEnabled(True)
            tariffa_edit.setEnabled(True)
            dataInizio_edit.setEnabled(True)
            dataFine_edit.setEnabled(True)
            polizza_edit.setEnabled(True)
        else:
            modify_button.setText("Modifica")
            data_edit.setEnabled(False)
            mezzo_edit.setEnabled(False)
            tariffa_edit.setEnabled(False)
            dataInizio_edit.setEnabled(False)
            dataFine_edit.setEnabled(False)
            polizza_edit.setEnabled(False)


    def go_aggiungiPrenotazione(self):
        pass