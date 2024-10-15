import json
import random
import string
from datetime import datetime, timedelta
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

        # Se non ci sono prenotazioni, non ci sono conflitti
        if not prenotazioni:
            return validita, inizio, fine

        # Convertiamo le date in oggetti datetime per poter fare confronti
        data_inizio = datetime.strptime(data_inizio, '%Y-%m-%d %H.%M')
        if data_fine != 'da definire':
            data_fine = datetime.strptime(data_fine, '%Y-%m-%d %H.%M')

        for prenotazione in prenotazioni:
            if prenotazione["mezzo"] == mezzo:
                prenotazione_inizio = datetime.strptime(prenotazione["data_inizio"], '%Y-%m-%d %H.%M')

                # Controllo se la prenotazione ha una data di fine 'da definire'
                if prenotazione["data_fine"] == 'da definire':
                    # Verifica che l'inizio della nuova prenotazione sia almeno 3 giorni dopo la prenotazione attuale
                    if data_inizio <= prenotazione_inizio + timedelta(days=3):
                        validita = False
                        inizio = prenotazione["data_inizio"]
                        fine = prenotazione["data_fine"]
                        break
                else:
                    # Se c'è una data di fine, controlliamo la sovrapposizione
                    prenotazione_fine = datetime.strptime(prenotazione["data_fine"], '%Y-%m-%d %H.%M')
                    if data_fine != 'da definire':
                        # Controllo per sovrapposizioni di date
                        if (prenotazione_inizio <= data_inizio <= prenotazione_fine
                                or prenotazione_inizio <= data_fine <= prenotazione_fine
                                or data_inizio <= prenotazione_inizio and data_fine >= prenotazione_fine):
                            validita = False
                            inizio = prenotazione["data_inizio"]
                            fine = prenotazione["data_fine"]
                            break
                    else:
                        if (data_inizio <= prenotazione_inizio + timedelta(days=3)):
                            validita = False
                            inizio = prenotazione["data_inizio"]
                            fine = prenotazione["data_fine"]
                            break

        return validita, inizio, fine

    def aggiorna_stato_mezzo(self, el=False):
        from Noleggio.auto import Auto
        from Noleggio.moto import Moto
        from Noleggio.van import Van
        from Noleggio.furgone import Furgone
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
        self.check = False
        for a in auto:
            if self.mezzo == a:
                self.check = True
                a["stato"] = Auto().setStato(self.mezzo["stato"], 1)
                Auto().writeData(url_auto, auto)
                break
        if not self.check:
            for m in moto:
                if self.mezzo == m:
                    self.check = True
                    m["stato"] = Moto().setStato(self.mezzo["stato"], 1)
                    Moto().writeData(url_moto, moto)
                    break
        if not self.check:
            for v in van:
                if self.mezzo == v:
                    self.check = True
                    v["stato"] = Van().setStato(self.mezzo["stato"], 1)
                    Van().writeData(url_van, van)
                    break
        if not self.check:
            for f in fur:
                if self.mezzo == f:
                    self.check = True
                    f["stato"] = Furgone().setStato(self.mezzo["stato"], 1)
                    Furgone().writeData(url_fur, fur)
                    break

    def verificaScadenzaPrenotazione(self, p):
        ritardo = False
        prenotazioni = self.readData()
        for x in prenotazioni:
            if p["prenotazione"] == x["id"]:
                prenotazione = x
        oggi = datetime.now().strftime("%Y-%m-%d %H.%M")
        if prenotazione["data_fine"] < oggi:
            ritardo = True
        return ritardo

    def writeData(self, data):
        with open(self.file, 'w') as file:
            json.dump(data, file, indent=4)

    def readData(self):
        with open(self.file, "r") as file:
            data = json.load(file)
            return data
