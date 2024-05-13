from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json

class Moto(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""
        self.stato = "disponibile"

    def aggiungiMoto(self, to, url, t, prod, mod, anno, cv, cc, np, c, a):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            # Apre il file JSON in modalità append
            with open("dati/moto.json", 'a') as file:
                # Scrive il dizionario dell'auto nel file JSON
                json.dump(self, file, indent=4)
                # Aggiunge un nuovo line feed dopo ogni auto per mantenere ogni auto su una riga separata
                file.write('\n')
            print("moto aggiunta correttamente.")
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
