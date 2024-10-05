from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from viste.viste_utente.prenotazione_auto import PrenotazioneAuto
from viste.viste_utente.prenotazione_moto import PrenotazioneMoto
from viste.viste_utente.prenotazione_van import PrenotazioneVan
from viste.viste_utente.prenotazione_furgoni import PrenotazioneFurgone
import darkdetect


class VistaPrenotazione(QMainWindow):
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
        button_layout = QHBoxLayout()
        self.stacklayout = QStackedLayout()

        title_layout = QHBoxLayout()
        back_button = QPushButton()
        back_button.setStyleSheet("max-width: 100px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/back.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        title_layout.addWidget(back_button)

        self.title_label = QLabel("Di cosa hai bisogno?")
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
        page_layout.addLayout(self.stacklayout)

        btn = QPushButton("Auto")
        btn.pressed.connect(self.go_auto)
        button_layout.addWidget(btn)
        self.widget_auto = PrenotazioneAuto(self.cliente, self)
        self.stacklayout.addWidget(self.widget_auto)

        btn = QPushButton("Moto")
        btn.pressed.connect(self.go_moto)
        button_layout.addWidget(btn)
        self.widget_moto = PrenotazioneMoto(self.cliente, self)
        self.stacklayout.addWidget(self.widget_moto)

        btn = QPushButton("Van")
        btn.pressed.connect(self.go_van)
        button_layout.addWidget(btn)
        self.widget_van = PrenotazioneVan(self.cliente, self)
        self.stacklayout.addWidget(self.widget_van)

        btn = QPushButton("Furgone")
        btn.pressed.connect(self.go_furgone)
        button_layout.addWidget(btn)
        self.widget_furgone = PrenotazioneFurgone(self.cliente, self)
        self.stacklayout.addWidget(self.widget_furgone)

        self.central_widget.setLayout(page_layout)

    def go_back(self):
        from viste.viste_utente.home import VistaHome
        self.vista = VistaHome(self.cliente)
        self.vista.show()
        self.close()

    def go_auto(self):
        self.stacklayout.setCurrentIndex(0)

    def go_moto(self):
        self.stacklayout.setCurrentIndex(1)

    def go_van(self):
        self.stacklayout.setCurrentIndex(2)

    def go_furgone(self):
        self.stacklayout.setCurrentIndex(3)
