import unittest
import json
from Attivita.pagamento import Pagamento
from Attivita import pagamento_path
class TestPagamento(unittest.TestCase):
    def setUp(self):
        # Create a Pagamento instance for testing
        self.pagamento = Pagamento()
        self.file = pagamento_path

    def test_aggiungiPagamento(self):
        # Create sample data for a payment
        data = ""
        prenotazione = {"id": "123", "tariffa": "giornaliera", "data_inizio": "2024-05-02 10.00", "data_fine": "2024-05-03 10.00",
                        "mezzo": {"tariffaOraria": 10}, "polizza": "rca"}
        cliente = {"codiceFiscale": "ABC123"}

        self.pagamento.aggiungiPagamento(data, prenotazione, cliente)
        with open(self.file) as f:
            data = json.load(f)
            self.assertTrue(any(pagamento["cliente"] == "ABC123" for pagamento in data))

        pagamenti = self.pagamento.readData()
        if pagamenti[-1]["cliente"] == "ABC123":
            pagamenti.pop()


    def test_calcolaTotale(self):
        prenotazione_giornaliera = {"tariffa": "giornaliera", "data_inizio": "2024-05-02 10.00", "data_fine": "2024-05-03 10.00", "mezzo": {"tariffaOraria": 10}, "polizza": "rca"}
        total_giornaliera = self.pagamento.calcolaTotale(prenotazione_giornaliera)
        self.assertEqual(total_giornaliera, "198€")


        prenotazione_indefinita = {"tariffa": "oraria", "data_inizio": "2024-05-02 10.00", "data_fine": "da definire", "mezzo": {"tariffaOraria": 10}, "polizza": "rca"}
        total_indefinita = self.pagamento.calcolaTotale(prenotazione_indefinita)
        self.assertEqual(total_indefinita, 'da definire')

