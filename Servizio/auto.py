from datetime import datetime

from Servizio.mezzo import Mezzo
from Attivita.prenotazione import Prenotazione
import json

class Auto(Mezzo):
    def __init__(self):
        super().__init__()
        self.tariffaOraria = ""
        self.stato = "disponibile"

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

    def controllaPrenotazione(self):
        oggi = datetime.now().date()
        auto_prenotate_oggi = []

        """with open("dati/prenotazioni.json", "r") as file:
            prenotazioni = json.load(file)
            for prenotazione in prenotazioni['prenotazioni']:
                data_prenotazione = datetime.strptime(prenotazione['data_inizio']).date()
                if data_prenotazione == oggi:
                    auto_prenotate_oggi.append(prenotazione['mezzo'])

        with open("dati/auto.json", "r+") as file:
            auto = json.load(file)
            for a in auto:
                if a['telaio'] in auto_prenotate_oggi:
                    a['stato'] = "prenotato"

            # Torna all'inizio del file e riscrive il JSON aggiornato
            file.seek(0)
            json.dump(auto, file, indent=4)
            file.truncate()

            print("Stati delle auto aggiornati correttamente.")"""
