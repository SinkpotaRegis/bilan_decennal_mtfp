# =============================================================================
#  migration_kpis_officiels.py
#  À placer à la RACINE du projet.
#
#  CE QUE ÇA FAIT :
#  1. Ajoute l'index UNIQUE(kpi_id, annee) sur kpis_annuels
#  2. Supprime les anciens KPIs créés manuellement (avec confirmation)
#  3. Insère les 45 KPIs officiels depuis kpi_mapping.py dans l'ordre chronologique
#  4. Chaque KPI est créé avec toutes ses métadonnées complètes
#
#  USAGE : python migration_kpis_officiels.py
#  À exécuter UNE SEULE FOIS après avoir remplacé kpi_mapping.py.
# =============================================================================

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from app import create_app
from app.models.database import db
from sqlalchemy import text

app = create_app()


def run():
    with app.app_context():
        print("=" * 65)
        print("  Migration — 45 KPIs officiels MTFP 2016-2026")
        print("=" * 65)

        from app.kpi_mapping import KPI_META, KPI_ORDRE_CHRONOLOGIQUE
        from app.models.database import GroupeThematique, KPI

        # ── Résoudre les IDs des groupes ────────────────────────────────
        groupes = GroupeThematique.query.all()
        groupe_id_map = {}
        for g in groupes:
            nom = g.nom.lower()
            if 'gouvernance' in nom or 'reforme' in nom:
                groupe_id_map['GT1'] = g.id
            elif 'travail' in nom or 'securite' in nom or 'sécurité' in nom:
                groupe_id_map['GT2'] = g.id
            elif 'fonction' in nom or 'publique' in nom:
                groupe_id_map['GT3'] = g.id

        print(f"\n  Groupes BDD trouvés : {groupe_id_map}")
        if len(groupe_id_map) < 3:
            print("  ❌ Groupes thématiques manquants en BDD !")
            print("     Relance l'app une fois pour les créer, puis relance ce script.")
            return

        # ── Supprimer les anciens KPIs si souhaité ───────────────────────
        nb_existants = KPI.query.count()
        if nb_existants > 0:
            print(f"\n  ⚠️  {nb_existants} KPI(s) déjà en base.")
            rep = input("  Vider et réinsérer proprement ? (oui/non) : ").strip().lower()
            if rep == 'oui':
                db.session.execute(text("DELETE FROM kpis_annuels"))
                db.session.execute(text("DELETE FROM preuves_documentaires"))
                db.session.execute(text("DELETE FROM commentaires_annuels"))
                db.session.execute(text("DELETE FROM validations"))
                db.session.execute(text("DELETE FROM kpis"))
                db.session.commit()
                print("  ✅ Anciens KPIs supprimés.")
            else:
                print("  → Insertion uniquement des KPIs manquants.")

        # ── Index UNIQUE sur kpis_annuels(kpi_id, annee) ────────────────
        print("\n  Vérification contrainte UNIQUE kpis_annuels…")
        try:
            idx = db.session.execute(text(
                "SELECT name FROM sqlite_master WHERE type='index' "
                "AND tbl_name='kpis_annuels' AND name='uq_kpi_annee'"
            )).fetchone()
            if not idx:
                # Nettoyer doublons éventuels
                db.session.execute(text("""
                    DELETE FROM kpis_annuels WHERE id NOT IN (
                        SELECT MIN(id) FROM kpis_annuels GROUP BY kpi_id, annee
                    )
                """))
                db.session.execute(text("""
                    CREATE UNIQUE INDEX uq_kpi_annee ON kpis_annuels(kpi_id, annee)
                """))
                db.session.commit()
                print("  ✅ Index UNIQUE créé sur kpis_annuels(kpi_id, annee)")
            else:
                print("  ℹ️  Index UNIQUE déjà présent")
        except Exception as e:
            db.session.rollback()
            print(f"  ⚠️  Index : {e}")

        # ── Insertion des 45 KPIs dans l'ordre chronologique ────────────
        print(f"\n  Insertion de {len(KPI_ORDRE_CHRONOLOGIQUE)} KPIs…\n")
        inserted = 0
        skipped  = 0

        for code in KPI_ORDRE_CHRONOLOGIQUE:
            meta = KPI_META.get(code)
            if not meta:
                print(f"  ⚠️  {code} absent du mapping — ignoré")
                continue

            # Vérifier si déjà présent
            if KPI.query.filter(db.func.upper(KPI.code) == code).first():
                skipped += 1
                continue

            groupe_id = groupe_id_map.get(meta['groupe'])
            if not groupe_id:
                print(f"  ⚠️  Groupe {meta['groupe']} introuvable pour {code}")
                continue

            try:
                kpi = KPI(
                    code               = code,
                    indicateur         = meta['intitule'],
                    groupe_id          = groupe_id,
                    definition         = meta.get('definition', ''),
                    objectif           = meta.get('objectif', ''),
                    formule_type       = meta.get('formule_type', 'pourcentage'),
                    unite              = meta.get('unite', '%'),
                    numerateur_label   = meta.get('numerateur_label', 'Numérateur'),
                    denominateur_label = meta.get('denominateur_label', 'Dénominateur') or 'Dénominateur',
                    frequence_collecte = meta.get('frequence', 'Annuelle'),
                    source_verification= meta.get('source', ''),
                    axe_strategique    = meta.get('direction', ''),
                    valeur_cible       = None,
                    observations       = meta.get('mode_calcul', ''),
                )
                db.session.add(kpi)
                db.session.flush()
                inserted += 1

                # Affichage condensé
                gt_label = {'GT1': '🏛', 'GT2': '💼', 'GT3': '👤'}.get(meta['groupe'], '📊')
                print(f"  {gt_label} {code} — {meta['intitule'][:55]}...")

            except Exception as e:
                db.session.rollback()
                print(f"  ❌ {code} : {e}")

        db.session.commit()

        # ── Résumé final ─────────────────────────────────────────────────
        total_bdd = KPI.query.count()
        print()
        print("=" * 65)
        print(f"  ✅ {inserted} KPI(s) insérés")
        print(f"  ℹ️  {skipped} KPI(s) déjà présents")
        print(f"  📊 Total en BDD : {total_bdd} KPIs")
        print()

        # Vérification de l'ordre
        kpis_bdd = [k.code for k in KPI.query.order_by(KPI.id).all()]
        print("  Ordre en BDD :")
        for i, c in enumerate(kpis_bdd, 1):
            print(f"    {i:>2}. {c}")

        print()
        print("  ✅ Accède maintenant à /admin/liste-kpis pour voir tous les KPIs")
        print("  ✅ /kpi/gt1pki01, /kpi/gt2pki05, /kpi/gt3pki09 etc. sont actifs")
        print("=" * 65)


if __name__ == "__main__":
    run()
