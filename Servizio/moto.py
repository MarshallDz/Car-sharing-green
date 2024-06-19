from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json


class Moto(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""
        self.stato = "disponibile"

    def aggiungiMoto(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            moto = self.get_dati()
            nuovaMoto = self.__dict__.copy()
            moto.append(nuovaMoto)
            with open("dati/moto.json", "w") as f:
                json.dump(moto, f, indent=4)

            print("Moto aggiunta correttamente.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def getInfoMoto(self):
        info = self.getInfoMezzo()
        info["tariffa_oraria"] = self.tariffaOraria
        return info

    def get_dati(self):
        file_path = "dati/moto.json"
        with open(file_path) as file:
            data = json.load(file)
            return data

    def eliminaMoto(self):
        pass

    def cercaMoto(self):
        pass
    def controllaPrenotazione(self):
        pass
