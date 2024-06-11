import reportlab
import uuid

def create_invoice(invoice_number:str):
    from reportlab.pdfgen import canvas
    from reportlab.lib.pagesizes import A4
    from reportlab.tables import Table
    c = canvas.Canvas('myfile.pdf', pagesize=A4)
    width, height = A4
    c.drawImage('static/logo.png', 0, height-100, 100, 100)
    c.setFont("Helvetica", 36)
    c.drawString(120, height-50-18, "Donut Disturb Pvt. Ltd.")
    c.setFont("Helvetica", 12)
    c.drawString(10, height-120, f"Invoice: {invoice_number}")
    # Header
    c.drawString(10, )


    c.showPage()
    c.save()

create_invoice(uuid.uuid4())
