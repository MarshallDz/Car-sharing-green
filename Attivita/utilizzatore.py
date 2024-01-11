import datetime
from abc import abstractmethod

class Utilizzatore:

    def __init__(self):
        self.codiceFiscale = ""
        self.nome = ""
        self.cognome = ""
        self.dataNascita = ""
        self.email = ""
        self.password = ""
        self.cellulare = ""

    def aggiungiUtilizzatore(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare):
        self.codiceFiscale = codiceFiscale
        self.nome = nome
        self.cognome = cognome
        self.dataNascita = dataNascita
        self.password = password
        self.email = email
        self.cellulare = cellulare

    def getInfoUtilizzatore(self):
        return {
            "codice": self.codice,
            "codiceFiscale": self.codiceFiscale,
            "cognome": self.cognome,
            "dataNascita": self.dataNascita,
            "email": self.email,
            "nome": self.nome,
            "telefono": self.telefono
        }

    @abstractmethod
    def ricercaUtilizzatoreNomeCognome(self, nome, cognome):
        pass

    @abstractmethod
    def ricercaUtilizzatoreCF(self, codiceFiscale):
        pass

    @abstractmethod
    def ricercaUtilizzatoreCodice(self, codice):
        pass

    def rimuoviUtilizzatore(self):
        self.codice = -1
        self.codiceFiscale = ""
        self.cognome = ""
        self.dataNascita = datetime.datetime(year=1970, month=1, day=1)
        self.email = ""
        self.nome = ""
        self.telefono = 0