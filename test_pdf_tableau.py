from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet
from io import BytesIO

print("Test 3: Création PDF avec tableau...")

try:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []
    
    # Titre
    elements.append(Paragraph("TEST TABLEAU - BILAN DECENNAL MTFP", styles['Title']))
    elements.append(Spacer(1, 20))
    
    # Tableau simple
    data = [
        ['Année', 'Taux (%)', 'Commentaire'],
        ['2016', '65%', 'Donnée initiale'],
        ['2017', '68%', 'En progression'],
        ['2018', '72%', 'Stable'],
    ]
    
    table = Table(data)
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#006633')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table)
    
    doc.build(elements)
    buffer.seek(0)
    
    with open("test_tableau.pdf", "wb") as f:
        f.write(buffer.read())
    
    print("✅ PDF avec tableau créé avec succès !")
    print("   Fichier: test_tableau.pdf")
except Exception as e:
    print(f"❌ Erreur: {e}")