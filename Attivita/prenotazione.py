import datetime
import json
from PyQt5.QtWidgets import QWidget, QMessageBox

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

    def aggiungiPrenotazione(self, id, cliente, data_prenotazione, data_inizio, data_fine, mezzo,  filiale, tariffa, polizza):
        self.id = id
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
        with open("dati/prenotazioni.json", "w") as f:
            json.dump({"prenotazioni": prenotazioni}, f, indent=4)
        return 1

    def eliminaPrenotazione(self):
        pass

    def get_dati(self):
        url = "dati/prenotazioni.json"
        with open(url, "r") as file:
            data = json.load(file)
            prenotazioni = data.get("prenotazioni", [])
            return prenotazioni