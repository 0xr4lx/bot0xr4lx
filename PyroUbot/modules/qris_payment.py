import requests
from PIL import Image
from io import BytesIO

class QRISPayment:
    def __init__(self, *, token, apikey, merchant, qris_data):
        self.token = token
        self.apikey = apikey
        self.merchant = merchant
        self.qris_data = qris_data

    def generate_qr(self, amount):
        url = "http://api.ranz.my.id/createqris"
        params = {
            "nominal": amount,
            "token": self.token,
            "qris": self.qris_data
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("statusCode") != 200:
            raise Exception(data.get("message", "Gagal generate QR"))

        qr_url = data["data"].get("qrImageUrl")
        if not qr_url:
            raise Exception("QR image tidak ditemukan")

        qr_image_response = requests.get(qr_url)
        qr_image = Image.open(BytesIO(qr_image_response.content))

        return {
            "qr_image": qr_image,
            "transaction_id": data["data"].get("transactionId"),
            "amount": int(data["data"].get("amount", 0))
        }

    def check_payment(self, expected_amount):
        url = "https://api.ranz.my.id/checkpayment"
        params = {
            "token": self.token,
            "merchant": self.merchant,
            "apikey": self.apikey
        }
        response = requests.get(url, params=params)
        data = response.json()

        if data.get("statusCode") != 200:
            return {"status": "unpaid"}

        payment = data.get("data", {})

        if int(payment.get("amount", 0)) == expected_amount:
            return {"status": "paid"}
        
        return {"status": "unpaid"}
