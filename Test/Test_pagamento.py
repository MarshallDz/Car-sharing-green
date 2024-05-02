import unittest
import json
import time
# Import the Pagamento class from your code
from Attivita.pagamento import Pagamento

class TestPagamento(unittest.TestCase):
    def setUp(self):
        # Create a Pagamento instance for testing
        self.pagamento = Pagamento()


    def test_init(self):
        # Test if attributes are initialized correctly
        self.assertEqual(self.pagamento.codice, "")
        self.assertEqual(self.pagamento.totale, "")
        self.assertEqual(self.pagamento.dataPagamento, "")
        self.assertEqual(self.pagamento.prenotazione, "")
        self.assertEqual(self.pagamento.cliente, "")
        self.assertEqual(self.pagamento.statoPagamento, "da pagare")

    def test_aggiungiPagamento(self):
        # Create sample data for a payment
        data = ""
        prenotazione = {"id": "123", "tariffa": "giornaliera", "data_inizio": "2024-05-02 10.00", "data_fine": "2024-05-03 10.00",
                        "mezzo": {"tariffa_oraria": 10}, "polizza": "rca"}
        cliente = {"codiceFiscale": "ABC123"}

        result = self.pagamento.aggiungiPagamento(data, prenotazione, cliente)
        self.assertTrue(result)

        with open('../dati/pagamenti.json') as f:
            data = json.load(f)
            self.assertTrue(any(pagamento["cliente"] == "ABC123" for pagamento in data["pagamenti"]))
        pagamenti = self.pagamento.get_dati()
        if pagamenti[-1]["cliente"] == "ABC123":
            pagamenti.pop()
        with open("../dati/pagamenti.json", "w") as f:
            json.dump({"pagamenti": pagamenti}, f, indent=4)


    def test_calcolaTotale(self):
        # Test calculation of total amount for a reservation
        prenotazione_giornaliera = {"tariffa": "giornaliera", "data_inizio": "2024-05-02 10.00", "data_fine": "2024-05-03 10.00", "mezzo": {"tariffa_oraria": 10}, "polizza": "rca"}
        total_giornaliera = self.pagamento.calcolaTotale(prenotazione_giornaliera)
        self.assertEqual(total_giornaliera, 270)

        # Test calculation of total amount for a reservation with undefined tariff
        prenotazione_indefinita = {"tariffa": "indefinita"}
        total_indefinita = self.pagamento.calcolaTotale(prenotazione_indefinita)
        self.assertEqual(total_indefinita, 'da definire')

