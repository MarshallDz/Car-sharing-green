import os

auto_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir)
auto_path = os.path.join(auto_path, "dati")
auto_path = os.path.join(auto_path, "auto.json")

moto_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir)
moto_path = os.path.join(moto_path, "dati")
moto_path = os.path.join(moto_path, "moto.json")

van_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir)
van_path = os.path.join(van_path, "dati")
van_path = os.path.join(van_path, "van.json")

furgone_path = os.path.normpath(os.path.dirname(os.path.realpath(__file__)) + os.sep + os.pardir)
furgone_path = os.path.join(furgone_path, "dati")
furgone_path = os.path.join(furgone_path, "furgoni.json")