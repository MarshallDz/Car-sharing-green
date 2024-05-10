import datetime
import json
from PyQt5.QtWidgets import QWidget, QMessageBox
from Attivita.utilizzatore import Utilizzatore
import os

class Cliente(Utilizzatore):

    def __init__(self):
        super().__init__()
        self.prenotazioni = []
        self.dataRegistrazione = ""

    def aggiungiCliente(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare):
        self.aggiungiUtilizzatore(codiceFiscale, nome, cognome, dataNascita, email, password, cellulare)
        self.dataRegistrazione = datetime.datetime.now().strftime("%d%m%Y")

        # controllo se il cliente esiste gia
        clienti = self.get_dati()  # Ottieni la lista dei clienti
        for cliente_esistente in clienti:
            if cliente_esistente["codiceFiscale"] == self.codiceFiscale:
                QMessageBox.warning(None, "Cliente esistente", "Il cliente esiste già.")
                return
        clienti.append(self.__dict__)

        # salvo nel file
        with open("../dati/clienti.json", "w") as f:
            json.dump({"clienti": clienti}, f, indent=4)
        QMessageBox.information(None, "Success", "Account registrato correttamente!")
        return 1

    def get_prenotazione(self, cf):
        lista_prenotazioni = []
        file_path = "dati/prenotazioni.json"
        with open(file_path) as file:
            data = json.load(file)

            for value in data['prenotazioni']:
                if value["cliente"]['codiceFiscale'] == cf:
                    lista_prenotazioni.append(value)

        return lista_prenotazioni

    def get_login(self):
        email = []
        psw = []
        file_path = "dati/clienti.json"
        with open(file_path, "r") as file:
            data = json.load(file)
            for e in data["clienti"]:
                email.append(e["email"])
            for p in data["clienti"]:
                psw.append(p["password"])
        return email, psw

    def get_dati(self, email=None, password=None):
        file_path = "/Users/michelemarzioni/Documents/Python/dati/clienti.json"
        with open(file_path) as file:
            data = json.load(file)
            if not email and not password:
                clienti = data.get("clienti", [])
                return clienti
            else:
                for u in data["clienti"]:
                    if u["email"] == email and u["password"] == password:
                        cliente = u
                        return cliente

    def set_prenotazioni_cliente(self, user, psw, id):
        # Carica i dati dei clienti dal file JSON
        with open("dati/clienti.json", "r") as file:
            data = json.load(file)

        # Cerca il cliente specifico usando il suo codice fiscale
        for cliente in data["clienti"]:
            if cliente["email"] == user and cliente["password"] == psw:
                # Aggiungi il codice della nuova prenotazione alla lista delle prenotazioni del cliente
                cliente["prenotazioni"].append(id)
                break

        # Scrivi i dati aggiornati nel file JSON
        with open("dati/clienti.json", "w") as file:
            json.dump(data, file, indent=4)



