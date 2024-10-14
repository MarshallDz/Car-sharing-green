import darkdetect
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QPixmap, QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QLabel, QHBoxLayout, QLineEdit, \
    QScrollArea, QPushButton, QGroupBox, QGridLayout, QMessageBox, QLayoutItem

from Attivita.cliente import Cliente


class VistaGestioneClienti(QMainWindow):
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

        self.title_label = QLabel("Gestione clienti")
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
        self.search_edit.textChanged.connect(self.search_cliente)
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
                                  "}")

        scroll_area.setWidgetResizable(True)
        self.scroll_content = QWidget(scroll_area)
        scroll_area.setWidget(self.scroll_content)
        self.scroll_layout = QVBoxLayout(self.scroll_content)
        self.central_layout.addWidget(scroll_area)

        self.aggiungi_box_info()
        aggiungiCliente_button = QPushButton("Aggiungi cliente")
        aggiungiCliente_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #6AFE67; "
                                             "border-radius: 15px; color: black; padding: 10px; margin-bottom: 20px")
        aggiungiCliente_button.clicked.connect(self.go_aggiungiCliente)
        self.central_layout.addWidget(aggiungiCliente_button, alignment=Qt.AlignHCenter | Qt.AlignBottom)

    def aggiungi_box_info(self):
        cliente = Cliente()
        clienti_info = cliente.get_dati()
        for client in clienti_info:
            info_box = QGroupBox()
            info_box.setStyleSheet("QGroupBox{max-height: 200px;}")
            info_layout = QGridLayout(info_box)

            cF_label = QLabel("Codice Fiscale:")

            cF_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cF_label, 1, 0)

            self.cf_edit = QLineEdit(client["codiceFiscale"])
            self.cf_edit.setEnabled(False)
            info_layout.addWidget(self.cf_edit, 1, 1)

            nome_label = QLabel("Nome:")
            nome_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(nome_label, 2, 0)

            self.nome_edit = QLineEdit(client["nome"])
            self.nome_edit.setEnabled(False)
            info_layout.addWidget(self.nome_edit, 2, 1)

            cognome_label = QLabel("Cognome:")
            cognome_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cognome_label, 3, 0)

            self.cognome_edit = QLineEdit(client["cognome"])
            self.cognome_edit.setEnabled(False)
            info_layout.addWidget(self.cognome_edit, 3, 1)

            dataNascita_label = QLabel("Data di nascita:")
            dataNascita_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(dataNascita_label, 1, 2)

            self.dataNascita_edit = QLineEdit(client["dataNascita"])
            self.dataNascita_edit.setEnabled(False)
            info_layout.addWidget(self.dataNascita_edit, 1, 3)

            email_label = QLabel("Email:")
            email_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(email_label, 2, 2)

            self.email_edit = QLineEdit(client["email"])
            self.email_edit.setEnabled(False)
            info_layout.addWidget(self.email_edit, 2, 3)

            cellulare_label = QLabel("Cellulare:")
            cellulare_label.setStyleSheet("font-size: 24px; ")
            info_layout.addWidget(cellulare_label, 3, 2)

            self.cellulare_edit = QLineEdit(client["cellulare"])
            self.cellulare_edit.setEnabled(False)
            info_layout.addWidget(self.cellulare_edit, 3, 3)

            buttons_layout = QHBoxLayout()
            info_layout.addLayout(buttons_layout, 4, 2, alignment=Qt.AlignRight)
            modify_button = QPushButton("Modifica")
            modify_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #D9D9D9; border-radius: "
                                        "15px; color: black; padding: 10px;")
            modify_button.clicked.connect(
                lambda _, cc=client, a=self.cf_edit, b=self.nome_edit, c=self.cognome_edit, d=self.dataNascita_edit, e=self.email_edit, f=self.cellulare_edit, g=modify_button: self.modifica_valori_lineedit(cc, a, b, c, d, e, f, g))

            buttons_layout.addWidget(modify_button)
            elimina = QPushButton("Elimina")
            elimina.clicked.connect(lambda _, p=client: self.eliminaCliente(p))
            elimina.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; "
                                  "color: black; padding: 10px;")
            buttons_layout.addWidget(elimina)

            self.scroll_layout.addWidget(info_box)

    def go_back(self):
        from viste.viste_amministratore.admin import VistaAmministrazione
        self.vista = VistaAmministrazione()
        self.vista.show()
        self.close()

    def eliminaCliente(self, c):
        cliente = Cliente()
        reply = QMessageBox.warning(self, 'Conferma eliminazione', 'Sei sicuro di voler eliminare il cliente?',
                                    QMessageBox.Yes, QMessageBox.No)

        if reply == QMessageBox.Yes:
            cliente.eliminaCliente(c)
            QMessageBox.information(self, 'Disdetta Confermata', 'Il cliente è stato eliminato con successo.',QMessageBox.Ok)

    def modifica_valori_lineedit(self, cc, cF, nome, cognome, dataN, email, cellulare, modify_button):
        # bisogna aggiungere anche la modifica nel file prenotazioni.json
        if modify_button.text() == "Modifica":
            modify_button.setText("Salva")
            cF.setEnabled(True)
            nome.setEnabled(True)
            cognome.setEnabled(True)
            dataN.setEnabled(True)
            email.setEnabled(True)
            cellulare.setEnabled(True)

            # Salva i riferimenti ai campi QLineEdit
            self.cf = cF
            self.nome = nome
            self.cognome = cognome
            self.datan = dataN
            self.email = email
            self.cel = cellulare
            self.clientec = cc
        else:
            modify_button.setText("Modifica")
            cF.setEnabled(False)
            nome.setEnabled(False)
            cognome.setEnabled(False)
            dataN.setEnabled(False)
            email.setEnabled(False)
            cellulare.setEnabled(False)
            self.salva_valori()

    def go_aggiungiCliente(self):
        from viste.viste_amministratore.aggiungiCliente import VistaRegistrazioneCliente
        self.vista = VistaRegistrazioneCliente()
        self.vista.show()
        self.close()

    def search_cliente(self, text):
        for i in range(self.scroll_layout.count()):
            item = self.scroll_layout.itemAt(i)
            if isinstance(item, QLayoutItem):
                widget = item.widget()
                if isinstance(widget, QGroupBox):
                    cliente_labels = widget.findChildren(QLineEdit)
                    for label in cliente_labels:
                        client_name = label.text()
                        if text.lower() in client_name.lower():
                            widget.show()
                            break
                    else:
                        widget.hide()

    def salva_valori(self):
        # Estrai i valori dai campi QLineEdit e memorizzali nelle variabili di istanza
        self.cod = self.cf.text()
        self.n = self.nome.text()
        self.c = self.cognome.text()
        self.dN = self.datan.text()
        self.e = self.email.text()
        self.cl = self.cel.text()
        cliente = Cliente()
        cliente.aggiornaValori(self.clientec, self.cod, self.n, self.c, self.dN, self.e, self.cl)
        self.aggiorna_vista()

    def aggiorna_vista(self):
        # Rimuovi tutti i widget dalla scroll_layout
        while self.scroll_layout.count():
            item = self.scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # Ora puoi chiamare nuovamente il metodo per aggiungere i widget aggiornati
        self.aggiungi_box_info()



