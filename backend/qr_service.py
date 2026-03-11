import qrcode
import io
import base64


def generate_qr_code(ticket_id):

    qr = qrcode.make(f"http://localhost:8000/ticket/{ticket_id}")

    buffer = io.BytesIO()
    qr.save(buffer, format="PNG")

    qr_base64 = base64.b64encode(buffer.getvalue()).decode()

    return qr_base64