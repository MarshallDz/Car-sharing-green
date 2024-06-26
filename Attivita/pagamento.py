from datetime import datetime
import json
import random
import string


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
        pagamenti = self.get_dati()
        nuovoPagamento = self.__dict__.copy()
        nuovoPagamento.popitem()
        pagamenti.append(nuovoPagamento)
        self.writeData(pagamenti)
        return 1

    def get_dati(self):
        with open(self.file, "r") as file:
            data = json.load(file)
            pagamenti = data.get("pagamenti", [])
            return pagamenti

    def set_id(self):
        # Creazione di una stringa contenente lettere minuscole, lettere maiuscole e numeri
        caratteri = string.ascii_letters + string.digits
        # Generazione della stringa casuale di 6 caratteri
        stringa_random = ''.join(random.choice(caratteri) for _ in range(6))
        return stringa_random

    def calcolaTotale(self, p):
        if p["tariffa"] == "giornaliera":
            formato = "%Y-%m-%d %H.%M"
            data_inizio = datetime.strptime(p["data_inizio"], formato).date()
            data_fine = datetime.strptime(p["data_fine"], formato).date()
            differenza = data_fine - data_inizio
            ore = differenza.total_seconds() / 3600
            totale = ore * int(p['mezzo']['tariffa_oraria'])
            if p['polizza'] == 'rca':
                totale += 30
            else:
                totale += 50
        else:
            totale = 'da definire'
        return totale

    def eliminaPagamento(self, p, cliente):
        pagamenti = self.get_dati()

        for i in pagamenti:
            if i['cocice'] == p["codice"]:
                pagamenti['codice'].remove(i)
                break

        self.writeData(pagamenti)

        # Aggiorna l'interfaccia utente per visualizzare le prenotazioni aggiornate
        from viste.viste_impiegato.gestionePagamenti import VistaPagamentiImpiegato
        self.vista = VistaPagamentiImpiegato(cliente)
        self.vista.show()

    def writeData(self, data):
        with open(self.file, 'w') as file:
            json.dump({"pagamenti": data}, file, indent=4)
