import unittest
import json
from Attivita.cliente import Cliente
from Test import cliente_path, prenotazione_path


class TestCliente(unittest.TestCase):

    def setUp(self):
        self.cliente = Cliente()
        self.file = cliente_path

    def test_aggiungi_cliente(self):
        self.cliente.aggiungiCliente("ABCDEF12G34H567I", "John", "Doe", "1990-01-01", "john@example.com", "password", "1234567890")

        with open(self.file) as f:
            data = json.load(f)
            self.assertTrue(any(cliente["codiceFiscale"] == "ABCDEF12G34H567I" for cliente in data))

        result = self.cliente.aggiungiCliente("ABCDEF12G34H567I", "Jane", "Doe", "1990-01-01", "jane@example.com", "password", "0987654321")

        self.assertFalse(result)
        print("Existing client warning: Il cliente esiste già.")

    def test_get_prenotazione(self):

        url = prenotazione_path
        with open(url, "r") as file:
            data = json.load(file)
            print(len(data))
            prenotazioni = data
            if len(data) != 0:
                if prenotazioni[-1]["cliente"]["codiceFiscale"] == "ABCDEF12G34H567I":
                    prenotazioni.pop()
        prenotazione = {"cliente": {"codiceFiscale": "ABCDEF12G34H567I"}, "id": 1}
        prenotazioni.append(prenotazione)
        with open(prenotazione_path, "w") as f:
            json.dump(prenotazioni, f, indent=4)

        prenotazioni = self.cliente.get_prenotazione("ABCDEF12G34H567I")
        self.assertEqual(len(prenotazioni), 1)
        self.assertEqual(prenotazioni[0]["id"], 1)

        # Prova a recuperare le prenotazioni per un cliente inesistente
        prenotazioni = self.cliente.get_prenotazione("CF000000")
        self.assertEqual(len(prenotazioni), 0)
