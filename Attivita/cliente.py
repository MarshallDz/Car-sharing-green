import datetime
import json
from PyQt5.QtWidgets import QWidget, QMessageBox
from Attivita.utilizzatore import Utilizzatore
from Attivita.pagamento import Pagamento
from Attivita.prenotazione import Prenotazione


class Cliente(Utilizzatore):

    def __init__(self):
        self.file = "dati/clienti.json"

        super().__init__()
        self.prenotazioni = []
        self.dataRegistrazione = ""

    def aggiungiCliente(self, cF, no, cog, datN, em, pas, cel):
        self.aggiungiUtilizzatore(cF, no, cog, datN, em, pas, cel)
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
        self.writeData(self.file, clienti)
        QMessageBox.information(None, "Success", "Account registrato correttamente!")
        return 1

    def get_prenotazione(self, cf):
        lista_prenotazioni = []
        file_path = "dati/prenotazioni.json"
        data = self.readData(file_path)
        for value in data['prenotazioni']:
            if value["cliente"]['codiceFiscale'] == cf:
                lista_prenotazioni.append(value)

        return lista_prenotazioni

    def get_dati(self):
        return self.readData(self.file)

    def set_prenotazioni_cliente(self, cliente, idp):
        # Carica i dati dei clienti dal file JSON
        with open(self.file, "r") as file:
            data = json.load(file)

        # Cerca il cliente specifico usando il suo codice fiscale
        for c in data:
            if c["email"] == cliente["email"] and c["password"] == cliente["password"]:
                # Aggiungi il codice della nuova prenotazione alla lista delle prenotazioni del cliente
                c["prenotazioni"].append(idp)
                break

        # Scrivi i dati aggiornati nel file JSON
        self.writeData(self.file, data)

    def verificaCliente (self, user, password):
        return self.verify_login(self.file, user, password)

    def eliminaCliente(self, cliente):
        self.eliminaUtilizzatore(self.file, cliente)

    def cercaCliente(self, cliente):
        return self.searchById(self.file, cliente, False)

    def aggiornaValori(self, cc, cf, n, c, dN, e, cel):
        # aggiorno i valori del cliente
        with open(self.file, "r") as f:
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
        # aggiorno il codice fiscale anche relativo ai pagamenti e prenotazione del cliente
        pagamento = Pagamento()
        pagamenti = pagamento.get_dati()
        for x in pagamenti:
            if cc["codiceFiscale"] == x["cliente"]:
                x["cliente"] = cf
        with open("dati/pagamenti.json", "w") as f:
            json.dump({"pagamenti":pagamenti}, f, indent=4)

            prenotazione = Prenotazione()
            prenotazioni = prenotazione.get_dati()
            for x in prenotazioni:
                if cc["codiceFiscale"] == x["cliente"]["codiceFiscale"]:
                    x["cliente"]["codiceFiscale"] = cf
            with open("dati/prenotazioni.json", "w") as f:
                json.dump({"prenotazioni": prenotazioni}, f, indent=4)

