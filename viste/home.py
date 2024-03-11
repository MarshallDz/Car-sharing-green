from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from viste.areacliente import VistaCliente
from Attivita.cliente import Cliente
from viste.prenotazione import VistaPrenotazione
from viste.visualizzaPrenotazioni import PrenotazioniView
import darkdetect


class VistaHome(QMainWindow):
    def __init__(self, user, psw):
        super().__init__()
        self.user = user
        self.psw = psw

        self.setWindowTitle("Home")
        self.setGeometry(0, 0, QApplication.desktop().width(), QApplication.desktop().height())
        if(darkdetect.isDark()):
            self.setStyleSheet("background-color: #121212;")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        form_layout = QHBoxLayout()
        self.central_widget.setLayout(form_layout)

        left_layout = QVBoxLayout()
        left_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        cliente_button = QPushButton("Area clienti")
        cliente_button.setStyleSheet("max-width: 200px;")
        cliente_button.setIcon(QIcon("viste/Icone/boy.png"))
        cliente_button.setIconSize(QSize(50, 50))

        cliente_button.clicked.connect(self.area_clienti)
        left_layout.addWidget(cliente_button)
        form_layout.addLayout(left_layout)

        center_layout = QVBoxLayout()
        center_layout.setAlignment(Qt.AlignTop)
        self.title_label = QLabel("Home")
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_font = QFont("Arial", 42, QFont.Bold)
        self.title_label.setFont(self.title_font)
        self.title_label.adjustSize()
        center_layout.addWidget(self.title_label)

        options_layout = QVBoxLayout()
        button1 = QPushButton("Nuova prenotazione")
        button1.setStyleSheet(
            "width: 500px; height: 75px; background-color: #D9D9D9; border-radius: 5px; padding: 10px; "
            "margin-top: 100px;")
        button1.clicked.connect(self.go_registrazione)
        button2 = QPushButton("Visualizza prenotazioni")
        button2.setStyleSheet(
            "width: 500px; height: 75px; background-color: #D9D9D9; border-radius: 5px; color: black; padding: 10px; ")
        button2.clicked.connect(self.go_visualizza_prenotazioni)
        button3 = QPushButton("Visualizza pagamenti")
        button3.setStyleSheet(
            "width: 500px; height: 75px; background-color: #D9D9D9; border-radius: 5px; color: black; padding: 10px;")

        options_layout.addWidget(button1)
        options_layout.addWidget(button2)
        options_layout.addWidget(button3)
        options_layout.setSpacing(50)
        center_layout.addLayout(options_layout)
        form_layout.addLayout(center_layout)

        right_layout = QVBoxLayout()
        right_layout.setAlignment(Qt.AlignTop | Qt.AlignRight)
        back_button = QPushButton("Esci")
        back_button.setStyleSheet("max-width: 200px; color:")
        back_button.setIcon(QIcon("viste/Icone/logout.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        right_layout.addWidget(back_button)
        form_layout.addLayout(right_layout)

        # self.animation1 = QPropertyAnimation(button1, b"pos")
        # self.animation1.setDuration(150)
        # self.animation1.setEndValue()
        # self.animation1.setEasingCurve(QEasingCurve.InOutCubic)
        # button1.clicked.connect(self.clickAnimation)

    def clickAnimation(self):
        self.animation1.start()

    def area_clienti(self):
        cliente = Cliente.get_dati(self, self.user, self.psw)
        self.area = VistaCliente(cliente)
        self.area.show()

    def go_registrazione(self):
        self.area = VistaPrenotazione(self.user, self.psw)
        self.area.show()
        self.close()

    def go_visualizza_prenotazioni(self):
        self.vista = PrenotazioniView(self.user, self.psw)
        self.vista.show()

    def go_back(self):
        from viste.login import VistaLogin
        self.vista = VistaLogin()
        self.vista.show()
        self.close()