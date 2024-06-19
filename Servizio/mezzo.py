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

    def getInfoMezzo(self):
        with open(url, "r") as file:
            data = json.load(file)
            mezzi = data.get([])
            return mezzi
