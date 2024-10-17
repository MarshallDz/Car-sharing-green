import os

#path cliente
cliente_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
cliente_path = os.path.join(cliente_path, "dati")
cliente_path = os.path.join(cliente_path, "clienti.json")

prenotazione_path = os.path.normpath(os.getcwd()+ os.sep + os.pardir)
prenotazione_path = os.path.join(prenotazione_path, "dati")
prenotazione_path = os.path.join(prenotazione_path, "prenotazioni.json")

pagamento_path = os.path.normpath(os.getcwd() + os.sep + os.pardir)
pagamento_path = os.path.join(pagamento_path, "dati")
pagamento_path = os.path.join(pagamento_path, "pagamenti.json")