import json

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt
from viste.effettua_prenotazione import VistaEffettuaPrenotazione
import darkdetect

class VistaPrenotazioneAuto(QMainWindow):
    def __init__(self, user, psw):
        super().__init__()
        self.user = user
        self.psw = psw

        self.setWindowTitle("Pagina di prenotazione auto")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.setMinimumWidth(1000)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout()

        title_layout = QVBoxLayout()
        title_layout.setAlignment(Qt.AlignTop | Qt.AlignCenter)

        self.central_widget.setLayout(self.central_layout)

        self.title_label = QLabel("Prenota la tua auto: ")
        self.title_font = self.title_label.font()
        self.title_font.setPointSize(42)
        self.title_font.setBold(True)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()

        title_layout.addWidget(self.title_label)
        self.central_layout.addLayout(title_layout)

        mezzi = []
        file_path = "dati/auto.json"
        with open(file_path, "r") as file:
            data = json.load(file)
            chiavi = list(data[0].keys())
            for auto in data:
                valori = list(auto.values())

                for i in range(len(valori)):
                    auto[chiavi[i]] = valori[i]
                # print(auto)
                mezzi.append(auto)

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

        for i in range(len(mezzi)):
            self.aggiungi_box_auto(mezzi[i])

        # Aggiungiamo il pulsante "Indietro"
        button_layout = QVBoxLayout()
        button_layout.setAlignment(Qt.AlignBottom | Qt.AlignRight)

        self.back_button = QPushButton("Indietro")
        self.back_button.setStyleSheet("width: 150px; background-color: #F85959; border-radius: 15px; color: black; padding: 10px;"
            "margin-right: 60px; margin-bottom: 60px;")
        self.back_button.clicked.connect(self.go_back)

        button_layout.addWidget(self.back_button)
        self.central_layout.addLayout(button_layout)

    def aggiungi_box_auto(self, auto):
        car_info_frame = QFrame()
        car_info_frame.setStyleSheet("border: 2px solid white; border-radius: 5px; margin-right: 5px;")
        car_info_frame.setMinimumWidth(600)
        car_info_frame.setMaximumWidth(1000)

        car_info_layout = QGridLayout(car_info_frame)
        car_info_layout.setAlignment(Qt.AlignTop)
        # Aggiungi le informazioni alla griglia
        self.labels_values = [("Produttore:", auto["produttore"]),
                              ("Modello:", auto["modello"]),
                              ("Anno:", auto["anno"]),
                              ("Alimentazione:", auto["alimentazione"]),
                              ("Cavalli:", auto["cavalli"]),
                              ("Cilindrata:", auto["cilindrata"]),
                              ("Cambio:", auto["cambio"]),
                              ("Numero Posti:", auto["nPosti"])]

        for i, (label_name, value) in enumerate(self.labels_values):
            label_name = QLabel(label_name, self)
            label_name.setStyleSheet("border: 0px")

            value_label = QLabel(str(value), self)
            value_label.setStyleSheet("border: 0px")

            row = i // 2
            col = i % 2

            car_info_layout.addWidget(label_name, row, col * 2)
            car_info_layout.addWidget(value_label, row, col * 2 + 1)

        tariffaLabel = QLabel(f"A partire da {auto['tariffa_oraria']}€ ad ora \n oppure  {int(auto['tariffa_oraria'])*24*0.7}€ al giorno")
        tariffaLabel.setStyleSheet("border: 0px")
        myFont = QtGui.QFont()
        myFont.setBold(True)
        tariffaLabel.setFont(myFont)
        car_info_layout.addWidget(tariffaLabel, 6, 0)
        prenota_button = QPushButton("Prenota")
        prenota_button.setStyleSheet("color: black; border-radius: 5px; background-color: #D9D9D9")
        prenota_button.clicked.connect(
            lambda _, car=auto: self.go_prenota(car))  # Connessione con la funzione go_prenota
        car_info_layout.addWidget(prenota_button, 6, 3)
        car_layout = QHBoxLayout()
        car_layout.setAlignment(Qt.AlignTop)

        pixmap = QPixmap(auto["URL_immagine"])
        if not pixmap.isNull():
            label = QLabel()
            label.setStyleSheet("margin-left: 20px;")
            label.setMaximumWidth(200)
            label.setPixmap(pixmap.scaled(200, 200, Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)
            car_layout.addWidget(label)
        else:
            error_label = QLabel("Immagine non disponibile")
            error_label.setMaximumWidth(200)
            error_label.setAlignment(Qt.AlignCenter)
            car_layout.addWidget(error_label)

        car_layout.addWidget(car_info_frame)

        self.scroll_layout.addLayout(car_layout)

    def go_back(self):
        from viste.prenotazione import VistaPrenotazione
        self.vista = VistaPrenotazione(self.user, self.psw)
        self.vista.show()
        self.close()

    def go_prenota(self, auto):
        self.vista_prenotazione = VistaEffettuaPrenotazione(self.user, self.psw, auto)
        self.vista_prenotazione.show()
        self.close()
