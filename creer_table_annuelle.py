from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

try:
    db.session.execute(text('DROP TABLE IF EXISTS kpis_annuels'))
    db.session.execute(text('''
        CREATE TABLE kpis_annuels (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            kpi_id INTEGER NOT NULL,
            annee INTEGER NOT NULL,
            numerateur_valeur REAL DEFAULT 0,
            denominateur_valeur REAL DEFAULT 0,
            valeur_calculee REAL DEFAULT 0,
            commentaire TEXT,
            direction_concernee TEXT,
            created_at DATETIME,
            created_by INTEGER,
            FOREIGN KEY (kpi_id) REFERENCES kpis(id),
            UNIQUE(kpi_id, annee)
        )
    '''))
    db.session.commit()
    print("✅ Table kpis_annuels créée avec succès")
except Exception as e:
    print(f"❌ Erreur: {e}")

exit()