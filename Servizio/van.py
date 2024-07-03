from Servizio.mezzo import Mezzo


class Van(Mezzo):
    def __init__(self):
        self.file = "dati/van.json"

        super().__init__()
        self.stato = "disponibile"
        self.tariffaOraria = ""

    def aggiungiVan(self, url, t, prod, mod, anno, cv, cc, np, c, a, to):
        self.aggiungiMezzo(url, t, prod, mod, anno, cv, cc, np, c, a)
        self.tariffaOraria = to

        try:
            van = self.get_dati()
            nuovoVan = self.__dict__.copy()
            del nuovoVan['file']
            van.append(nuovoVan)
            self.writeData(self.file, van)

            print("Van aggiunto correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def get_dati(self):
        return self.readData(self.file)

    def eliminaVan(self, van):
        try:
            self.eliminaMezzo(self.file, van)
            print("Van eliminato correttamente")
        except Exception as e:
            print(f"Si è verificato un errore: {e}")

    def cercaAuto(self, van):
        return self.searchById(self.file, van)

    def controllaPrenotazione(self):
        pass
