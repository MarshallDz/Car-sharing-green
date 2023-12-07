import datetime
import json
from PyQt5.QtWidgets import QWidget, QMessageBox
from Attivita.utilizzatore import Utilizzatore

class Cliente(Utilizzatore):

    def __init__(self):
        super().__init__()
        self.prenotazioni = []
        self.dataRegistrazione = ""

    def aggiungiCliente(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare):
        # Controlla che tutti i campi siano compilati
        if not all([codiceFiscale, nome, cognome, dataNascita, email, password, cellulare]):
            QMessageBox.critical(None, "Campi mancanti", "Tutti i campi devono essere compilati.")
            return

        # Controlla se il cellulare è un numero
        if not cellulare.isdigit():
            QMessageBox.warning(None, "Cellulare non valido", "Il numero di cellulare deve essere un numero.")
            return

        self.aggiungiUtilizzatore(codiceFiscale, nome, cognome, dataNascita, email, password, cellulare)
        self.dataRegistrazione = datetime.datetime.now().strftime("%d%m%Y")
        #controllo se il cliente esiste gia
        with open("/Users/michelemarzioni/Documents/Python/dati/clienti.json", "r") as f:
            data = json.load(f)
            clienti = data.get("clienti", [])  # Ottieni la lista dei clienti
        for cliente_esistente in clienti:
                if(cliente_esistente["codiceFiscale"] == self.codiceFiscale):
                    QMessageBox.warning(None, "Cliente esistente", "Il cliente esiste già.")
                    return
        clienti.append(self.__dict__)
        #voglio salvarlo nel file
        with open("/Users/michelemarzioni/Documents/Python/dati/clienti.json", "w") as f:
                json.dump({"clienti": clienti}, f, indent=4)
    
    #per ora non serve a nulla
    def get_prenotazione(self, cf):
        lista_prenotazioni = []
        file_path = "/Users/michelemarzioni/Documents/Python/dati/prenotazioni.json"
        with open(file_path) as file:
            data = json.load(file)

            for value in data:
                prenotazione = value
                if(prenotazione["cliente"] == cf):
                    lista_prenotazioni.append(prenotazione["id"])

        return lista_prenotazioni


