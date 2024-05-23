import json
import os
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
        # ottengo il path assoluto del file in cui salvare
        absolute_path = os.path.dirname(__file__)
        relative_path = "dati/prenotazioni.json"
        dir_list = absolute_path.split(os.sep)
        dir_list.pop()
        new_dir = os.sep.join(dir_list)
        self.url = os.path.join(new_dir, relative_path)

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
        nuovaPrenotazione = self.__dict__.copy()
        nuovaPrenotazione.popitem()
        prenotazioni.append(nuovaPrenotazione)
        with open(self.url, "w") as f:
            json.dump({"prenotazioni": prenotazioni}, f, indent=4)

    def eliminaPrenotazione(self, p):
        url_prenotazioni = "./dati/prenotazioni.json"
        url_clienti = "./dati/clienti.json"
        url_pagamenti = "./dati/pagamenti.json"

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
        from viste.viste_utente.visualizzaPrenotazioni import PrenotazioniView
        self.vista = PrenotazioniView(p['cliente']['email'], p['cliente']['password'])
        self.vista.show()

    def get_dati(self):
        with open(self.url, "r") as file:
            data = json.load(file)
            prenotazioni = data.get("prenotazioni", [])
            return prenotazioni

    def set_id(self):
        # Creazione di una stringa contenente lettere minuscole, lettere maiuscole e numeri
        caratteri = string.ascii_letters + string.digits
        # Generazione della stringa casuale di 6 caratteri
        stringa_random = ''.join(random.choice(caratteri) for _ in range(6))
        return stringa_random

    def aggiornaValori(self, nc, dataP, p, dI, dF, m, t):
        with open(self.url, "r") as f:
            data = json.load(f)
            prenotazioni = data.get("prenotazioni", [])
            for prenotazione in prenotazioni:
                if nc[0] == prenotazione["cliente"]["nome"] and nc[1] == prenotazione["cliente"]["cognome"]:
                    prenotazione["data_prenotazione"] = dataP
                    prenotazione["polizza"] = p
                    prenotazione["data_inizio"] = dI
                    prenotazione["data_fine"] = dF
                    prenotazione["tariffa"] = t
            with open(self.url, "w") as f:
                json.dump({"prenotazioni": prenotazioni}, f, indent=4)

    def controllo_assegnamento_mezzo(self, mezzo, data_inizio=None, data_fine=None):
        prenotazioni = self.get_dati()
        validita = True
        inizio = None
        fine = None
        if not prenotazioni:
            return validita, inizio, fine
        for prenotazione in prenotazioni:
            if prenotazione["mezzo"] == mezzo:
                if (data_inizio >= prenotazione["data_inizio"] and data_inizio <= prenotazione["data_fine"]
                        or data_fine >= prenotazione["data_inizio"] and data_fine <= prenotazione["data_fine"]
                        or data_inizio <= prenotazione["data_inizio"] and data_fine >= prenotazione["data_fine"]):
                    validita = False
                    inizio = prenotazione["data_inizio"]
                    fine = prenotazione["data_fine"]
                else:
                    if mezzo["stato"] != "non disponibile":
                        mezzo["stato"] = "prenotato"
        return validita, inizio, fine