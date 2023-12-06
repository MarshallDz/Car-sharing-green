import datetime
import json

from Attivita.utilizzatore import Utilizzatore

class Cliente(Utilizzatore):

    def __init__(self):
        super().__init__()
        self.prenotazioni = []
        self.dataRegistrazione = ""

    def aggiungiCliente(self, nome, telefono, email, cognome, dataNascita, codiceFiscale):
        self.aggiungiUtilizzatore(telefono, nome, email, dataNascita, cognome, codiceFiscale)
        self.dataRegistrazione = datetime.datetime.now()
        clienti = {}

    def get_prenotazione(self, cf):
        file_path = "/Users/michelemarzioni/Documents/Python/dati/prenotazioni.json"
        with open(file_path) as file:
            data = json.load(file)

            for value in data:
                prenotazione = value
                if(prenotazione["cliente"] == cf):
                    print(prenotazione["id"])
                    self.prenotazioni.append(prenotazione["id"])

