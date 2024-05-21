import json
import os
from PyQt5.QtWidgets import QWidget, QMessageBox

from Attivita.pagamento import Pagamento
from Attivita.prenotazione import Prenotazione
from Attivita.utilizzatore import Utilizzatore


class Impiegato(Utilizzatore):
    def __init__(self):
        super().__init__()
        self.dataAssunzione = ""
        self.stipendio = ""

        # ottengo il path assoluto del file in cui salvare
        absolute_path = os.path.dirname(__file__)
        relative_path = "dati/impiegati.json"
        dir_list = absolute_path.split(os.sep)
        dir_list.pop()
        new_dir = os.sep.join(dir_list)
        self.url = os.path.join(new_dir, relative_path)

    def aggiungiImpiegato(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare, stipendio, dataAssunzione):
        self.aggiungiUtilizzatore(codiceFiscale, nome, cognome, dataNascita, email, password, cellulare)
        self.stipendio = stipendio
        self.dataAssunzione = dataAssunzione
        impiegato = self.__dict__.copy()
        impiegato.popitem()
        # salvo nel file
        with open(self.url, "r") as f:
            data = json.load(f)
            impiegati = data.get("impiegati", [])
            impiegati.append(impiegato)

            # Salva nel file
        with open(self.url, "w") as f:
            json.dump({"impiegati": impiegati}, f, indent=4)
        QMessageBox.information(None, "Success", "Account aggiunto correttamente!")
        return 1

    def get_login(self):
        email = []
        psw = []
        with open(self.url, "r") as file:
            data = json.load(file)
            for e in data["impiegati"]:
                email.append(e["email"])
            for p in data["impiegati"]:
                psw.append(p["password"])
        return email, psw

    def get_dati(self, email=None, password=None):
        with open(self.url) as file:
            data = json.load(file)
            if not email and not password:
                impiegati = data.get("impiegati", [])
                return impiegati
            else:
                for u in data["impiegati"]:
                    if u["email"] == email and u["password"] == password:
                        impiegati = u
                        return impiegati

    def eliminaImpiegato(self, impiegato, user, psw):
        with open(self.url, 'r') as file:
            data = json.load(file)

        for i in data['impiegati']:
            if i['codiceFiscale'] == i["codiceFiscale"]:
                data['impiegati'].remove(i)
                break

        with open(self.url, 'w') as file:
            json.dump(data, file, indent=4)

    def aggiornaValori(self, cc, cf, n, c, dN, e, cel):
        # aggiorno i valori dell'impiegato
        with open(self.url, "r") as f:
            data = json.load(f)
            impiegati = data.get("impiegati", [])
            for impiegato in impiegati:
                if cc["codiceFiscale"] == impiegato["codiceFiscale"]:
                    impiegato["codiceFiscale"] = cf
                    impiegato["nome"] = n
                    impiegato["cognome"] = c
                    impiegato["dataNascita"] = dN
                    impiegato["email"] = e
                    impiegato["cellulare"] = cel
            with open(self.url, "w") as f:
                json.dump({"impiegati": impiegati}, f, indent=4)

        # aggiorno il codice fiscale anche relativo ai pagamenti e prenotazione del cliente
        pagamento = Pagamento()
        pagamenti = pagamento.get_dati()
        for x in pagamenti:
            if cc["codiceFiscale"] == x["cliente"]:
                x["cliente"] = cf
        with open("dati/pagamenti.json", "w") as f:
            json.dump({"pagamenti":pagamenti}, f, indent=4)

            prenotazione = Prenotazione()
            prenotazioni = prenotazione.get_dati()
            for x in prenotazioni:
                if cc["codiceFiscale"] == x["cliente"]["codiceFiscale"]:
                    x["cliente"]["codiceFiscale"] = cf
            with open("dati/prenotazioni.json", "w") as f:
                json.dump({"prenotazioni": prenotazioni}, f, indent=4)