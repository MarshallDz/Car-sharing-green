from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Servizio.auto import Auto
from Servizio.moto import Moto
from Servizio.furgone import Furgone
from Servizio.van import Van
import darkdetect


class VistaMezziAmministratore(QMainWindow):
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

        self.title_label = QLabel("Lista dei mezzi")
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

        self.add_category_buttons()

        # Aggiungi la barra di ricerca in alto a destra
        self.search_layout = QHBoxLayout()
        self.search_layout.setAlignment(Qt.AlignRight | Qt.AlignTop)
        search_icon = QLabel()
        icon = QPixmap("viste/Icone/varie/search.png")
        icon.setDevicePixelRatio(10)
        search_icon.setPixmap(icon)
        search_icon.setAlignment(Qt.AlignRight)
        self.search_edit = QLineEdit()
        self.search_edit.setStyleSheet("max-width: 300px; max-height: 30px; border-radius: 15px; ")
        if darkdetect.isDark():
            self.search_edit.setStyleSheet("max-width: 300px; min-height: 60px; border-radius: 15px; "
                                           "background-color: #403F3F")
        self.search_edit.setPlaceholderText("cerca per nome")
        self.search_layout.addWidget(search_icon)
        self.search_layout.addWidget(self.search_edit)
        self.search_edit.textChanged.connect(self.search_mezzi)
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

        aggiungiPrenotazione_button = QPushButton("Aggiungi mezzo")
        aggiungiPrenotazione_button.setStyleSheet(
            "width: 150px; max-width: 150px; background-color: #6AFE67; border-radius: 15px; "
            "color: black; padding: 10px; margin-bottom: 20px")
        aggiungiPrenotazione_button.clicked.connect(self.go_aggiungiMezzo)
        self.central_layout.addWidget(aggiungiPrenotazione_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)

    def populate_scroll_layout(self, vehicle_list):
        for x in vehicle_list:
            info_box = QGroupBox()
            info_box.setStyleSheet("QGroupBox{max-height: 250px;}")
            info_layout = QGridLayout(info_box)

            telaio = QLabel(f"Codice telaio: {x['telaio']} ")
            telaio.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(telaio, 0, 0)

            produttore = QLabel(f"Produttore: {x['produttore']} ")
            produttore.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(produttore, 1, 0)

            modello = QLabel(f"Modello: {x['modello']} ")
            modello.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(modello, 2, 0)

            cilindrata = QLabel(f"Cilindrata: {x['cilindrata']} ")
            cilindrata.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cilindrata, 3, 0)

            anno = QLabel(f"Anno: {x['anno']} ")
            anno.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(anno, 0, 1)

            cavalli = QLabel(f"Cavalli: {x['cavalli']} ")
            cavalli.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cavalli, 1, 1)

            alimentazione = QLabel(f"Alimentazione: {x['alimentazione']} ")
            alimentazione.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(alimentazione, 2, 1)

            nPosti = QLabel(f"Numero posti: {x['nPosti']} ")
            nPosti.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(nPosti, 3, 1)

            cambio = QLabel(f"Cambio: {x['cambio']} ")
            cambio.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cambio, 4, 0)

            tariffa_oraria = QLabel(f"Tariffa oraria: {x['tariffa_oraria']} ")
            tariffa_oraria.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(tariffa_oraria, 5, 0)

            stato = QLabel(f"Stato: {x['stato']} ")
            stato.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(stato, 4, 1)

            pixmap = QPixmap(x["URL_immagine"])
            if not pixmap.isNull():
                label = QLabel()
                label.setStyleSheet("margin-left: 20px;")
                label.setMaximumWidth(300)
                label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))
                label.setAlignment(Qt.AlignCenter)
                info_layout.addWidget(label, 0, 3, 0, 3, alignment= Qt.AlignRight)
            else:
                error_label = QLabel("Immagine non disponibile")
                error_label.setMaximumWidth(200)
                error_label.setAlignment(Qt.AlignCenter)
                info_layout.addWidget(error_label, alignment= Qt.AlignRight)

            self.scroll_layout.addWidget(info_box)

    def go_back(self):
        from viste.viste_amministratore.admin import VistaAmministrazione
        self.vista = VistaAmministrazione()
        self.vista.show()
        self.close()

    def go_aggiungiMezzo(self):
        pass

    def search_mezzi(self, text):
        # Funzione per filtrare le prenotazioni in base al nome del cliente
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if isinstance(item, QLayoutItem):
                widget = item.widget()
                if isinstance(widget, QGroupBox):
                    labels = widget.findChildren(QLabel)
                    for label in labels:
                        client_name = label.text()
                        if text.lower() in client_name.lower():
                            widget.show()
                            break
                    else:
                        widget.hide()

    def add_category_buttons(self):
        # Create a horizontal layout for category buttons
        self.category_layout = QHBoxLayout()
        self.category_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

        # Create buttons for each category
        self.auto_button = QPushButton("Auto")
        self.auto_button.clicked.connect(lambda: self.filter_vehicles("Auto"))
        self.category_layout.addWidget(self.auto_button)

        self.moto_button = QPushButton("Moto")
        self.moto_button.clicked.connect(lambda: self.filter_vehicles("Moto"))
        self.category_layout.addWidget(self.moto_button)

        self.van_button = QPushButton("Van")
        self.van_button.clicked.connect(lambda: self.filter_vehicles("Van"))
        self.category_layout.addWidget(self.van_button)

        self.furgone_button = QPushButton("Furgone")
        self.furgone_button.clicked.connect(lambda: self.filter_vehicles("Furgone"))
        self.category_layout.addWidget(self.furgone_button)

        # Set stretch factor for buttons to occupy all available horizontal space
        self.auto_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.moto_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.van_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.furgone_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        # Add category layout to the main layout
        self.central_layout.addLayout(self.category_layout)

    def filter_vehicles(self, category):
        # Clear existing vehicles from scroll layout
        self.clear_scroll_layout()

        # Set background color for the pressed button and reset others
        buttons = [self.auto_button, self.moto_button, self.van_button, self.furgone_button]
        for button in buttons:
            if button.text() == category:
                button.setStyleSheet("QPushButton { background-color: #6AFE67; color: black}")
            else:
                button.setStyleSheet("QPushButton { background-color: none; }")

        # Populate the scroll layout with vehicles of the selected category
        if category == "Auto":
            self.populate_scroll_layout(Auto().get_dati())
        elif category == "Moto":
            self.populate_scroll_layout(Moto().get_dati())
        elif category == "Van":
            self.populate_scroll_layout(Van().get_dati())
        elif category == "Furgone":
            self.populate_scroll_layout(Furgone().get_dati())

    def clear_scroll_layout(self):
        # Clear existing vehicles from scroll layout
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()
