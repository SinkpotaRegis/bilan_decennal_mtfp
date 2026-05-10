from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

colonnes_a_ajouter = [
    'formule_type',
    'numerateur_label',
    'denominateur_label',
    'numerateur_valeur',
    'denominateur_valeur',
    'preuve_numerique'
]

for col in colonnes_a_ajouter:
    try:
        db.session.execute(text(f'ALTER TABLE kpis ADD COLUMN {col} TEXT'))
        db.session.commit()
        print(f"✅ Colonne {col} ajoutée")
    except Exception as e:
        if "duplicate" in str(e).lower():
            print(f"⚠️ Colonne {col} existe déjà")
        else:
            print(f"❌ Erreur pour {col}: {e}")

exit()