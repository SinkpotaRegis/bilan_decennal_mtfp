from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

# 1. Table pour les commentaires annuels
print("Création de la table commentaires_annuels...")

commentaires_table_sql = '''
    CREATE TABLE commentaires_annuels (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kpi_id INTEGER NOT NULL,
        annee INTEGER NOT NULL,
        commentaire TEXT,
        date_ajout TEXT,
        ajoute_par TEXT,
        FOREIGN KEY (kpi_id) REFERENCES kpis(id)
    )
'''

existing_commentaires_sql = db.session.execute(text("""
    SELECT sql
    FROM sqlite_master
    WHERE type = 'table' AND name = 'commentaires_annuels'
""")).scalar()

if not existing_commentaires_sql:
    db.session.execute(text(commentaires_table_sql))
elif 'UNIQUE(KPI_ID, ANNEE)' in existing_commentaires_sql.upper():
    print("Migration de commentaires_annuels pour supprimer la contrainte unique...")
    db.session.execute(text('ALTER TABLE commentaires_annuels RENAME TO commentaires_annuels_old'))
    db.session.execute(text(commentaires_table_sql))
    db.session.execute(text('''
        INSERT INTO commentaires_annuels (id, kpi_id, annee, commentaire, date_ajout, ajoute_par)
        SELECT id, kpi_id, annee, commentaire, date_ajout, ajoute_par
        FROM commentaires_annuels_old
        ORDER BY id
    '''))
    db.session.execute(text('DROP TABLE commentaires_annuels_old'))
else:
    print("Table commentaires_annuels déjà compatible.")

# 2. Table pour les preuves documentaires
print("Création de la table preuves_documentaires...")
db.session.execute(text('''
    CREATE TABLE IF NOT EXISTS preuves_documentaires (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        kpi_id INTEGER NOT NULL,
        annee INTEGER NOT NULL,
        titre TEXT,
        type_fichier TEXT,
        chemin_fichier TEXT,
        url_sharepoint TEXT,
        date_ajout TEXT,
        ajoute_par TEXT,
        FOREIGN KEY (kpi_id) REFERENCES kpis(id)
    )
'''))

db.session.commit()
print("✅ Tables créées avec succès")

exit()