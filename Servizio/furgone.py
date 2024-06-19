from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json


class Furgone(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""
        self.stato = "disponibile"

    def aggiungiFurgone(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            furgone = self.get_dati()
            nuovoFurgone = self.__dict__.copy()
            furgone.append(nuovoFurgone)
            with open("dati/furgoni.json", "w") as f:
                json.dump(furgone, f, indent=4)

            print("Furgone aggiunto correttamente.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def getInfoFurgone(self):
        info = self.getInfoMezzo()
        info["tariffa_oraria"] = self.tariffaOraria
        return info

    def get_dati(self):
        file_path = "dati/furgoni.json"
        with open(file_path) as file:
            data = json.load(file)
            return data

    def eliminaFurgone(self):
        pass

    def cercaFurgone(self):
        pass

    def controllaPrenotazione(self):
        pass
