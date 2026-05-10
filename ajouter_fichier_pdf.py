from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

try:
    db.session.execute(text('ALTER TABLE kpis ADD COLUMN fichier_pdf TEXT'))
    db.session.commit()
    print("✅ Colonne fichier_pdf ajoutée")
except Exception as e:
    if "duplicate" in str(e).lower():
        print("⚠️ Colonne fichier_pdf existe déjà")
    else:
        print(f"❌ Erreur: {e}")

exit()