from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json

class Van(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""
        self.stato = "disponibile"

    def aggiungiVan(self, to, url, t, prod, mod, anno, cv, cc, np, c, a):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            # Apre il file JSON in modalità append
            with open("dati/van.json", 'a') as file:
                # Scrive il dizionario dell'auto nel file JSON
                json.dump(self, file, indent=4)
                # Aggiunge un nuovo line feed dopo ogni auto per mantenere ogni auto su una riga separata
                file.write('\n')
            print("van aggiunta correttamente.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def getInfoVan(self):
        info = self.getInfoMezzo()
        info["tariffa_oraria"] = self.tariffaOraria
        return info

    def eliminaVan(self):
        pass

    def cercaVan(self):
        pass
    def controllaPrenotazione(self):
        pass
