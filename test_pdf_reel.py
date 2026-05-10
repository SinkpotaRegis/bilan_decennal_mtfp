from app import create_app
from app.models.database import db
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4, landscape
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm
from io import BytesIO
from sqlalchemy import text

print("Test 4: Export PDF avec données réelles...")

app = create_app()
ctx = app.app_context()
ctx.push()

# Récupérer les données manuellement
kpi_result = db.session.execute(text("SELECT * FROM kpis WHERE id = 1")).fetchone()
if not kpi_result:
    print("❌ Aucune donnée KPI")
    exit()

# Afficher tous les indices pour déboguer
print("\n=== STRUCTURE DU TUPLE KPI ===")
print(f"Nombre de colonnes: {len(kpi_result)}")
for i, val in enumerate(kpi_result):
    print(f"  index {i}: {val} (type: {type(val).__name__})")

# Récupérer les données annuelles
annuel_result = db.session.execute(
    text("SELECT annee, numerateur_valeur, denominateur_valeur, valeur_calculee, commentaire FROM kpis_annuels WHERE kpi_id = 1 ORDER BY annee")
).fetchall()

# Identifier les bons indices (à adapter selon l'affichage ci-dessus)
# Exemple: si 'code' est à l'index 5, 'indicateur' à l'index 6, etc.
kpi_dict = {
    'id': kpi_result[0],
    'code': kpi_result[5] if len(kpi_result) > 5 else '',
    'indicateur': kpi_result[6] if len(kpi_result) > 6 else '',
    'definition': kpi_result[7] if len(kpi_result) > 7 else '',
    'objectif': kpi_result[8] if len(kpi_result) > 8 else '',
    'numerateur_label': kpi_result[18] if len(kpi_result) > 18 else '',
    'denominateur_label': kpi_result[19] if len(kpi_result) > 19 else '',
}

# Convertir en chaîne si ce n'est pas déjà le cas
for key in ['code', 'indicateur', 'definition', 'objectif', 'numerateur_label', 'denominateur_label']:
    if kpi_dict[key] is None:
        kpi_dict[key] = ''
    elif not isinstance(kpi_dict[key], str):
        kpi_dict[key] = str(kpi_dict[key])

print(f"\nKPI: {kpi_dict['indicateur']}")
print(f"Nombre d'années: {len(annuel_result)}")

try:
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=landscape(A4))
    styles = getSampleStyleSheet()
    elements = []
    
    title_style = ParagraphStyle('CustomTitle', parent=styles['Heading1'], fontSize=16, textColor=colors.HexColor('#006633'), alignment=1)
    elements.append(Paragraph("FICHE INDICATEUR - TEST", title_style))
    elements.append(Spacer(1, 20))
    
    data_info = [
        ['Code', kpi_dict['code']],
        ['Indicateur', kpi_dict['indicateur']],
        ['Définition', (kpi_dict['definition'] or '')[:200]],
    ]
    
    table_info = Table(data_info, colWidths=[3*cm, 12*cm])
    table_info.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (0, -1), colors.HexColor('#006633')),
        ('TEXTCOLOR', (0, 0), (0, -1), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table_info)
    elements.append(Spacer(1, 20))
    
    # Tableau des données
    data_table = [['Année', kpi_dict['numerateur_label'] or 'Numérateur', kpi_dict['denominateur_label'] or 'Dénominateur', 'Taux (%)']]
    for row in annuel_result:
        data_table.append([row[0], row[1] or 0, row[2] or 0, f"{row[3]:.2f}%"])
    
    table_data = Table(data_table, colWidths=[2*cm, 3*cm, 3*cm, 2.5*cm])
    table_data.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#006633')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.grey),
    ]))
    elements.append(table_data)
    
    doc.build(elements)
    buffer.seek(0)
    
    with open("test_reel.pdf", "wb") as f:
        f.write(buffer.read())
    
    print("✅ PDF réel créé avec succès !")
    print("   Fichier: test_reel.pdf")
except Exception as e:
    print(f"❌ Erreur: {e}")
    import traceback
    traceback.print_exc()

exit()