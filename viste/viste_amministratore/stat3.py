from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QFrame, QHBoxLayout

from Attivita.pagamento import Pagamento

class stat3(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignLeft)

        data = self.getData()

        card1 = self.createCard("Totale incassato", str(data[0]))
        card2 = self.createCard("Totale non contabilizzato", str(data[1]))

        layout.addWidget(card1)
        layout.addWidget(card2)

    def createCard(self, title, value):
        frame = QFrame()
        frame.setFrameShape(QFrame.Box)
        frame.setStyleSheet("background-color: #D9D9D9; border: 2px solid black; border-radius: 5px; padding: 10px;"
                            "color: black")

        layout = QVBoxLayout(frame)

        titleLabel = QLabel(title)
        titleLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(titleLabel)

        valueLabel = QLabel(value)
        valueLabel.setAlignment(Qt.AlignCenter)
        layout.addWidget(valueLabel)

        return frame

    def getData(self):
        data = Pagamento().readData()

        countp = 0
        countn = 0
        for pagamento in data:
            if pagamento["statoPagamento"] == "pagato":
                countp += int(pagamento["totale"])
            else:
                countn += int(pagamento["totale"])

        return countp, countn
