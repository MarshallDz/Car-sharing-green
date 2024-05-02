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

        prenotazioni = self.get_dati()
        prenotazioni.append(self.__dict__)
        with open("../dati/prenotazioni.json", "w") as f:
            json.dump({"prenotazioni": prenotazioni}, f, indent=4)
        return 1

    def eliminaPrenotazione(self, p):
        url_prenotazioni = "../dati/prenotazioni.json"
        url_clienti = "../dati/clienti.json"
        url_pagamenti = "../dati/pagamenti.json"

        # Rimuovi la prenotazione dalla lista delle prenotazioni nel file JSON principale
        with open(url_prenotazioni, "r") as file:
            data_prenotazioni = json.load(file)

        if p in data_prenotazioni['prenotazioni']:
            data_prenotazioni['prenotazioni'].remove(p)

        with open(url_prenotazioni, "w") as file:
            json.dump(data_prenotazioni, file, indent=4)

        # Rimuovi la prenotazione dalla lista delle prenotazioni nel file JSON del cliente
        with open(url_clienti, "r") as file:
            data_clienti = json.load(file)

        for cliente_data in data_clienti["clienti"]:
            if cliente_data['email'] == p['cliente']['email'] and cliente_data['password'] == p['cliente']['password']:
                if 'prenotazioni' in cliente_data:
                    cliente_data['prenotazioni'].remove(p['id'])
                    break

        with open(url_clienti, "w") as file:
            json.dump(data_clienti, file, indent=4)

        # Rimuovi il pagamento associato alla prenotazione dalla lista dei pagamenti nel file JSON
        with open(url_pagamenti, "r") as file:
            data_pagamenti = json.load(file)

        updated_pagamenti = [pagamento for pagamento in data_pagamenti['pagamenti'] if pagamento['prenotazione'] != p['id']]

        with open(url_pagamenti, "w") as file:
            json.dump({"pagamenti": updated_pagamenti}, file, indent=4)

        # Aggiorna l'interfaccia utente per visualizzare le prenotazioni aggiornate
        from viste.visualizzaPrenotazioni import PrenotazioniView
        self.vista = PrenotazioniView(p['cliente']['email'], p['cliente']['password'])
        self.vista.show()

    def get_dati(self):
        url = "../dati/prenotazioni.json"
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

