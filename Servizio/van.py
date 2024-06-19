from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json


class Van(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""
        self.stato = "disponibile"

    def aggiungiVan(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            van = self.get_dati()
            nuovoVan = self.__dict__.copy()
            van.append(nuovoVan)
            with open("dati/van.json", "w") as f:
                json.dump(van, f, indent=4)

            print("Van aggiunto correttamente.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def getInfoVan(self):
        info = self.getInfoMezzo()
        info["tariffa_oraria"] = self.tariffaOraria
        return info

    def get_dati(self):
        file_path = "dati/van.json"
        with open(file_path) as file:
            data = json.load(file)
            return data

    def eliminaVan(self):
        pass

    def cercaVan(self):
        pass
    def controllaPrenotazione(self):
        pass
