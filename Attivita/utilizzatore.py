import datetime
import json
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

    def aggiungiUtilizzatore(self, cF, no, cog, datN, em, pas, cel):
        self.codiceFiscale = cF
        self.nome = no
        self.cognome = cog
        self.dataNascita = datN
        self.password = pas
        self.email = em
        self.cellulare = cel

    def getInfoUtilizzatore(self):
        return {
            "codiceFiscale": self.codiceFiscale,
            "nome": self.nome,
            "cognome": self.cognome,
            "dataNascita": self.dataNascita,
            "email": self.email,
            "telefono": self.cellulare
        }

    def eliminaUtilizzatore(self, file, utilizzatore):
        self.searchById(file, utilizzatore, True)

    def searchById(self, file, utilizzatore, delete=False):
        data = self.readData(file)
        for c in data:
            if c["codiceFiscale"] == utilizzatore["codiceFiscale"]:
                if delete:
                    data.remove(c)
                    self.writeData(file, data)
                return c

    def verify_login(self, file, user, password):
        with open(file, "r") as file:
            data = json.load(file)
            for u in data:
                if u["email"] == user:
                    if u["password"] == password:
                        return u


    @abstractmethod
    def ricercaUtilizzatoreNomeCognome(self, nome, cognome):
        pass

    @abstractmethod
    def ricercaUtilizzatoreCF(self, codiceFiscale):
        pass

    @abstractmethod
    def ricercaUtilizzatoreNominativo(self, nome, cogome):
        pass

    def writeData(self, file, data):
        with open(file, 'w') as file:
            json.dump(data, file, indent=4)

    def readData(self, file):
        with open(file, "r") as file:
            data = json.load(file)
            return data
