from datetime import datetime
import json
import random
import string

from PyQt5.QtCore import QDate, Qt


class Pagamento:
    def __init__(self):
        self.codice = ""
        self.totale = ""
        self.dataPagamento = ""
        self.prenotazione = ""
        self.cliente = ""
        self.statoPagamento = "da pagare"

        self.file = "dati/pagamenti.json"

    def aggiungiPagamento(self, data, pren, cliente):
        self.codice = self.set_id()
        self.totale = self.calcolaTotale(pren)
        self.dataPagamento = data
        self.prenotazione = pren["id"]
        self.cliente = cliente['codiceFiscale']
        pagamenti = self.readData()
        nuovoPagamento = self.__dict__.copy()
        nuovoPagamento.popitem()
        pagamenti.append(nuovoPagamento)
        self.writeData(pagamenti)

    def set_id(self):
        # Creazione di una stringa contenente lettere minuscole, lettere maiuscole e numeri
        caratteri = string.ascii_letters + string.digits
        # Generazione della stringa casuale di 6 caratteri
        stringa_random = ''.join(random.choice(caratteri) for _ in range(6))
        return stringa_random

    def calcolaTotale(self, p):
        if p["tariffa"] == "oraria":
            formato = "%Y-%m-%d %H.%M"
            data1 = datetime.strptime(p["data_inizio"], formato)
            data2 = datetime.strptime(p["data_fine"], formato)
            differenza = data2 - data1
            totale = int((differenza.total_seconds() / 3600)) * int(p["mezzo"]["tariffaOraria"])
            if p['polizza'] == 'rca':
                totale += 30
            else:
                totale += 50
        else:
            formato = "%Y-%m-%d %H.%M"
            data_inizio = datetime.strptime(p["data_inizio"], formato)
            data_fine = datetime.strptime(p["data_fine"], formato)
            differenza = (data_fine - data_inizio).days
            totale = differenza * int(int(p['mezzo']['tariffaOraria'])*24*0.7)
            if p['polizza'] == 'rca':
                totale += 30
            else:
                totale += 50
        return totale

    def eliminaPagamento(self, p, cliente):
        pagamenti = self.readData()

        for i in pagamenti:
            if i['cocice'] == p["codice"]:
                pagamenti['codice'].remove(i)
                break

        self.writeData(pagamenti)

        # Aggiorna l'interfaccia utente per visualizzare le prenotazioni aggiornate
        from viste.viste_impiegato.gestionePagamenti import VistaPagamentiImpiegato
        self.vista = VistaPagamentiImpiegato(cliente)
        self.vista.show()

    def verificaPagamento(self, p):
        pagamenti = self.readData()
        for pagamento in pagamenti:
            if pagamento["codice"] == p["codice"]:
                pagamento["statoPagamento"] = "pagato"
                pagamento["dataPagamento"] = QDate.currentDate().toString(Qt.ISODate)
        self.writeData(pagamenti)

    def writeData(self, data):
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4)

    def readData(self):
        with open(self.file, "r") as file:
            data = json.load(file)
            return data
