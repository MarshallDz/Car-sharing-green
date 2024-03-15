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
        return {
            "URL_immagine": self.immagine,
            "telaio": self.telaio,
            "produttore": self.produttore,
            "modello": self.modello,
            "anno": self.anno,
            "cavalli": self.cavalli,
            "cilindrata": self.cilindrata,
            "nPosti": self.nPosti,
            "cambio": self.cambio,
            "alimentazione": self.alimentazione
        }
