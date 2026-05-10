from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

print("1. Création de la table kpis_annuels...")
db.session.execute(text('''
    CREATE TABLE IF NOT EXISTS kpis_annuels (
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
print("   ✅ Table créée")

print("2. Récupération des KPIs existants...")
kpis = db.session.execute(text("SELECT id FROM kpis")).fetchall()
print(f"   {len(kpis)} KPIs trouvés")

annees = list(range(2016, 2027))
print(f"   Années: {annees[0]} → {annees[-1]}")

print("3. Insertion des données par défaut...")
compteur = 0
for kpi in kpis:
    kpi_id = kpi[0]
    for annee in annees:
        try:
            db.session.execute(
                text('''INSERT OR IGNORE INTO kpis_annuels (kpi_id, annee, numerateur_valeur, denominateur_valeur, valeur_calculee, commentaire)
                        VALUES (:kpi_id, :annee, 0, 0, 0, '')'''),
                {'kpi_id': kpi_id, 'annee': annee}
            )
            compteur += 1
        except Exception as e:
            print(f"   Erreur KPI {kpi_id}, année {annee}: {e}")

db.session.commit()
print(f"   ✅ {compteur} enregistrements insérés")

print("4. Vérification finale...")
total = db.session.execute(text("SELECT COUNT(*) FROM kpis_annuels")).fetchone()[0]
print(f"   ✅ Total dans kpis_annuels: {total} enregistrements")

exit()