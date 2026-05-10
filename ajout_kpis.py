from app import create_app
from app.models.database import db, KPI

app = create_app()
ctx = app.app_context()
ctx.push()

# Liste des indicateurs
indicateurs = [
    # Groupe 3 : Gouvernance et Reformes (id=3)
    (3, "Taux de satisfaction des usagers du ministere", 80, "%", "Enquetes de satisfaction", "CCSP/GSRU"),
    (3, "Taux de satisfaction des agents du ministere", 75, "%", "Enquete RH interne", "DRH"),
    (3, "Services public dematerialises accessibles en ligne", 70, "%", "Catalogue officiel", "DSI"),
    (3, "Taux d'adoption des outils numeriques", 65, "%", "Journaux de connexion", "DSI"),
    (3, "Taux de dematerialisation du courrier", 60, "%", "Gestion electronique", "DSI"),
    (3, "Taux d'utilisation de la signature numerique", 55, "%", "Signature electronique", "DSI"),
    (3, "Taux de couverture des ministeres en audit", 85, "%", "Rapports IGSEP", "IGSEP"),
    (3, "Taux de couverture reseau et connectivite", 90, "%", "Inventaire reseau", "DSI"),
    (3, "Taux de traitement des plaintes des usagers", 70, "%", "Registre des plaintes", "CCSP"),
    (3, "Indice de perception de la corruption", 45, "/100", "Transparency International", "Cabinet"),
    (3, "Taux de couverture des communes en CCSP", 65, "%", "Tableau de bord CCSP", "DSI"),
    (3, "Taux de retard dans l'Administration Publique", 30, "%", "SI de gestion des actes", "SGM"),
    # Groupe 1 : Travail et Securite Sociale (id=1)
    (1, "Enfants retires des pires formes de travail", 15000, "enfants", "Rapports DGT", "DGT"),
    (1, "Taux de prevalence du travail des enfants", 25, "%", "Enquetes MICS", "DGT"),
    (1, "Assures CNSS payes par virement bancaire", 60, "%", "Base de gestion CNSS", "CNSS"),
    (1, "Delai de liquidation des pensions CNSS", 90, "jours", "Systeme de gestion CNSS", "CNSS"),
    (1, "Taux de conformite aux normes de securite", 55, "%", "Rapports inspecteurs", "DGT"),
    # Groupe 2 : Fonction Publique (id=2)
    (2, "Taux de numerisation des archives RH", 40, "%", "Base SIGRH", "DGFP"),
    (2, "Delai de parution des actes de carriere", 60, "jours", "SI de gestion des actes", "DGFP"),
    (2, "Proces gagnes par l'Etat en Contentieux FP", 75, "%", "Cour Supreme", "SA"),
    (2, "Delai de la procedure disciplinaire", 120, "jours", "Registres des instances", "DGFP"),
    (2, "Delai de remise des livrets de pension", 45, "jours", "Base FNRB", "FNRB"),
    (2, "Nombre de pieces du dossier de retraite", 15, "pieces", "Guide FNRB", "FNRB"),
    (2, "Delai de notification des actes de retraite", 30, "jours", "Registre DGFP", "DGFP"),
    (2, "Agents ayant souscrit au Code d'ethique", 50, "%", "Base des signatures", "DGFP"),
    (2, "Agents recrutes (2016-2026)", 25000, "agents", "Fichier des recrutements", "DGFP"),
    (2, "Delai de mise a disposition des nouveaux recrues", 60, "jours", "Registre des affectations", "DGFP"),
    (2, "Nouveaux recrues adherent au Code d'ethique", 95, "%", "Base des signatures", "DGFP"),
    (2, "Taux d'absenteisme dans la fonction publique", 12, "%", "Registres de presence", "DGFP"),
    (2, "Personnes handicapees recrutees", 500, "personnes", "Registre DGRH", "DGFP"),
]

print("Ajout des indicateurs...")
compteur = 0

for groupe_id, intitule, cible, unite, source, responsable in indicateurs:
    kpi = KPI(
        axe_strategique="PAG 2 (2021-2026)",
        groupe_id=groupe_id,
        indicateur=intitule,
        valeur_cible=cible,
        valeur_atteinte=0,
        unite=unite,
        source_verification=source,
        responsable=responsable
    )
    db.session.add(kpi)
    compteur += 1
    print(f"  + {intitule[:40]}")

db.session.commit()
print(f"\n✅ {compteur} indicateurs ajoutes !")
print(f"Total KPIs: {KPI.query.count()}")

exit()