from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json


class Auto(Mezzo):
    def __init__(self):
        super().__init__()
        self.stato = "disponibile"
        self.tariffaOraria = ""

    def aggiungiAuto(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            auto = self.get_dati()
            nuovaAuto = self.__dict__.copy()
            auto.append(nuovaAuto)
            with open("dati/auto.json", "w") as f:
                json.dump(auto, f, indent=4)

            print("Auto aggiunta correttamente.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def getInfoAuto(self):
        info = self.getInfoMezzo()
        info["tariffa_oraria"] = self.tariffaOraria
        return info

    def get_dati(self):
        file_path = "dati/auto.json"
        with open(file_path) as file:
            data = json.load(file)
            return data

    def eliminaAuto(self):
        pass

    def cercaAuto(self):
        pass

    def controllaPrenotazione(self):
        pass
