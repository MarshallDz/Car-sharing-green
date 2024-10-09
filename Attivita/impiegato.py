from PyQt5.QtWidgets import QMessageBox
from Attivita.utilizzatore import Utilizzatore


class Impiegato(Utilizzatore):
    def __init__(self):
        super().__init__()
        self.dataAssunzione = ""
        self.stipendio = ""
        self.file = "dati/impiegati.json"

    def aggiungiImpiegato(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare, stipendio, dataAssunzione):
        self.aggiungiUtilizzatore(codiceFiscale, nome, cognome, dataNascita, email, password, cellulare)
        self.stipendio = stipendio
        self.dataAssunzione = dataAssunzione

        # controllo se l'impiegato esiste gia
        impiegati = self.get_dati()

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

    def get_dati(self):
        return self.readData(self.file)