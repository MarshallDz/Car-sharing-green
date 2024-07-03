from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QScrollArea, QFrame

from Attivita.cliente import Cliente


class stat2(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea(self)
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOn)
        scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        scroll_area.setMinimumHeight(300)



        scroll_widget = QWidget()
        scroll_layout = QHBoxLayout(scroll_widget)

        data = self.getData()
        label1 = QLabel("Clienti registrati al servizio: " + str(len(data)))
        mainLayout.addWidget(label1)

        for cliente in data:
            card = self.createCard(cliente["email"], str(len(cliente["prenotazioni"])))
            scroll_layout.addWidget(card)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        mainLayout.addWidget(scroll_area)

    def createCard(self, email, prenotazioni):
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setStyleSheet("background-color: #D9D9D9; border: 2px solid black; border-radius: 5px;"
                            "color: black; width: 200px;")

        layout = QVBoxLayout(frame)

        email_label = QLabel(email)
        email_label.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        prenotazioni_label = QLabel("Ha prenotato " + prenotazioni + " veicoli")
        prenotazioni_label.setAlignment(Qt.AlignCenter)

        layout.addWidget(email_label)
        layout.addWidget(prenotazioni_label)

        return frame

    def getData(self):
        file_clienti = "dati/clienti.json"
        data = Cliente().readData(file_clienti)

        return data
