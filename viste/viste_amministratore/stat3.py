from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel

from Attivita.pagamento import Pagamento


class stat3(QWidget):
    def __init__(self):
        super().__init__()

        layout = QVBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)

        data = self.getData()

        label1 = QLabel("Totale incassato: " + str(data[0]))
        label2 = QLabel("Totale non contabilizzato: " + str(data[1]))
        layout.addWidget(label1)
        layout.addWidget(label2)

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
