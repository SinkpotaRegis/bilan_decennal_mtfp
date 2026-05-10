from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

try:
    # Sauvegarder les données existantes
    print("1. Sauvegarde des donnees...")
    kpis_data = []
    try:
        result = db.session.execute(text("SELECT * FROM kpis"))
        for row in result:
            kpis_data.append(dict(row._mapping))
        print(f"   {len(kpis_data)} indicateurs sauvegardes")
    except:
        print("   Aucune donnee existante")
    
    # Supprimer l'ancienne table
    print("2. Suppression de l'ancienne table...")
    db.session.execute(text("DROP TABLE IF EXISTS kpis"))
    db.session.commit()
    
    # Recréer la table avec les bons types
    print("3. Recreation de la table...")
    db.session.execute(text('''
        CREATE TABLE kpis (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            axe_strategique TEXT,
            groupe_id INTEGER,
            code TEXT,
            indicateur TEXT,
            definition TEXT,
            objectif TEXT,
            valeur_cible REAL,
            valeur_atteinte REAL,
            unite TEXT,
            source_verification TEXT,
            responsable TEXT,
            observations TEXT,
            fichier_pdf TEXT,
            frequence_collecte TEXT,
            formule_type TEXT,
            numerateur_label TEXT,
            denominateur_label TEXT,
            numerateur_valeur REAL,
            denominateur_valeur REAL,
            preuve_numerique TEXT
        )
    '''))
    db.session.commit()
    print("   Table recreee avec les bons types")
    
    # Restaurer les données
    if kpis_data:
        print("4. Restauration des donnees...")
        for k in kpis_data:
            db.session.execute(text('''
                INSERT INTO kpis (
                    id, axe_strategique, groupe_id, code, indicateur,
                    definition, objectif, valeur_cible, valeur_atteinte,
                    unite, source_verification, responsable, observations,
                    fichier_pdf, frequence_collecte, formule_type,
                    numerateur_label, denominateur_label, numerateur_valeur,
                    denominateur_valeur, preuve_numerique
                ) VALUES (
                    :id, :axe_strategique, :groupe_id, :code, :indicateur,
                    :definition, :objectif, :valeur_cible, :valeur_atteinte,
                    :unite, :source_verification, :responsable, :observations,
                    :fichier_pdf, :frequence_collecte, :formule_type,
                    :numerateur_label, :denominateur_label, :numerateur_valeur,
                    :denominateur_valeur, :preuve_numerique
                )
            '''), k)
        db.session.commit()
        print(f"   {len(kpis_data)} indicateurs restores")
    
    print("\n✅ Correction terminee !")
    
except Exception as e:
    print(f"❌ Erreur: {e}")
    db.session.rollback()

exit()