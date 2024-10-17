from Noleggio.mezzo import Mezzo
from Noleggio import auto_path

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
            del nuovaAuto['file']
            auto.append(nuovaAuto)
            self.writeData(self.file, auto)

            print("Auto aggiunta correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def eliminaAuto(self, auto):
        try:
            self.eliminaMezzo(auto_path, auto)
            print("Auto eliminata correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def cercaAuto(self, auto):
        return self.searchById(auto_path, auto)

    def get_dati(self):
        return self.readData(auto_path)

