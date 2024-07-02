import darkdetect
from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QMainWindow, QApplication, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QGridLayout

from viste.viste_amministratore.stat1 import stat1
from viste.viste_amministratore.stat2 import stat2
from viste.viste_amministratore.stat3 import stat3
from viste.viste_amministratore.stat4 import stat4


class VistaStatistiche(QMainWindow):
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
        self.central_widget.setLayout(self.central_layout)

        title_layout = QHBoxLayout()
        back_button = QPushButton()
        back_button.setStyleSheet("max-width: 100px; border: none")
        back_button.setIcon(QIcon("viste/Icone/varie/back.png"))
        back_button.setIconSize(QSize(50, 50))
        back_button.clicked.connect(self.go_back)
        title_layout.addWidget(back_button)

        title_label = QLabel("Statistiche")
        title_font = title_label.font()
        title_font.setPointSize(42)
        title_font.setBold(True)
        title_label.setFont(title_font)
        title_label.adjustSize()
        title_label.setAlignment(Qt.AlignCenter)
        title_layout.addWidget(title_label)

        ghost_button = QPushButton()
        ghost_button.setStyleSheet("max-width: 100px; border: none")
        title_layout.addWidget(ghost_button)

        self.central_layout.addLayout(title_layout)

        stats_layout = QGridLayout()
        # numero prenotazioni al momento (divise per tipo veicolo)
        stats_layout.addWidget(stat1(), 0, 0)
        # numero prenotazioni per cliente
        stats_layout.addWidget(stat2(), 0, 1)
        # incassi totali
        stats_layout.addWidget(stat3(), 1, 0)
        # numero veicoli disponibili al momento
        stats_layout.addWidget(stat4(), 1, 1)
        self.central_layout.addLayout(stats_layout)

    def go_back(self):
        from viste.viste_amministratore.admin import VistaAmministrazione
        self.vista = VistaAmministrazione()
        self.vista.show()
        self.close()
