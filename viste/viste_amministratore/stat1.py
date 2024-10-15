from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QFrame
from Noleggio.auto import Auto
from Noleggio.furgone import Furgone
from Noleggio.moto import Moto
from Noleggio.van import Van


class stat1(QWidget):
    def __init__(self):
        super().__init__()

        mainLayout = QVBoxLayout(self)
        mainLayout.setAlignment(Qt.AlignLeft)

        cardLayout = QHBoxLayout()
        cardLayout.setAlignment(Qt.AlignLeft)

        data = self.getData()

        cardLayout.addWidget(self.createCard("Totale veicoli disponibili", str(data[4])))
        cardLayout.addWidget(self.createCard("Auto prenotate", str(data[0])))
        cardLayout.addWidget(self.createCard("Moto prenotate", str(data[1])))
        cardLayout.addWidget(self.createCard("Van prenotati", str(data[2])))
        cardLayout.addWidget(self.createCard("Furgoni prenotati", str(data[3])))

        mainLayout.addLayout(cardLayout)

    def createCard(self, title, value):
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setStyleSheet("background-color: #D9D9D9; border: 2px solid ; border-radius: 5px; padding: 10px; color: black;")

        layout = QVBoxLayout(frame)

        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignCenter)
        valueLabel = QLabel(value)
        valueLabel.setAlignment(Qt.AlignCenter)

        layout.addWidget(titleLabel)
        layout.addWidget(valueLabel)

        return frame

    def getData(self):
        file_auto = "dati/auto.json"
        file_moto = "dati/moto.json"
        file_van = "dati/van.json"
        file_furgone = "dati/furgoni.json"
        auto = Auto().readData(file_auto)
        moto = Moto().readData(file_moto)
        van = Van().readData(file_van)
        furgoni = Furgone().readData(file_furgone)

        countot = 0
        counta = 0
        for a in auto:
            countot += 1
            if a["stato"] == "prenotato":
                counta += 1
        countm = 0
        for m in moto:
            countot += 1
            if m["stato"] == "prenotato":
                countm += 1
        countv = 0
        for v in van:
            countot += 1
            if v["stato"] == "prenotato":
                countv += 1
        countf = 0
        for f in furgoni:
            countot += 1
            if f["stato"] == "prenotato":
                countf += 1

        return counta, countm, countv, countf, countot
