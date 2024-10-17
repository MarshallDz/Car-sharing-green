import unittest
import json
from datetime import datetime

from PyQt5.QtWidgets import QApplication
from Attivita import prenotazione_path
from Attivita.prenotazione import Prenotazione

class TestPrenotazione(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.app = QApplication([])
    def setUp(self):
        self.prenotazione = Prenotazione()

    def tearDown(self):
        prenotazioni = self.prenotazione.readData()
        for prenotazione in prenotazioni:
            if prenotazione["cliente"]["email"] == "test@example.com":
                prenotazioni.remove(prenotazione)
        with open(prenotazione_path, "w") as f:
            json.dump(prenotazioni, f, indent=4)

    def test_aggiungiPrenotazione(self):
        cliente = {"email": "test@example.com", "password": "testpassword"}
        data_prenotazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_inizio = "2024-05-03 10:00:00"
        data_fine = "2024-05-04 10:00:00"
        mezzo = "Auto"
        filiale = "Milano"
        tariffa = "giornaliera"
        polizza = "rca"

        self.prenotazione.aggiungiPrenotazione(cliente, data_prenotazione, data_inizio, data_fine, mezzo, filiale, tariffa, polizza)


        prenotazioni = self.prenotazione.readData()
        prenotazione_data = prenotazioni[-1]
        self.assertEqual(prenotazione_data["cliente"], cliente)
        self.assertEqual(prenotazione_data["data_prenotazione"], data_prenotazione)
        self.assertEqual(prenotazione_data["data_inizio"], data_inizio)
        self.assertEqual(prenotazione_data["data_fine"], data_fine)
        self.assertEqual(prenotazione_data["filiale"], filiale)
        self.assertEqual(prenotazione_data["mezzo"], mezzo)
        self.assertEqual(prenotazione_data["tariffa"], tariffa)
        self.assertEqual(prenotazione_data["polizza"], polizza)

    #per testare elimnaPrenotazione bisogna apportare delle modifiche alla funzione in modo da non aggiornale la UI nella funzione stessa
    """def test_eliminaPrenotazione(self):
        # Create a test reservation
        cliente = {"codiceFiscale": "","email": "test@example.com", "password": "testpassword"}
        data_prenotazione = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        data_inizio = "2024-05-03 10:00:00"
        data_fine = "2024-05-04 10:00:00"
        mezzo = "Auto"
        filiale = "Milano"
        tariffa = "giornaliera"
        polizza = "rca"

        test_prenotazione = {
            "id": "TEST01",
            "cliente": cliente,
            "data_prenotazione": data_prenotazione,
            "data_inizio": data_inizio,
            "data_fine": data_fine,
            "filiale": filiale,
            "mezzo": mezzo,
            "tariffa": tariffa,
            "polizza": polizza
        }

        # Add the test reservation to the JSON file
        with open("../dati/prenotazioni.json", "r") as f:
            data = json.load(f)
            prenotazioni = data.get("prenotazioni", [])
            prenotazioni.append(test_prenotazione)
        with open("../dati/prenotazioni.json", "w") as f:
            json.dump({"prenotazioni": prenotazioni}, f, indent=4)

        # Delete the test reservation
        self.prenotazione.eliminaPrenotazione(test_prenotazione)

        # Check if the reservation is removed from the JSON file
        prenotazioni = self.prenotazione.get_dati()
        self.assertNotIn(test_prenotazione, prenotazioni)"""

