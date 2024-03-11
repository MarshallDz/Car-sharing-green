import datetime
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

    def aggiungiPagamento(self, data, pren, cliente):
        self.codice = self.set_id()
        self.totale = self.calcolaTotale()
        self.dataPagamento = data
        self.prenotazione = pren
        self.cliente = cliente
        """pagamenti = self.get_dati()
        pagamenti.append(self.__dict__)
        with open("dati/pagamenti.json", "w") as f:
            json.dump({"pagamenti":pagamenti}, f, indent=4)
        return 1"""


    def get_dati(self):
        url = "dati/pagamenti.json"
        with open(url, "r") as file:
            data = json.load(file)
            pagamenti = data.get("pagamenti", [])
            return pagamenti

    def set_id(self):
        # Creazione di una stringa contenente lettere minuscole, lettere maiuscole e numeri
        caratteri = string.ascii_letters + string.digits
        # Generazione della stringa casuale di 6 caratteri
        stringa_random = ''.join(random.choice(caratteri) for _ in range(6))
        return stringa_random

    def calcolaTotale(self):
        print(self.prenotazione.__dict__['tariffa'])
        """if self.prenotazione["tariffa"] == "giornaliera":
            formato = "%Y-%m-%d %H:%M:%S"
            data_inizio = datetime.strptime(self.prenotazione["data_inizio"], formato)
            data_fine = datetime.strptime(self.prenotazione["data_fine"], formato)

            differenza = data_fine - data_inizio
            ore = differenza.total_seconds() / 3600  # 3600 secondi in un'ora
            totale = ore * self.prenotazione['mezzo']['tariffa']
            if self.prenotazione['polizza'] == 'rca':
                totale += 30
            else: totale += 50
        print(totale)
        return totale"""

