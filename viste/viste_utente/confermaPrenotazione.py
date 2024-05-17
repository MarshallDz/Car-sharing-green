from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLabel, QFrame, QGroupBox, QPushButton, QGridLayout
from PyQt5.QtCore import Qt
import darkdetect

class VistaConfermaPrenotazione(QMainWindow):
    def __init__(self, user, psw,  data, mezzo, inizio, fine, tariffa, polizza):
        super().__init__()
        self.user = user
        self.psw = psw
        self.data = data
        self.mezzo = mezzo
        self.inizio = inizio
        self.fine = fine
        self.tariffa = tariffa
        self.polizza = polizza
        self.setWindowTitle("CarGreen")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if darkdetect.isDark():
            self.setStyleSheet("background-color: #121212;")
        self.setStyleSheet(f"max-width: {self.width()}")
        self.showMaximized()
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.central_layout = QGridLayout()
        self.central_widget.setLayout(self.central_layout)

        # Creazione del frame verde
        green_frame = QFrame(self)
        green_frame.setFrameShape(QFrame.StyledPanel)
        green_frame.setStyleSheet(f"background-color: #85F52D; min-height: {self.height()*0.3}px")
        green_frame_layout = QVBoxLayout()

        # Creazione della label all'interno del frame verde
        label = QLabel(f"Prenotazione \n confermata", green_frame)
        label.setStyleSheet("color: black;")
        title_font = label.font()
        title_font.setPointSize(42)
        title_font.setBold(True)
        label.setFont(title_font)
        label.setAlignment(Qt.AlignCenter)

        # Aggiungere la label al layout del frame
        green_frame_layout.addWidget(label)
        green_frame.setLayout(green_frame_layout)

        # Aggiungere il frame al layout centrale con allineamento al centro
        self.central_layout.addWidget(green_frame, 0, 0, alignment=Qt.AlignTop)

        # Creazione del box per le informazioni sulla prenotazione
        info_box = QGroupBox("Informazioni sulla prenotazione")
        info_layout = QVBoxLayout()
        info_box.setLayout(info_layout)

        # Aggiungi le informazioni sulla prenotazione al box

        data_label = QLabel(f"data prenotazione: {self.data}")
        data_label.setStyleSheet("font-size: 24px")
        info_layout.addWidget(data_label)

        mezzo_label = QLabel(f"mezzo: {self.mezzo['produttore'] + ' ' + self.mezzo['modello']}")
        mezzo_label.setStyleSheet("font-size: 24px")
        info_layout.addWidget(mezzo_label)

        dataInizio_label = QLabel(f"data inizio prenotazione: {self.inizio}")
        dataInizio_label.setStyleSheet("font-size: 24px")
        info_layout.addWidget(dataInizio_label)

        dataFine_label = QLabel(f"data fine prenotazione: {self.fine}")
        dataFine_label.setStyleSheet("font-size: 24px")
        info_layout.addWidget(dataFine_label)

        tariffa_label = QLabel(f"tariffa selezionata: {self.tariffa}")
        tariffa_label.setStyleSheet("font-size: 24px")
        info_layout.addWidget(tariffa_label)

        polizza_label = QLabel(f"polizza selezionata: {self.polizza}")
        polizza_label.setStyleSheet("font-size: 24px")
        info_layout.addWidget(polizza_label)

        back_button = QPushButton("Indietro")
        back_button.clicked.connect(self.go_home)
        back_button.setStyleSheet("width: 150px; max-width: 150px; background-color: #F85959; border-radius: 15px; color: black; "
            "padding: 10px; margin-bottom: 20px")
        self.central_layout.addWidget(back_button, 2, 0, alignment=Qt.AlignHCenter | Qt.AlignBottom)
        # Aggiungi il box al layout centrale
        self.central_layout.addWidget(info_box, 1, 0, alignment=Qt.AlignTop)

    def go_home(self):
        from viste.viste_utente.home import VistaHome
        self.vistaHome = VistaHome(self.user, self.psw)
        self.vistaHome.show()
        self.close()


