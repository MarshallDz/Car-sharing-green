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
        with open("dati/clienti.json", "w") as f:
            json.dump({"clienti": clienti}, f, indent=4)
        QMessageBox.information(None, "Success", "Account registrato correttamente!")
        return 1
    
    # per ora non serve a nulla
    def get_prenotazione(self, cf):
        lista_prenotazioni = []
        file_path = "dati/prenotazioni.json"
        with open(file_path) as file:
            data = json.load(file)

            for value in data:
                prenotazione = value
                if prenotazione["cliente"] == cf:
                    lista_prenotazioni.append(prenotazione["id"])

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
        file_path = "dati/clienti.json"
        with open(file_path, "r") as file:
            data = json.load(file)
            if not email and not password:
                clienti = data.get("clienti", [])
                return clienti
            else:
                for u in data["clienti"]:
                    if u["email"] == email and u["password"] == password:
                        cliente = u
                        return cliente

    def get_cliente(self, email, password):
        file_path = "dati/clienti.json"
        with open(file_path, "r") as file:
            data = json.load(file)
            for u in data["clienti"]:
                if u["email"] == email and u["password"] == password:
                    cliente = u
                    return cliente
