from app import create_app
from app.models.database import db
from sqlalchemy import text

print("=== AJOUT DES COLONNES D'ANALYSE ===")

app = create_app()
ctx = app.app_context()
ctx.push()

# Liste des colonnes à ajouter
colonnes = [
    ('facteurs_explicatifs', 'TEXT'),
    ('benchmarking', 'TEXT'),
    ('recommandations', 'TEXT')
]

for col, col_type in colonnes:
    try:
        db.session.execute(text(f'ALTER TABLE kpis ADD COLUMN {col} {col_type}'))
        db.session.commit()
        print(f"✅ Colonne {col} ajoutée")
    except Exception as e:
        if "duplicate" in str(e).lower():
            print(f"⚠️ Colonne {col} existe déjà")
        else:
            print(f"❌ Erreur pour {col}: {e}")

print("\n=== VÉRIFICATION DES COLONNES ===")
result = db.session.execute(text("PRAGMA table_info(kpis)"))
for row in result:
    print(f"  - {row[1]}")

exit()