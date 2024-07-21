import json
import random
import string
from datetime import datetime

from Attivita.pagamento import Pagamento

class Prenotazione:
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

        self.file = "dati/prenotazioni.json"

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

        prenotazioni = self.readData()
        nuovaPrenotazione = self.__dict__.copy()
        nuovaPrenotazione.popitem()
        prenotazioni.append(nuovaPrenotazione)
        self.writeData(prenotazioni)
        self.aggiorna_stato_mezzo()

    def eliminaPrenotazione(self, p):
        url_clienti = "dati/clienti.json"
        url_pagamenti = "dati/pagamenti.json"

        # Rimuovi la prenotazione dalla lista delle prenotazioni nel file JSON principale
        data_prenotazioni = self.readData()

        if p in data_prenotazioni:
            data_prenotazioni.remove(p)

        self.writeData(data_prenotazioni)

        # Rimuovi la prenotazione dalla lista delle prenotazioni nel file JSON del cliente
        with open(url_clienti, "r") as file:
            data_clienti = json.load(file)

        for cliente_data in data_clienti:
            if cliente_data['email'] == p['cliente']['email'] and cliente_data['password'] == p['cliente']['password']:
                if 'prenotazioni' in cliente_data:
                    cliente_data['prenotazioni'].remove(p['id'])
                    break

        with open(url_clienti, "w") as file:
            json.dump(data_clienti, file, indent=4)

        # Rimuovi il pagamento associato alla prenotazione dalla lista dei pagamenti nel file JSON
        data_pagamenti = Pagamento().readData()

        updated_pagamenti = [pagamento for pagamento in data_pagamenti if pagamento['prenotazione'] != p['id']]

        Pagamento().writeData(updated_pagamenti)

        # Resetta lo stato del mezzo a disponibile
        self.mezzo = p["mezzo"]
        self.aggiorna_stato_mezzo(True)

        # Aggiorna l'interfaccia utente per visualizzare le prenotazioni aggiornate
        from viste.viste_utente.visualizzaPrenotazioni import PrenotazioniView
        self.vista = PrenotazioniView(p['cliente'])
        self.vista.show()

    def set_id(self):
        # Creazione di una stringa contenente lettere minuscole, lettere maiuscole e numeri
        caratteri = string.ascii_letters + string.digits
        # Generazione della stringa casuale di 6 caratteri
        stringa_random = ''.join(random.choice(caratteri) for _ in range(6))
        return stringa_random

    def aggiornaValori(self, nc, dataP, p, dI, dF, m, t):
        data = self.readData()
        for prenotazione in data:
            if nc[0] == prenotazione["cliente"]["nome"] and nc[1] == prenotazione["cliente"]["cognome"]:
                prenotazione["data_prenotazione"] = dataP
                prenotazione["polizza"] = p
                prenotazione["data_inizio"] = dI
                prenotazione["data_fine"] = dF
                prenotazione["tariffa"] = t
        self.writeData(data)

    def controllo_assegnamento_mezzo(self, mezzo, data_inizio=None, data_fine=None):
        prenotazioni = self.readData()
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
        return validita, inizio, fine

    def aggiorna_stato_mezzo(self, el=False):
        from Servizio.auto import Auto
        from Servizio.moto import Moto
        from Servizio.van import Van
        from Servizio.furgone import Furgone
        url_auto = "dati/auto.json"
        url_moto = "dati/moto.json"
        url_van = "dati/van.json"
        url_fur = "dati/furgoni.json"
        auto = Auto().get_dati()
        moto = Moto().get_dati()
        van = Van().get_dati()
        fur = Furgone().get_dati()
        # per come è costruita p, l'if serve a verificare se la chiamata della funzione arriva da eliminaPrenotazione
        if el:
            self.mezzo["stato"] = "prenotato"
        for a in auto:
            if self.mezzo == a:
                a["stato"] = Auto().setStato(self.mezzo["stato"])
            Auto().writeData(url_auto, auto)
        for m in moto:
            if self.mezzo == m:
                m["stato"] = Moto().setStato(self.mezzo["stato"])
            Moto().writeData(url_moto, moto)
        for v in van:
            if self.mezzo == v:
                v["stato"] = Van().setStato(self.mezzo["stato"])
            Van().writeData(url_van, van)
        for f in fur:
            if self.mezzo == f:
                f["stato"] = Furgone().setStato(self.mezzo["stato"])
            Furgone().writeData(url_fur, fur)

    def verificaScadenzaPrenotazione(self, p):
        ritardo = False
        prenotazioni = self.readData()
        for x in prenotazioni:
            if p["prenotazione"] == x["id"]:
                prenotazione = x
        oggi = datetime.now().strftime("%Y-%m-%d %H:%M")
        if prenotazione["data_fine"] <= oggi and p["statoPagamento"] == "da pagare":
            ritardo = True
        return ritardo

    def writeData(self, data):
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4)

    def readData(self):
        with open(self.file, "r") as file:
            data = json.load(file)
            return data
