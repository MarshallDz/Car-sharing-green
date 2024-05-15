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

        # ottengo il path assoluto del file in cui salvare
        absolute_path = os.path.dirname(__file__)
        relative_path = "dati/clienti.json"
        dir_list = absolute_path.split(os.sep)
        dir_list.pop()
        new_dir = os.sep.join(dir_list)
        self.url = os.path.join(new_dir, relative_path)

    def aggiungiCliente(self, codiceFiscale, nome, cognome, dataNascita, email, password, cellulare):
        self.aggiungiUtilizzatore(codiceFiscale, nome, cognome, dataNascita, email, password, cellulare)
        self.dataRegistrazione = datetime.datetime.now().strftime("%d%m%Y")

        # controllo se il cliente esiste gia
        clienti = self.get_dati()  # Ottieni la lista dei clienti

        for cliente_esistente in clienti:
            if cliente_esistente["codiceFiscale"] == self.codiceFiscale:
                QMessageBox.warning(None, "Cliente esistente", "Il cliente esiste già.")
                return
        nuovoCliente = self.__dict__.copy()
        nuovoCliente.popitem()
        clienti.append(nuovoCliente)

        # salvo nel file
        with open(self.url, "w") as f:
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
        file_path = "dati/clienti.json"
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

    def eliminaCliente(self, cliente, user, psw):
        with open(self.url, 'r') as file:
            data = json.load(file)

        for client in data['clienti']:
            if client['codiceFiscale'] == cliente["codiceFiscale"]:
                data['clienti'].remove(client)
                break

        with open(self.url, 'w') as file:
            json.dump(data, file, indent=4)

        # Aggiorna l'interfaccia utente per visualizzare le prenotazioni aggiornate
        from viste.viste_impiegato.vistaGestisciClienti import VistaGestioneClienti
        self.vista = VistaGestioneClienti(user, psw)
        self.vista.show()

    def aggiornaValori(self, cc, cf, n, c, dN, e, cel):
        print(cc, cf, n, c, dN, e, cel)
        with open(self.url, "r") as f:
            data = json.load(f)
            clienti = data.get("clienti", [])
            for cliente in clienti:
                if cc["codiceFiscale"] == cliente["codiceFiscale"]:
                    cliente["codiceFiscale"] = cf
                    cliente["nome"] = n
                    cliente["cognome"] = c
                    cliente["dataNascita"] = dN
                    cliente["email"] = e
                    cliente["cellulare"] = cel
            with open(self.url, "w") as f:
                json.dump({"clienti": clienti}, f, indent=4)


