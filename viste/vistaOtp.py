import json
import sys

import pyotp
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QMainWindow, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtGui import QPixmap, QImage
import qrcode
from io import BytesIO


class QRCodeGenerator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Generatore QR CarGreen")

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout()
        self.central_widget.setLayout(self.layout)

        # Campo di inserimento email
        self.email_input = QLineEdit(self)
        self.email_input.setPlaceholderText("Inserisci la tua email")
        self.layout.addWidget(self.email_input)

        # Bottone di invio
        self.submit_button = QPushButton("Verifica email", self)
        self.submit_button.clicked.connect(self.generate_qr)
        self.layout.addWidget(self.submit_button)

        # Label per visualizzare il QR code
        self.qr_label = QLabel(self)
        self.layout.addWidget(self.qr_label)

        # Campo di inserimento OTP (inizialmente nascosto)
        self.otp_input = QLineEdit(self)
        self.otp_input.setPlaceholderText("Inserisci il codice OTP")
        self.layout.addWidget(self.otp_input)
        self.otp_input.setVisible(False)

        # Bottone per verificare OTP (inizialmente nascosto)
        self.verify_button = QPushButton("Verifica OTP", self)
        self.verify_button.clicked.connect(self.verify_otp)
        self.layout.addWidget(self.verify_button)
        self.verify_button.setVisible(False)

        # Label per visualizzare il QR code
        self.qr_label = QLabel(self)
        self.layout.addWidget(self.qr_label)

    def generate_qr(self):
        email = self.email_input.text().strip()
        if not email:
            QMessageBox.warning(self, "Errore", "Inserisci una email valida.")
            return
        if not self.controllo_email_esistente():
            QMessageBox.warning(self, "Errore", "L'indirizzo inserito non esiste.")
            return
        if not self.controllo_associazione():
            self.key = pyotp.random_base32()
            nuova_associazione = {"email": email, "key": self.key}
            with open("dati/otpCode.json", "r") as f:
                data = json.load(f)
                associazioni = data.get("codici", [])
                associazioni.append(nuova_associazione)

            with open("dati/otpCode.json", "w") as f:
                json.dump({"codici": associazioni}, f, indent=4)
            # Genera il codice QR
            auth_url = pyotp.totp.TOTP(self.key).provisioning_uri(name=email, issuer_name='CarGreen')

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )
            qr.add_data(auth_url)
            qr.make(fit=True)

            img = qr.make_image(fill='black', back_color='white')
            buffer = BytesIO()
            img.save(buffer)
            qimage = QImage()
            qimage.loadFromData(buffer.getvalue())

            pixmap = QPixmap.fromImage(qimage)
            self.qr_label.setPixmap(pixmap)

        # Mostra i campi per l'inserimento e la verifica dell'OTP
        self.otp_input.setVisible(True)
        self.verify_button.setVisible(True)

    def verify_otp(self):
        otp = self.otp_input.text().strip()
        if not otp:
            QMessageBox.warning(self, "Errore", "Inserisci un codice OTP valido.")
            return

        if self.controllo_associazione():
            totp = pyotp.TOTP(self.chiave)
        else:
            totp = pyotp.TOTP(self.key)
        if totp.verify(otp):
            QMessageBox.information(self, "Successo", "OTP verificato con successo!")
            # Procedi con il login o altre azioni necessarie
            finestre = self.get_open_windows()
            for finestra in finestre:
                if finestra.windowTitle() == "CarGreen":
                    finestra.close()
            from viste.viste_utente.home import VistaHome
            self.vista = VistaHome(self.cliente)
            self.vista.show()
            self.close()
        else:
            QMessageBox.warning(self, "Errore", "OTP non valido. Riprova.")
            self.otp_input.clear()

    def controllo_email_esistente(self):
        from Attivita.cliente import Cliente
        clienti = Cliente().get_dati()
        for cliente in clienti:
            if self.email_input.text().strip() == cliente["email"]:
                self.cliente = cliente
                return True
        return False

    def controllo_associazione(self):
        with open("dati/otpCode.json", "r") as f:
            data = json.load(f)
            associazioni = data.get("codici", [])
            for associazione in associazioni:
                if self.email_input.text().strip() == associazione["email"]:
                    self.chiave = associazione["key"]
                    return True
            return False

    def get_open_windows(self):
        app = QApplication.instance()
        if not app:
            app = QApplication(sys.argv)
        all_widgets = app.allWidgets()
        open_windows = [widget for widget in all_widgets if isinstance(widget, QMainWindow)]
        return open_windows
