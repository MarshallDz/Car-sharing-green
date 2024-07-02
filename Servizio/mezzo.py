import json


class Mezzo:

    def __init__(self):
        self.immagine = ""
        self.telaio = ""
        self.produttore = ""
        self.modello = ""
        self.anno = ""
        self.cavalli = ""
        self.cilindrata = ""
        self.nPosti = ""
        self.cambio = ""
        self.alimentazione = ""

    def aggiungiMezzo(self, url, telaio, produttore, modello, anno, cavalli, cilindrata, nPosti, cambio, alimentazione):
        self.immagine = url
        self.telaio = telaio
        self.produttore = produttore
        self.modello = modello
        self.anno = anno
        self.cavalli = cavalli
        self.cilindrata = cilindrata
        self.nPosti = nPosti
        self.cambio = cambio
        self.alimentazione = alimentazione

    def eliminaMezzo(self, file, mezzo):
        self.searchById(file, mezzo, True)

    def searchById(self, file, mezzo, delete=False):
        data = self.readData(file)
        for m in data:
            if m["telaio"] == mezzo.telaio:
                if delete:
                    data.remove(m)
                    self.writeData(file, data)
                return 1

    def setStato(self, stato):
        if stato == "disponibile":
            stato = "prenotato"
        else:
            stato = "disponibile"
        return stato

    def writeData(self, file, data):
        with open(file, 'w') as file:
            json.dump(data, file, indent=4)

    def readData(self, file):
        with open(file, "r") as file:
            data = json.load(file)
            return data
