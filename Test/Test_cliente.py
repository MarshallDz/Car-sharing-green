import unittest
import os
import json
from PyQt5.QtWidgets import QMessageBox
from Attivita.cliente import Cliente

class TestClienteMethods(unittest.TestCase):

    def setUp(self):
        # Initialize a test instance of the Cliente class
        self.cliente = Cliente()

    def tearDown(self):
        # Clean up any test data or files created during testing
        if os.path.exists("dati/clienti.json"):
            os.remove("dati/clienti.json")

    def test_aggiungiCliente(self):
        self.cliente = Cliente()
        self.cliente.aggiungiCliente("CF123456", "John", "Doe", "1990-01-01", "john@example.com", "password", "1234567890")
        clienti = None
        if os.path.isfile('dati/clienti.json'):
            with open('dati/clienti.json', 'r') as f:
                clienti = json.load(f)
        self.assertIsNotNone(clienti)
        self.assertIn(1, clienti)

    def test_get_prenotazione(self):
        # Add some test bookings
        try:
            with open("dati/prenotazioni.json", "w") as f:
                json.dump({"prenotazioni": [{"cliente": {"codiceFiscale": "CF123456"}, "id": 1}, {"cliente": {"codiceFiscale": "CF7891011"}, "id": 2}]},
                          f)
        except:
            print("file not found")

        # Test retrieving bookings for a specific client
        prenotazioni = self.cliente.get_prenotazione("CF123456")
        self.assertEqual(len(prenotazioni), 1)
        self.assertEqual(prenotazioni[0]["id"], 1)

        # Test retrieving bookings for a non-existent client
        prenotazioni = self.cliente.get_prenotazione("CF000000")
        self.assertEqual(len(prenotazioni), 0)

