from app import create_app
from app.models.database import db, KPI, GroupeThematique

app = create_app()
ctx = app.app_context()
ctx.push()

# Dictionnaire pour mapper les groupes
groupes_map = {
    "Gouvernance et reformes": 3,
    "Travail et Sécurité Sociale": 1,
    "Fonction Publique": 2
}

# Liste des 40 indicateurs
indicateurs = [
    # Gouvernance et reformes (groupe 3)
    (1, 3, "GT1PKI01", "Taux de satisfaction des usagers du ministere", 80, "%", "pourcentage", "Usagers satisfaits", "Total repondants"),
    (2, 3, "GT1PKI02", "Taux de satisfaction des agents du ministere", 75, "%", "pourcentage", "Agents satisfaits", "Total agents repondants"),
    (3, 3, "GT1PKI03", "% des services publics dematerialises accessibles en ligne", 70, "%", "pourcentage", "Services en ligne", "Total services identifies"),
    (4, 3, "GT1PKI04", "Taux d'adoption des outils numeriques par les structures", 65, "%", "pourcentage", "Structures utilisant activement", "Total structures"),
    (5, 3, "GT1PKI05", "Taux de dematerialisation du courrier à la source", 60, "%", "pourcentage", "Courriers numeriques", "Total courriers"),
    (6, 3, "GT1PKI06", "Taux d'utilisation de la signature numerique", 55, "%", "pourcentage", "Actes signes numeriquement", "Total actes"),
    (7, 3, "GT1PKI07", "Taux de couverture des ministeres en missions d'audit", 85, "%", "pourcentage", "Ministeres audites", "Total ministeres"),
    (8, 3, "GT1PKI08", "Taux de couverture reseau et connectivite", 90, "%", "pourcentage", "Structures connectees", "Total structures MTFP"),
    (9, 3, "GT1PKI09", "Taux de traitement des plaintes des usagers", 70, "%", "pourcentage", "Plaintes traitees", "Total plaintes"),
    (10, 3, "GT1PKI10", "Indice de perception de la corruption", 45, "/100", "score_externe", "Score IPC", None),
    (11, 3, "GT1PKI11", "Taux de couverture des communes en CCSP/GSRU", 65, "%", "pourcentage", "Communes avec CCSP", "77"),
    (12, 3, "GT1PKI12", "Taux d'accroissement moyen des dotations budgetaires", 5.08, "%", "pourcentage", "TCAC", None),
    (13, 3, "GT1PKI13", "Taux moyen d'execution financiere des dotations", 85, "%", "pourcentage", "Montant execute", "Montant vote"),
    (14, 3, "GT1PKI14", "Taux moyen d'execution physique des activites du PTA", 80, "%", "pourcentage", "Activites realisees", "Activites prevues"),
    (15, 3, "GT1PKI15", "Ratio d'efficience sur la periode 2016-2026", 75, "%", "pourcentage", "Outputs", "Inputs"),
    
    # Travail et Securite Sociale (groupe 1)
    (16, 1, "GT2PKI01", "Nombre d'enfants retires des pires formes de travail", 15000, "enfants", "somme", "Nombre d'enfants retires", None),
    (17, 1, "GT2PKI02", "Nombre d'enfants retires et reinseres", 12000, "enfants", "somme", "Enfants reinseres", None),
    (18, 1, "GT2PKI03", "Taux de prevalence du travail des enfants", 25, "%", "pourcentage", "Enfants au travail", "Population 5-17 ans"),
    (19, 1, "GT2PKI04", "% des assures CNSS payes par virement electronique", 60, "%", "pourcentage", "Assures payes electroniquement", "Total assures"),
    (20, 1, "GT2PKI05", "Delai moyen de liquidation des pensions CNSS", 90, "jours", "moyenne", "Somme des delais", "Nombre de dossiers"),
    (21, 1, "GT2PKI06", "Taux de conflictualite dans le secteur public", 15, "%", "pourcentage", "Conflits enregistres", "Total structures"),
    (22, 1, "GT2PKI07", "Taux de conflictualite dans le secteur prive", 20, "%", "pourcentage", "Conflits enregistres", "Total entreprises"),
    (23, 1, "GT2PKI08", "Taux de representativite des organisations syndicales", 70, "%", "pourcentage", "Syndicats representatifs", "Total syndicats"),
    (24, 1, "GT2PKI09", "Taux de reglement des litiges par conciliation", 65, "%", "pourcentage", "Litiges concilies", "Total litiges"),
    (25, 1, "GT2PKI10", "Taux de conformite aux normes de securite (SST)", 55, "%", "pourcentage", "Entreprises conformes", "Total entreprises controlees"),
    # (26, 1, "GT2PKI10", "Taux de conformite aux normes de securite (SST)", 55, "%", "pourcentage", "Entreprises conformes", "Total entreprises controlees"),
    # (27, 1, "GT2PKI10", "Taux de conformite aux normes de securite (SST)", 55, "%", "pourcentage", "Entreprises conformes", "Total entreprises controlees"),

    
    # Fonction Publique (groupe 2)
    (26, 2, "GT3PKI01", "Taux de numerisation des archives RH", 40, "%", "pourcentage", "Dossiers numerises", "Total dossiers"),
    (27, 2, "GT3PKI02", "Delai de parution des actes de carriere", 60, "jours", "moyenne", "Somme des delais", "Nombre d'actes"),
    (28, 2, "GT3PKI03", "Taux du Turn-over dans la fonction publique", 12, "%", "pourcentage", "Departs", "Effectif total"),
    (29, 2, "GT3PKI04", "% de proces gagnes par l'Etat (Contentieux FP)", 75, "%", "pourcentage", "Proces gagnes", "Total proces"),
    (30, 2, "GT3PKI05", "Delai moyen de la procedure disciplinaire", 120, "jours", "moyenne", "Somme des delais", "Nombre de procedures"),
    (31, 2, "GT3PKI06", "Delai de remise des livrets de pension (FNRB)", 45, "jours", "moyenne", "Somme des delais", "Nombre de livrets"),
    (32, 2, "GT3PKI07", "Nombre de pieces du dossier de retraite", 15, "pieces", "somme", "Nombre de pieces", None),
    (33, 2, "GT3PKI08", "Delai de notification des actes de retraite", 30, "jours", "moyenne", "Somme des delais", "Nombre d'agents"),
    (34, 2, "GT3PKI09", "% d'agents ayant souscrit au Code d'ethique", 50, "%", "pourcentage", "Agents ayant souscrit", "Total agents actifs"),
    (35, 2, "GT3PKI10", "Nombre d'agents recrutes (2016-2026)", 25000, "agents", "somme", "Agents recrutes", None),
    (36, 2, "GT3PKI11", "Delai de mise à disposition des nouveaux recrues", 60, "jours", "moyenne", "Somme des delais", "Nombre de recrues"),
    (37, 2, "GT3PKI12", "% de nouveaux recrues adherent au Code d'ethique", 95, "%", "pourcentage", "Nouveaux signataires", "Total nouveaux"),
    (38, 2, "GT3PKI13", "Nombre d'agents recrutes par ministere", 0, "agents", "somme", "Agents par ministere", None),
    (39, 2, "GT3PKI14", "Taux d'absenteisme dans la fonction publique", 12, "%", "pourcentage", "Jours d'absence", "Total jours theoriques"),
    (40, 2, "GT3PKI15", "Nombre de personnes handicapees recrutees", 500, "personnes", "somme", "PSH recrutees", None),
]

print("Suppression des anciens KPIs...")
KPI.query.delete()
db.session.commit()

print("Ajout des 40 indicateurs...")
compteur = 0

for num, groupe_id, code, intitule, cible, unite, formule, num_label, den_label in indicateurs:
    kpi = KPI(
        axe_strategique="PAG 2 (2021-2026)",
        groupe_id=groupe_id,
        indicateur=intitule,
        valeur_cible=cible,
        valeur_atteinte=0,
        unite=unite,
        formule_type=formule,
        numerateur_label=num_label,
        denominateur_label=den_label,
        numerateur_valeur=0,
        denominateur_valeur=0,
        source_verification="A renseigner",
        responsable="A renseigner"
    )
    db.session.add(kpi)
    compteur += 1
    print(f"  {compteur}. {intitule[:50]}...")

db.session.commit()
print(f"\n✅ {compteur} indicateurs ajoutes avec succes !")

# Verification
print("\n📊 Verification par groupe:")
for g in GroupeThematique.query.all():
    count = KPI.query.filter_by(groupe_id=g.id).count()
    print(f"   {g.nom}: {count} indicateurs")

print("\n✅ Importation terminee !")
exit()