import json
from PyQt5.QtWidgets import QMessageBox

from Attivita.pagamento import Pagamento
from Attivita.prenotazione import Prenotazione
from Attivita.utilizzatore import Utilizzatore


class Impiegato(Utilizzatore):
    def __init__(self):
        self.file = "dati/impiegati.json"

        super().__init__()
        self.dataAssunzione = ""
        self.stipendio = ""

    def aggiungiImpiegato(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare, stipendio, dataAssunzione):
        self.aggiungiUtilizzatore(codiceFiscale, nome, cognome, dataNascita, email, password, cellulare)
        self.stipendio = stipendio
        self.dataAssunzione = dataAssunzione

        # controllo se il cliente esiste gia
        impiegati = self.get_dati()  # Ottieni la lista dei clienti

        for impiegato_esistente in impiegati:
            if impiegato_esistente["codiceFiscale"] == self.codiceFiscale:
                QMessageBox.warning(None, "Impiegato esistente", "L'impiegato esiste già.")
                return
        nuovoImpiegato = self.__dict__.copy()
        nuovoImpiegato.popitem()
        impiegati.append(nuovoImpiegato)

        # salvo nel file
        self.writeData(self.file, impiegati)
        QMessageBox.information(None, "Success", "Account registrato correttamente!")
        return 1

    def verificaImpiegato(self, user, password):
        return self.verify_login(self.file, user, password)

    def get_dati(self):
        return self.readData(self.file)

    def eliminaImpiegato(self, impiegato):
        self.eliminaUtilizzatore(self.file, impiegato)

    def aggiornaValori(self, cc, cf, n, c, dN, e, cel):
        # aggiorno i valori dell'impiegato
        data = self.readData(self.file)
        for impiegato in data:
            if cc["codiceFiscale"] == impiegato["codiceFiscale"]:
                impiegato["codiceFiscale"] = cf
                impiegato["nome"] = n
                impiegato["cognome"] = c
                impiegato["dataNascita"] = dN
                impiegato["email"] = e
                impiegato["cellulare"] = cel
            self.writeData(self.file, data)

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
