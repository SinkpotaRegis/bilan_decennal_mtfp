from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

colonnes = ['code', 'definition', 'objectif', 'frequence_collecte']

for col in colonnes:
    try:
        db.session.execute(text(f'ALTER TABLE kpis ADD COLUMN {col} TEXT'))
        db.session.commit()
        print(f"Colonne {col} ajoutee")
    except Exception as e:
        if "duplicate" in str(e).lower():
            print(f"Colonne {col} existe deja")
        else:
            print(f"Erreur pour {col}: {e}")

exit()