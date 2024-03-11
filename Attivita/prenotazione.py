import json
import random
import string
class Prenotazione():
    def __init__(self):
        self.id = ""
        self.cliente = ""
        self.data_prenotazione = ""
        self.data_inizio = ""
        self.data_fine = ""
        self.filiale = ""
        self.mezzo = ""
        self.tariffa = ""
        self.polizza = ""

    def aggiungiPrenotazione(self, cliente, data_prenotazione, data_inizio, data_fine, mezzo,  filiale, tariffa, polizza):
        self.id = self.set_id()
        self.cliente = cliente
        self.data_prenotazione = data_prenotazione
        self.data_inizio = data_inizio
        self.data_fine = data_fine
        self.filiale = filiale
        self.mezzo = mezzo
        self.tariffa = tariffa
        self.polizza = polizza

        """prenotazioni = self.get_dati()
        prenotazioni.append(self.__dict__)
        with open("dati/prenotazioni.json", "w") as f:
            json.dump({"prenotazioni": prenotazioni}, f, indent=4)
        return 1"""

    def eliminaPrenotazione(self, p):
        url = "dati/prenotazioni.json"
        with open(url, "r") as file:
            data = json.load(file)

        # Rimuovi la prenotazione dalla lista se corrisponde a p
        data['prenotazioni'] = [x for x in data['prenotazioni'] if x != p]

        # Scrivi i dati aggiornati nel file JSON
        with open(url, "w") as file:
            json.dump(data, file, indent=4)
        from viste.visualizzaPrenotazioni import PrenotazioniView
        self.vista = PrenotazioniView(p['cliente']['email'], p['cliente']['password'])
        self.vista.show()

    def get_dati(self):
        url = "dati/prenotazioni.json"
        with open(url, "r") as file:
            data = json.load(file)
            prenotazioni = data.get("prenotazioni", [])
            return prenotazioni

    def set_id(self):
        # Creazione di una stringa contenente lettere minuscole, lettere maiuscole e numeri
        caratteri = string.ascii_letters + string.digits
        # Generazione della stringa casuale di 6 caratteri
        stringa_random = ''.join(random.choice(caratteri) for _ in range(6))
        return stringa_random

