from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from Servizio.auto import Auto
from Servizio.furgone import Furgone
from Servizio.moto import Moto
from Servizio.van import Van


class stat1(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        data = self.getData()

        label = QLabel("Totale veicoli disponibili: " + str(data[4]))
        layout.addWidget(label)

        label1 = QLabel("Auto prenotate: " + str(data[0]))
        layout.addWidget(label1)

        label1 = QLabel("Moto prenotate: " + str(data[1]))
        layout.addWidget(label1)

        label1 = QLabel("Van prenotati: " + str(data[2]))
        layout.addWidget(label1)

        label1 = QLabel("Furgoni prenotati: " + str(data[3]))
        layout.addWidget(label1)

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
