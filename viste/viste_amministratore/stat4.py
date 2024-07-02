from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea

from Attivita.impiegato import Impiegato


class stat4(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_widget = QWidget()
        scroll_layout = QVBoxLayout(scroll_widget)

        data = self.getData()
        label1 = QLabel("Impiegati dell'azienda: " + str(len(data)))
        layout.addWidget(label1)

        for impiegato in data:
            label = QLabel(impiegato["email"] + " ha uno stipendio di " + str(impiegato["stipendio"]) + "€")
            scroll_layout.addWidget(label)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

    def getData(self):
        file_impiegati = "dati/impiegati.json"
        data = Impiegato().readData(file_impiegati)

        return data

