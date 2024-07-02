from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from Attivita.cliente import Cliente


class stat2(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        data = self.getData()
        label1 = QLabel("Clienti registrati al servizio: " + str(len(data)))
        layout.addWidget(label1)

        for cliente in data:
            label = QLabel(cliente["email"] + " ha prenotato " + str(len(cliente["prenotazioni"])) + " veicoli")
            scroll_layout.addWidget(label)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

    def getData(self):
        file_clienti = "dati/clienti.json"
        data = Cliente().readData(file_clienti)

        return data
