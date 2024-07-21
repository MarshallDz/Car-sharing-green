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
        totale = 0
        if p["tariffa"] == "giornaliera":
            formato = "%Y-%m-%d %H.%M"
            data_inizio = datetime.strptime(p["data_inizio"], formato)
            data_fine = datetime.strptime(p["data_fine"], formato)
            differenza = (data_fine - data_inizio).days
            totale = differenza * int(int(p['mezzo']['tariffaOraria']) * 24 * 0.7)
            if p['polizza'] == 'rca':
                totale += 30
            else:
                totale += 50
        else:
            if p["data_fine"] != "da definire":
                formato = "%Y-%m-%d %H.%M"
                data1 = datetime.strptime(p["data_inizio"], formato)
                data2 = datetime.strptime(p["data_fine"], formato)
                differenza = data2 - data1
                totale = int((differenza.total_seconds() / 3600)) * int(p["mezzo"]["tariffaOraria"])
                if p['polizza'] == 'rca':
                    totale += 30
                else:
                    totale += 50
        return totale

    def eliminaPagamento(self, p, cliente):
        pagamenti = self.readData()
        for i in pagamenti:
            if i['codice'] == p["codice"]:
                pagamenti.remove(i)
                break

        self.writeData(pagamenti)

        # Aggiorna l'interfaccia utente per visualizzare le prenotazioni aggiornate
        from viste.viste_impiegato.gestionePagamenti import VistaPagamentiImpiegato
        self.vista = VistaPagamentiImpiegato(cliente)
        self.vista.show()

    def verificaPagamento(self, p):
        #controllo se devo applicare la mora
        from Attivita.prenotazione import Prenotazione
        pagamenti = self.readData()
        if Prenotazione().verificaScadenzaPrenotazione(p):
            p["totale"] = int(p["totale"]) + 25
            for x in pagamenti:
                if x["codice"] == p["codice"]:
                    x["totale"] = p["totale"]
        #cambio lo stato del pagamento in "pagato"
        for pagamento in pagamenti:
            if pagamento["codice"] == p["codice"]:
                pagamento["statoPagamento"] = "pagato"
                pagamento["dataPagamento"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        self.writeData(pagamenti)

    def writeData(self, data):
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4)


    def readData(self):
        with open(self.file, "r") as file:
            data = json.load(file)
            return data
