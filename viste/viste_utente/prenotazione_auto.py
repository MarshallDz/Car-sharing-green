import json

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt

from Servizio.auto import Auto
from viste.viste_utente.effettua_prenotazione import VistaEffettuaPrenotazione


class PrenotazioneAuto(QWidget):
    def __init__(self, cliente, s):
        super().__init__()
        self.cliente = cliente
        self.shell = s
        self.layout = QVBoxLayout()

        mezzi = []
        data = Auto().get_dati()
        chiavi = list(data[0].keys())
        for auto in data:
            valori = list(auto.values())

            for i in range(len(valori)):
                auto[chiavi[i]] = valori[i]
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
                                  "    border: none;"
                                  "}"
                                  "QScrollBar::sub-line:vertical {"
                                  "    background: none;"
                                  "}"
                                  "QScrollArea {"
                                  "border: none"
                                  "}")
        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.layout.addWidget(scroll_area)
        self.setLayout(self.layout)

        for i in range(len(mezzi)):
            self.aggiungi_box_auto(mezzi[i])

    def aggiungi_box_auto(self, auto):
        car_info_frame = QFrame()
        car_info_frame.setStyleSheet("border: 2px solid white; border-radius: 5px; margin-right: 5px;")
        car_info_frame.setMinimumWidth(600)
        car_info_frame.setMaximumWidth(1500)

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

        tariffaLabel = QLabel(f"A partire da {auto['tariffaOraria']}€ ad ora \n oppure  {int(int(auto['tariffaOraria'])*24*0.7)}€ al giorno")
        tariffaLabel.setStyleSheet("border: 0px")
        myFont = QtGui.QFont()
        myFont.setBold(True)
        tariffaLabel.setFont(myFont)
        car_info_layout.addWidget(tariffaLabel, 6, 0)
        if auto["stato"] == "disponibile":
            prenota_button = QPushButton("Prenota")
            prenota_button.setStyleSheet("max-height: 25px; color: black; border-radius: 10px; background-color: "
                                         "#0bd400")
            prenota_button.clicked.connect(
                lambda _, car=auto: self.go_prenota(car))  # Connessione con la funzione go_prenota
        else:
            prenota_button = QPushButton("Non disponibile")
            prenota_button.setStyleSheet("max-height: 25px; color: black; border-radius: 10px; background-color: "
                                         "#9c9c9c")
        car_info_layout.addWidget(prenota_button, 6, 3)
        car_layout = QHBoxLayout()
        car_layout.setAlignment(Qt.AlignTop)

        pixmap = QPixmap(auto["immagine"])
        if not pixmap.isNull():
            label = QLabel()
            label.setStyleSheet("margin-left: 20px;")
            label.setMaximumWidth(300)
            label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)
            car_layout.addWidget(label)
        else:
            error_label = QLabel("Immagine non disponibile")
            error_label.setMaximumWidth(200)
            error_label.setAlignment(Qt.AlignCenter)
            car_layout.addWidget(error_label)

        car_layout.addWidget(car_info_frame)

        self.scroll_layout.addLayout(car_layout)

    def go_prenota(self, auto):
        self.vista_prenotazione = VistaEffettuaPrenotazione(self.cliente, auto)
        self.vista_prenotazione.show()
        self.shell.close()
