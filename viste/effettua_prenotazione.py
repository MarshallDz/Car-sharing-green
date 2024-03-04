from PyQt5.QtWidgets import *
from PyQt5.QtCore import Qt, QDate
from Attivita.cliente import *
from Attivita.prenotazione import *
import datetime


class VistaEffettuaPrenotazione(QMainWindow):
    def __init__(self, user, psw, mezzo):
        super().__init__()
        self.user = user
        self.psw = psw
        self.mezzo = mezzo

        self.setWindowTitle("Schermata di prenotazione")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QGridLayout()
        self.central_layout.setContentsMargins(20, 0, 20, 0)
        self.central_layout.setVerticalSpacing(int(self.width()*0.04))
        self.central_widget.setLayout(self.central_layout)

        self.title_label = QLabel("Effettua la tua prenotazione ")
        self.title_label.setStyleSheet("color: white;")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.title_label.adjustSize()
        self.central_layout.addWidget(self.title_label, 0, 1)

        self.valori = {}

        inizio_noleggio = QLabel("Data inizio noleggio:")
        inizio_noleggio.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(inizio_noleggio, 1, 0, alignment=Qt.AlignTop)

        self.campo1 = QDateEdit()
        self.campo1.setCalendarPopup(True)
        self.campo1.setMinimumDate(QDate.currentDate())
        self.campo1.setStyleSheet("color: black; background-color: white; max-width: 1000px; min-width: 800px")
        self.campo1.setSpecialValueText("Scegli data inizio noleggio")
        self.central_layout.addWidget(self.campo1, 1, 3)
        self.campo1.dateChanged.connect(self.update_valori)
        self.valori["data_inizio"] = self.campo1.date().toString(Qt.ISODate)

        fine_noleggio = QLabel("Data fine noleggio:")
        fine_noleggio.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(fine_noleggio, 2, 0, alignment=Qt.AlignTop)

        self.campo2 = QDateEdit()
        self.campo2.setCalendarPopup(True)
        self.campo2.setMinimumDate(QDate.currentDate())
        self.campo2.setStyleSheet("color: black; background-color: white; max-width: 1000px; min-width: 800px; "
                                  "margin-right: 15px")
        self.campo2.setSpecialValueText("Scegli data fine noleggio")
        self.central_layout.addWidget(self.campo2, 2, 3)
        self.campo2.dateChanged.connect(self.update_valori)
        self.valori["data_fine"] = self.campo2.date().toString(Qt.ISODate)

        filiale_label = QLabel("Filiale ritiro mezzo:")
        filiale_label.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(filiale_label, 3, 0)

        self.filiale = QComboBox(self)
        self.filiale.setStyleSheet("background-color: white; margin-right: 15px; color: black;")
        self.filiale.setPlaceholderText("Scegli:")
        self.filiale.addItems(["Milano, via padova", "Milano, via roma"])
        self.filiale.currentIndexChanged.connect(self.update_valori)
        self.central_layout.addWidget(self.filiale, 3, 3)
        self.valori["filiale"] = self.filiale.currentText()

        assicurazione_label = QLabel("Polizza assicurativa:")
        assicurazione_label.setStyleSheet("color: white; font-size: 18px")
        self.central_layout.addWidget(assicurazione_label, 4, 0)

        self.polizza = QComboBox(self)
        self.polizza.setStyleSheet("background-color: white; margin-right: 15px; color: black")
        self.polizza.setPlaceholderText("Scegli:")
        self.polizza.addItems(["rca", "kasko"])
        self.central_layout.addWidget(self.polizza, 4, 3)
        self.polizza.currentIndexChanged.connect(self.update_valori)
        self.valori["polizza"] = self.polizza.currentText()

        tariffa = QLabel("Tariffa:")
        tariffa.setStyleSheet(f"color: white; font-size: 18px;")
        self.central_layout.addWidget(tariffa, 5, 0)

        self.tariffa = QComboBox(self)
        self.tariffa.setStyleSheet(f"background-color: white; margin-right: 15px; color: black;")
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

        back_button = QPushButton("Indietro")
        back_button.setStyleSheet(
            "width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; "
            "padding: 10px; margin-right: 50px")
        back_button.clicked.connect(self.go_back)
        self.central_layout.addWidget(back_button, 7, 3, alignment=(Qt.AlignRight|Qt.AlignTop))

    def update_valori(self):
        sender = self.sender()  # Identifica quale combobox ha generato il segnale

        # Aggiorna self.valori
        if sender == self.campo1:
            self.valori["data_inizio"] = sender.date().toString(Qt.ISODate)
            new_start_date = sender.date()
            self.campo2.setMinimumDate(new_start_date)
            current_end_date = self.campo2.date()
            if current_end_date < new_start_date:
                # Se la data di fine noleggio è precedente alla nuova data di inizio noleggio, aggiorna la data di fine noleggio
                self.campo2.setDate(new_start_date)
        elif sender == self.campo2:
            self.valori["data_fine"] = sender.date().toString(Qt.ISODate)
        elif sender == self.filiale:
            self.valori["filiale"] = sender.currentText()
        elif sender == self.polizza:
            self.valori["polizza"] = sender.currentText()
        else:
            self.valori["tariffa"] = sender.currentText()

    def go_back(self):
        self.close()

    def conferma_prenotazione(self):
        cliente = Cliente.get_cliente(self, self.user, self.psw)
        prenotazione = Prenotazione()
        prenotazione.aggiungiPrenotazione("", cliente, QDate.currentDate().toString(), self.valori["data_inizio"],
                                          self.valori["data_fine"], self.mezzo, self.valori["filiale"],
                                          self.valori["polizza"], self.valori["tariffa"])
