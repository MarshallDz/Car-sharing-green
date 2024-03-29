import sys
import json

from PyQt5 import QtGui
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QSize
from viste.effettua_prenotazione import VistaEffettuaPrenotazione
import darkdetect

class VistaPrenotazioneMoto(QMainWindow):
    def __init__(self, user, psw):
        super().__init__()
        self.user = user
        self.psw = psw

        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.setMinimumWidth(1000)
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QVBoxLayout()
        self.central_widget.setLayout(self.central_layout)

        title_layout = QHBoxLayout()

        back_button = QPushButton()
        back_button.setStyleSheet("max-width: 100px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/back.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        title_layout.addWidget(back_button)

        self.title_label = QLabel("Prenota il tuo scooter")
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

        file_path = "dati/moto.json"
        mezzi = []
        with open(file_path, "r") as file:
            data = json.load(file)
            chiavi = list(data[0].keys())
            for moto in data:
                valori = list(moto.values())

                for i in range(len(valori)):
                    moto[chiavi[i]] = valori[i]
                # print(auto)
                mezzi.append(moto)

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
                                  "}")

        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)

        self.central_layout.addWidget(scroll_area)

        for i in range(len(mezzi)):
            self.aggiungi_box_moto(mezzi[i])

    def aggiungi_box_moto(self, moto):
        car_info_frame = QFrame()
        car_info_frame.setStyleSheet("border: 2px solid white; border-radius: 5px; margin-right: 5px;")
        car_info_frame.setMinimumWidth(600)
        car_info_frame.setMaximumWidth(1500)

        car_info_layout = QGridLayout(car_info_frame)
        car_info_layout.setAlignment(Qt.AlignTop)

        # Aggiungi le informazioni alla griglia
        self.labels_values = [("Produttore:", moto["produttore"]),
                              ("Modello:", moto["modello"]),
                              ("Anno:", moto["anno"]),
                              ("Alimentazione:", moto["alimentazione"]),
                              ("Cavalli:", moto["cavalli"]),
                              ("Cilindrata:", moto["cilindrata"]),
                              ("Cambio:", moto["cambio"]),
                              ("Numero Posti:", moto["nPosti"])]

        for i, (label_name, value) in enumerate(self.labels_values):
            label_name = QLabel(label_name, self)
            label_name.setStyleSheet("border: 0px")

            value_label = QLabel(str(value), self)
            value_label.setStyleSheet("border: 0px")

            row = i // 2
            col = i % 2

            car_info_layout.addWidget(label_name, row, col * 2)
            car_info_layout.addWidget(value_label, row, col * 2 + 1)

        tariffaLabel = QLabel(f"A partire da {moto['tariffa_oraria']}€ ad ora \n oppure  {int(int(moto['tariffa_oraria']) * 24 * 0.7)}€ al giorno")
        tariffaLabel.setStyleSheet("border: 0px")
        myFont = QtGui.QFont()
        myFont.setBold(True)
        tariffaLabel.setFont(myFont)
        car_info_layout.addWidget(tariffaLabel, 6, 0)
        prenota_button = QPushButton("Prenota")
        prenota_button.setStyleSheet("color: black; border-radius: 5px; background-color: #D9D9D9")
        prenota_button.clicked.connect(lambda _, car=moto: self.go_prenota(car))
        car_info_layout.addWidget(prenota_button, 6, 3)
        car_layout = QHBoxLayout()
        car_layout.setAlignment(Qt.AlignTop)

        pixmap = QPixmap(moto["URL_immagine"])
        if not pixmap.isNull():
            label = QLabel()
            label.setStyleSheet("margin-left: 20px;")
            label.setMaximumWidth(300)
            label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))
            label.setAlignment(Qt.AlignCenter)
            car_layout.addWidget(label)
        else:
            error_label = QLabel("Immagine non disponibile")
            error_label.setAlignment(Qt.AlignCenter)
            error_label.setMaximumWidth(200)
            car_layout.addWidget(error_label)

        car_layout.addWidget(car_info_frame)

        self.scroll_layout.addLayout(car_layout)

    def go_back(self):
        from viste.prenotazione import VistaPrenotazione
        self.vista = VistaPrenotazione(self.user, self.psw)
        self.vista.show()
        self.close()

    def go_prenota(self, moto):
        self.vista_prenotazione = VistaEffettuaPrenotazione(self.user, self.psw, moto)
        self.vista_prenotazione.show()
        self.close()
