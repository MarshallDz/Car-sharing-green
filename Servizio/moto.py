from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json


class Moto(Mezzo):
    def __init__(self):
        self.file = "dati/moto.json"

        super().__init__()
        self.stato = "disponibile"
        self.tariffaOraria = ""

    def aggiungiMoto(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            moto = self.get_dati()
            nuovaMoto = self.__dict__.copy()
            del nuovaMoto['file']
            moto.append(nuovaMoto)
            self.writeData(self.file, moto)

            print("Moto aggiunta correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def eliminaMoto(self, moto):
        try:
            self.eliminaMezzo(self.file, moto)
            print("Moto eliminata correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def cercaMoto(self, moto):
        return self.searchById(self.file, moto)

    def get_dati(self):
        return self.readData(self.file)


