from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
from io import BytesIO

print("Test 1: Création PDF minimal...")

try:
    buffer = BytesIO()
    c = canvas.Canvas(buffer, pagesize=A4)
    c.drawString(100, 800, "Test PDF - Bilan Decennal MTFP")
    c.save()
    buffer.seek(0)
    
    with open("test_minimal.pdf", "wb") as f:
        f.write(buffer.read())
    
    print("✅ PDF minimal créé avec succès !")
    print("   Fichier: test_minimal.pdf")
except Exception as e:
    print(f"❌ Erreur: {e}")