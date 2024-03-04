from Attivita.mezzo import Mezzo
import json

class Auto(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""

    def aggiungiAuto(self, to, url, t, prod, mod, anno, cv, cc, np, c, a):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            # Apre il file JSON in modalità append
            with open("dati/auto.json", 'a') as file:
                # Scrive il dizionario dell'auto nel file JSON
                json.dump(self, file, indent=4)
                # Aggiunge un nuovo line feed dopo ogni auto per mantenere ogni auto su una riga separata
                file.write('\n')
            print("Auto aggiunta correttamente.")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def getInfoAuto(self):
        info = self.getInfoMezzo()
        info["tariffa_oraria"] = self.tariffaOraria
        return info

