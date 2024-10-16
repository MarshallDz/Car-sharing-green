from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from Noleggio.auto import Auto
from Noleggio.mezzo import Mezzo
from Noleggio.moto import Moto
from Noleggio.furgone import Furgone
from Noleggio.van import Van
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

        self.title_label = QLabel("Gestione mezzi")
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
        self.search_edit.setStyleSheet("max-width: 300px; max-height: 40px; border-radius: 15px; ")
        if darkdetect.isDark():
            self.search_edit.setStyleSheet("max-width: 300px; max-height: 40px; border-radius: 15px; "
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

        self.aggiungiPrenotazione_button = QPushButton("Seleziona una categoria")
        self.aggiungiPrenotazione_button.setStyleSheet(
            "width: 150px; max-width: 150px; background-color: #6AFE67; border-radius: 15px; "
            "color: black; padding: 10px; margin-bottom: 20px")
        self.category = None
        self.central_layout.addWidget(self.aggiungiPrenotazione_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)

    def populate_scroll_layout(self, vehicle_list):
        for v in vehicle_list:
            info_box = QGroupBox()
            info_box.setStyleSheet("QGroupBox{max-height: 250px;}")
            info_layout = QGridLayout(info_box)

            telaio = QLabel(f"Codice telaio: {v['telaio']} ")
            telaio.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(telaio, 0, 0)

            produttore = QLabel(f"Produttore: {v['produttore']} ")
            produttore.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(produttore, 1, 0)

            modello = QLabel(f"Modello: {v['modello']} ")
            modello.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(modello, 2, 0)

            cilindrata = QLabel(f"Cilindrata: {v['cilindrata']} ")
            cilindrata.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cilindrata, 3, 0)

            anno = QLabel(f"Anno: {v['anno']} ")
            anno.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(anno, 0, 1)

            cavalli = QLabel(f"Cavalli: {v['cavalli']} ")
            cavalli.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cavalli, 1, 1)

            alimentazione = QLabel(f"Alimentazione: {v['alimentazione']} ")
            alimentazione.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(alimentazione, 2, 1)

            nPosti = QLabel(f"Numero posti: {v['nPosti']} ")
            nPosti.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(nPosti, 3, 1)

            cambio = QLabel(f"Cambio: {v['cambio']} ")
            cambio.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cambio, 4, 0)

            tariffa_label = QLabel("Tariffa oraria (€): ")
            tariffa_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(tariffa_label, 5, 0)

            tariffa_valore = QLineEdit(f"{v['tariffaOraria']}")
            tariffa_valore.setStyleSheet("font-size: 18px; max-width: 50px")
            info_layout.addWidget(tariffa_valore, 5, 1)

            stato = QLabel(f"Stato: {v['stato']} ")
            stato.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(stato, 4, 1, alignment=Qt.AlignRight)

            button_layout = QVBoxLayout()
            update_button = self.add_update_button(v, tariffa_valore)
            button_layout.addWidget(update_button)

            elimina = QPushButton("Elimina")
            elimina.clicked.connect(lambda _, m=v: self.eliminaMezzo(m))
            elimina.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; "
                                  "color: black; padding: 10px;")
            button_layout.addWidget(elimina)
            info_layout.addLayout(button_layout, 2, 2, 4, 2, alignment=Qt.AlignRight)

            pixmap = QPixmap(v["immagine"])
            if not pixmap.isNull():
                label = QLabel()
                label.setStyleSheet("margin-left: 20px;")
                label.setMaximumWidth(300)
                label.setPixmap(pixmap.scaled(300, 400, Qt.KeepAspectRatio))
                label.setAlignment(Qt.AlignCenter)
                info_layout.addWidget(label, 0, 3, 0, 3, alignment=Qt.AlignRight)
            else:
                error_label = QLabel("Immagine non disponibile")
                error_label.setMaximumWidth(200)
                error_label.setAlignment(Qt.AlignCenter)
                info_layout.addWidget(error_label, 0, 3, 0, 3, alignment=Qt.AlignRight)

            self.scroll_layout.addWidget(info_box)

    def go_back(self):
        from viste.viste_amministratore.admin import VistaAmministrazione
        self.vista = VistaAmministrazione()
        self.vista.show()
        self.close()

    def go_aggiungiMezzo(self):
        from viste.viste_amministratore.aggiungiMezzo import VistaAggiungiMezzo
        self.vista = VistaAggiungiMezzo(self.category)
        self.vista.show()
        self.close()

    def search_mezzi(self, text):
        # Funzione per filtrare le prenotazioni in base al nome del mezzo
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
        self.category_layout = QHBoxLayout()
        self.category_layout.setAlignment(Qt.AlignLeft | Qt.AlignTop)

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

        self.auto_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.moto_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.van_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.furgone_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

        self.central_layout.addLayout(self.category_layout)

    def filter_vehicles(self, category):
        self.clear_scroll_layout()
        self.category = category

        buttons = [self.auto_button, self.moto_button, self.van_button, self.furgone_button]
        for button in buttons:
            if button.text() == self.category:
                button.setStyleSheet("QPushButton { background-color: #6AFE67; color: black}")
                self.aggiungiPrenotazione_button.setText("Aggiungi " + self.category.lower())
                self.aggiungiPrenotazione_button.clicked.connect(self.go_aggiungiMezzo)
            else:
                button.setStyleSheet("QPushButton { background-color: none; }")

        # Popolo lo scroll
        if self.category == "Auto":
            self.populate_scroll_layout(Auto().get_dati())
        elif self.category == "Moto":
            self.populate_scroll_layout(Moto().get_dati())
        elif self.category == "Van":
            self.populate_scroll_layout(Van().get_dati())
        elif self.category == "Furgone":
            self.populate_scroll_layout(Furgone().get_dati())

    def clear_scroll_layout(self):
        for i in reversed(range(self.scroll_layout.count())):
            widget = self.scroll_layout.itemAt(i).widget()
            if widget:
                widget.deleteLater()

    def eliminaMezzo(self, m):
        reply = QMessageBox.warning(self, 'Conferma eliminazione', 'Sei sicuro di voler eliminare questo mezzo?',
                                    QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            if self.category == "Auto":
                Auto().eliminaAuto(m)
            elif self.category == "Moto":
                Moto().eliminaMoto(m)
            elif self.category == "Van":
                Van().eliminaVan(m)
            elif self.category == "Furgone":
                Furgone().eliminaFurgone(m)
            QMessageBox.information(self, 'Mezzo eliminato', 'Il mezzo è stato eliminato correttamente.',
                                    QMessageBox.Ok)
            self.filter_vehicles(None)

    def add_update_button(self, m, line_edit):
        button = QPushButton("Aggiorna tariffa")
        button.clicked.connect(lambda: self.aggiorna_tariffa(m, line_edit.text()))
        button.setStyleSheet("width: 150px; max-width: 150px; background-color: #D9D9D9; border-radius: 15px; color: black; padding: 10px;")
        return button

    def aggiorna_tariffa(self, mezzo, nuova):
        from Noleggio.auto import Auto
        from Noleggio.moto import Moto
        from Noleggio.van import Van
        from Noleggio.furgone import Furgone
        url_auto = "dati/auto.json"
        auto = Auto().get_dati()

        self.check = False
        for a in auto:
            if mezzo["telaio"] == a["telaio"]:
                self.check = True
                a["tariffaOraria"] = nuova
                Auto().writeData(url_auto, auto)
                break
        if not self.check:
            moto = Moto().get_dati()
            url_moto = "dati/moto.json"
            for m in moto:
                if mezzo == m:
                    self.check = True
                    m["tariffaOraria"] = nuova
                    Moto().writeData(url_moto, moto)
                    break
        if not self.check:
            van = Van().get_dati()
            url_van = "dati/van.json"
            for v in van:
                if mezzo == v:
                    self.check = True
                    v["tariffaOraria"] = nuova
                    Van().writeData(url_van, van)
                    break
        if not self.check:
            fur = Furgone().get_dati()
            url_fur = "dati/furgoni.json"
            for f in fur:
                if mezzo == f:
                    self.check = True
                    f["tariffaOraria"] = nuova
                    Furgone().writeData(url_fur, fur)
                    break
