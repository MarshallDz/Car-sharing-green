from Servizio.mezzo import Mezzo


class Auto(Mezzo):
    def __init__(self):
        self.file = "dati/auto.json"

        super().__init__()
        self.stato = "disponibile"
        self.tariffaOraria = ""

    def aggiungiAuto(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            auto = self.get_dati()
            nuovaAuto = self.__dict__.copy()
            del nuovaAuto['file']
            auto.append(nuovaAuto)
            self.writeData(self.file, auto)

            print("Auto aggiunta correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def eliminaAuto(self, auto):
        try:
            self.eliminaMezzo(self.file, auto)
            print("Auto eliminata correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def cercaAuto(self, auto):
        return self.searchById(self.file, auto)

    def get_dati(self):
        return self.readData(self.file)

    def controllaPrenotazione(self):
        pass
