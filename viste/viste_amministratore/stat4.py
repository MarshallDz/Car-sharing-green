from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QScrollArea, QFrame
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
        scroll_area.setMinimumHeight(300)


        data = self.getData()
        label1 = QLabel("Impiegati dell'azienda: " + str(len(data)))
        layout.addWidget(label1)

        for impiegato in data:
            card = self.createCard(impiegato["email"], str(impiegato["stipendio"]) + "€")
            scroll_layout.addWidget(card)

        scroll_widget.setLayout(scroll_layout)
        scroll_area.setWidget(scroll_widget)
        layout.addWidget(scroll_area)

    def createCard(self, email, stipendio):
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setStyleSheet("background-color: #D9D9D9; border: 2px solid black; border-radius: 5px; padding: 10px;"
                            "color:black")

        layout = QVBoxLayout(frame)

        emailLabel = QLabel(email)
        emailLabel.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        layout.addWidget(emailLabel)

        stipendioLabel = QLabel("Stipendio: " + stipendio)
        stipendioLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(stipendioLabel)

        return frame

    def getData(self):
        file_impiegati = "dati/impiegati.json"
        data = Impiegato().readData(file_impiegati)

        return data
