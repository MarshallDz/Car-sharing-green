from Noleggio.mezzo import Mezzo
from Noleggio import furgone_path

class Furgone(Mezzo):
    def __init__(self):
        self.file = furgone_path

        super().__init__()
        self.stato = "disponibile"
        self.tariffaOraria = ""

    def aggiungiFurgone(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            furgoni = self.get_dati()
            nuovoFurgone = self.__dict__.copy()
            del nuovoFurgone['file']
            furgoni.append(nuovoFurgone)
            self.writeData(self.file, furgoni)

            print("Furgone aggiunto correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def get_dati(self):
        return self.readData(self.file)

    def eliminaFurgone(self, furgone):
        try:
            self.eliminaMezzo(self.file, furgone)
            print("Furgone eliminato correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def cercaFurgone(self, furgone):
        return self.searchById(self.file, furgone)

