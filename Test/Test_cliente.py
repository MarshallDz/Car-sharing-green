import unittest
import json
from PyQt5.QtWidgets import QApplication, QMessageBox  # Aggiungi QApplication qui
from Attivita.cliente import Cliente

class TestClienteMethods(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a QApplication instance before running any tests
        cls.app = QApplication([])

    def setUp(self):
        # Initialize a test instance of the Cliente class
        self.cliente = Cliente()

    @classmethod
    def tearDownClass(cls):
        # Clean up any QApplication instance after all tests have run
        del cls.app

    def test_aggiungiCliente(self):
        self.cliente.aggiungiCliente("CF123456", "John", "Doe", "1990-01-01", "john@example.com", "password", "1234567890")
        # Check if the client data is correctly added to the JSON file
        with open('../dati/clienti.json') as f:
            data = json.load(f)
            self.assertTrue(any(cliente["codiceFiscale"] == "CF123456" for cliente in data["clienti"]))

        # Test adding an existing client
        result = self.cliente.aggiungiCliente("CF123456", "Jane", "Doe", "1990-01-01", "jane@example.com", "password", "0987654321")
        # Check if a warning message is shown
        self.assertFalse(result)  # Ensure that the method returns False for existing client
        print("Existing client warning: Il cliente esiste già.")
        # Print statement to indicate that a warning message is shown

    def test_get_prenotazione(self):
        # Add some test bookings
        url = "../dati/prenotazioni.json"
        with open(url, "r") as file:
            data = json.load(file)
            prenotazioni = data.get("prenotazioni", [])
            if prenotazioni[-1]["cliente"]["codiceFiscale"] == "CF123456":
                prenotazioni.pop()
        prenotazione = {"cliente": {"codiceFiscale": "CF123456"}, "id": 1}
        prenotazioni.append(prenotazione)
        with open("../dati/prenotazioni.json", "w") as f:
            json.dump({"prenotazioni": prenotazioni}, f, indent=4)

        # Test retrieving bookings for a specific client
        prenotazioni = self.cliente.get_prenotazione("CF123456")
        self.assertEqual(len(prenotazioni), 1)
        self.assertEqual(prenotazioni[0]["id"], 1)

        # Test retrieving bookings for a non-existent client
        prenotazioni = self.cliente.get_prenotazione("CF000000")
        self.assertEqual(len(prenotazioni), 0)
