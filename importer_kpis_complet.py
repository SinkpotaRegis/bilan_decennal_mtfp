"""
Script d'importation des indicateurs du Bilan Décennal MTFP 2016-2026
Basé sur le document officiel "Fiche complète des Indicateurs"

Mise à jour : Ajout des nouveaux indicateurs GT2PKI11, GT2PKI12, GT2PKI13
et GT3PKI15, GT3PKI16
"""

from app import create_app
from app.models.database import db, GroupeThematique, KPI

app = create_app()
ctx = app.app_context()
ctx.push()

# ============================================================
# LISTE COMPLETE DES INDICATEURS
# ============================================================

indicateurs = [
    # ========== GOUVERNANCE ET REFORMES (GT1PKI01 à GT1PKI15) ==========
    {
        "code": "GT1PKI01",
        "indicateur": "Taux de satisfaction des usagers du ministère",
        "definition": "Niveau de satisfaction des usagers ayant eu recours aux services du MTFP.",
        "objectif": "Évaluer la qualité perçue des services rendus par le MTFP.",
        "formule_type": "pourcentage",
        "numerateur_label": "Usagers satisfaits",
        "denominateur_label": "Total répondants",
        "unite": "%",
        "source_verification": "Enquêtes de satisfaction (CCSP, GSRU), rapports points focaux CCSP",
        "responsable": "CCSP/GSRU",
        "frequence": "Semestrielle",
        "valeur_cible": 85
    },
    {
        "code": "GT1PKI02",
        "indicateur": "Taux de satisfaction des agents du ministère",
        "definition": "Niveau de satisfaction des agents sur leurs conditions de travail et carrière.",
        "objectif": "Identifier les facteurs de mal-être professionnel au sein du ministère.",
        "formule_type": "pourcentage",
        "numerateur_label": "Agents satisfaits",
        "denominateur_label": "Total agents répondants",
        "unite": "%",
        "source_verification": "Enquête RH interne (DRH), entretiens professionnels",
        "responsable": "DRH",
        "frequence": "Annuelle",
        "valeur_cible": 80
    },
    {
        "code": "GT1PKI03",
        "indicateur": "% des services publics dématérialisés accessibles en ligne",
        "definition": "Proportion des services du MTFP intégralement accessibles par voie numérique.",
        "objectif": "Mesurer l'avancement de la dématérialisation des procédures administratives.",
        "formule_type": "pourcentage",
        "numerateur_label": "Services en ligne",
        "denominateur_label": "Total services identifiés",
        "unite": "%",
        "source_verification": "Catalogue officiel du MTFP, portail de téléprocédures, rapports DSI",
        "responsable": "DSI",
        "frequence": "Annuelle",
        "valeur_cible": 90
    },
    {
        "code": "GT1PKI04",
        "indicateur": "Taux d'adoption des outils numériques par les structures",
        "definition": "Proportion des structures utilisant activement les outils numériques.",
        "objectif": "Évaluer le degré réel d'appropriation des technologies numériques.",
        "formule_type": "pourcentage",
        "numerateur_label": "Structures utilisant activement",
        "denominateur_label": "Total structures",
        "unite": "%",
        "source_verification": "Journaux de connexion (logs DSI), enquête interne annuelle",
        "responsable": "DSI",
        "frequence": "Semestrielle",
        "valeur_cible": 85
    },
    {
        "code": "GT1PKI05",
        "indicateur": "Taux de dématérialisation du courrier à la source",
        "definition": "Part du courrier traité sous format numérique dès la source.",
        "objectif": "Mesurer la progression vers une gestion documentaire sans papier.",
        "formule_type": "pourcentage",
        "numerateur_label": "Courriers traités numériquement",
        "denominateur_label": "Total courriers traités",
        "unite": "%",
        "source_verification": "Système GEC, registres du courrier, rapports DSI",
        "responsable": "DSI",
        "frequence": "Trimestrielle",
        "valeur_cible": 95
    },
    {
        "code": "GT1PKI06",
        "indicateur": "Taux d'utilisation de la signature numérique",
        "definition": "Proportion des actes officiels signés par signature électronique qualifiée.",
        "objectif": "Accélérer la dématérialisation et sécuriser les actes administratifs.",
        "formule_type": "pourcentage",
        "numerateur_label": "Actes signés numériquement",
        "denominateur_label": "Total actes nécessitant signature",
        "unite": "%",
        "source_verification": "Système de signature électronique, logs plateforme",
        "responsable": "DSI",
        "frequence": "Trimestrielle",
        "valeur_cible": 90
    },
    {
        "code": "GT1PKI07",
        "indicateur": "Taux de couverture des ministères en missions d'audit",
        "definition": "Proportion des ministères ayant fait l'objet d'au moins un audit.",
        "objectif": "Évaluer l'effectivité de la fonction de contrôle interne.",
        "formule_type": "pourcentage",
        "numerateur_label": "Ministères audités",
        "denominateur_label": "Total ministères",
        "unite": "%",
        "source_verification": "Rapports Inspection Générale, programme annuel d'audit",
        "responsable": "IGSEP",
        "frequence": "Annuelle",
        "valeur_cible": 100
    },
    {
        "code": "GT1PKI08",
        "indicateur": "Taux de couverture réseau des structures",
        "definition": "Proportion des structures disposant d'une connexion réseau opérationnelle.",
        "objectif": "Garantir l'accès des agents aux systèmes d'information.",
        "formule_type": "pourcentage",
        "numerateur_label": "Structures connectées",
        "denominateur_label": "Total structures MTFP",
        "unite": "%",
        "source_verification": "Inventaire réseau DSI, rapports de monitoring",
        "responsable": "DSI",
        "frequence": "Semestrielle",
        "valeur_cible": 100
    },
    {
        "code": "GT1PKI09",
        "indicateur": "Taux de couverture des structures en connectivité opérationnelle",
        "definition": "Proportion des structures disposant d'une connectivité opérationnelle.",
        "objectif": "Garantir l'accès des agents aux systèmes d'information.",
        "formule_type": "pourcentage",
        "numerateur_label": "Structures avec connectivité",
        "denominateur_label": "Total structures MTFP",
        "unite": "%",
        "source_verification": "Inventaire réseau DSI, rapports de monitoring",
        "responsable": "DSI",
        "frequence": "Semestrielle",
        "valeur_cible": 100
    },
    {
        "code": "GT1PKI010",
        "indicateur": "Taux de traitement des plaintes des usagers",
        "definition": "Part des plaintes traitées dans un délai maximal de 30 jours.",
        "objectif": "Garantir le droit de recours et renforcer la confiance des citoyens.",
        "formule_type": "pourcentage",
        "numerateur_label": "Plaintes traitées ≤ 30 jours",
        "denominateur_label": "Total plaintes reçues",
        "unite": "%",
        "source_verification": "Registre des plaintes, ticketing CCSP/GSRU",
        "responsable": "CCSP/SRU",
        "frequence": "Trimestrielle",
        "valeur_cible": 95
    },
    {
        "code": "GT1PKI11",
        "indicateur": "Taux de couverture des communes en CCSP/GSRU",
        "definition": "Proportion des communes disposant d'un centre de services publics opérationnel.",
        "objectif": "Mesurer la déconcentration physique des services publics numériques.",
        "formule_type": "pourcentage",
        "numerateur_label": "Communes avec CCSP/GSRU",
        "denominateur_label": "77",
        "unite": "%",
        "source_verification": "Tableau de bord CCSP (DSI), rapports PARMAP",
        "responsable": "DSI",
        "frequence": "Semestrielle",
        "valeur_cible": 100
    },
    {
        "code": "GT1PKI12",
        "indicateur": "Taux d'accroissement moyen des dotations budgétaires (2016-2026)",
        "definition": "Évolution annuelle moyenne des crédits budgétaires alloués au MTFP (TCAC).",
        "objectif": "Évaluer l'engagement progressif de l'État en faveur du MTFP.",
        "formule_type": "tcac",
        "numerateur_label": "Dotation annuelle",
        "denominateur_label": None,
        "unite": "%",
        "source_verification": "Lois de finances, DPPD, RAP",
        "responsable": "DPAF",
        "frequence": "Annuelle",
        "valeur_cible": 8
    },
    {
        "code": "GT1PKI13",
        "indicateur": "Taux moyen d'exécution financière des dotations (2016-2026)",
        "definition": "Proportion moyenne des crédits effectivement engagés/ordonnancés.",
        "objectif": "Évaluer la capacité d'absorption budgétaire du MTFP.",
        "formule_type": "moyenne",
        "numerateur_label": "Dépenses réalisées",
        "denominateur_label": "Dotations inscrites",
        "unite": "%",
        "source_verification": "Comptes de gestion, RAP, DPAF",
        "responsable": "DPAF",
        "frequence": "Annuelle",
        "valeur_cible": 95
    },
    {
        "code": "GT1PKI14",
        "indicateur": "Taux moyen d'exécution physique des activités du PTA (2016-2026)",
        "definition": "Proportion moyenne des activités du PTA effectivement réalisées.",
        "objectif": "Apprécier la performance opérationnelle du MTFP.",
        "formule_type": "moyenne",
        "numerateur_label": "Activités réalisées",
        "denominateur_label": "Activités programmées",
        "unite": "%",
        "source_verification": "PTA, RAP, rapports de suivi DPAF",
        "responsable": "DPAF",
        "frequence": "Annuelle",
        "valeur_cible": 90
    },
    {
        "code": "GT1PKI15",
        "indicateur": "Ratio d'efficience sur la période 2016-2026",
        "definition": "Rapport entre taux exécution physique et taux exécution financière.",
        "objectif": "Mesurer l'efficience de la dépense publique.",
        "formule_type": "ratio",
        "numerateur_label": "Taux exécution physique",
        "denominateur_label": "Taux exécution financière",
        "unite": "ratio",
        "source_verification": "RAP, rapports d'exécution budgétaire",
        "responsable": "DPAF",
        "frequence": "Annuelle",
        "valeur_cible": 1.0
    },
    
    # ========== TRAVAIL ET SECURITE SOCIALE (GT2PKI01 à GT2PKI13) ==========
    {
        "code": "GT2PKI01",
        "indicateur": "Nombre d'enfants retirés des pires formes de travail",
        "definition": "Nombre cumulatif d'enfants retirés d'exploitation et pris en charge.",
        "objectif": "Mesurer l'efficacité des interventions de protection de l'enfant.",
        "formule_type": "cumul_annuel",
        "numerateur_label": "Enfants retirés dans l'année",
        "denominateur_label": None,
        "unite": "enfants",
        "source_verification": "Rapports Inspection du Travail (ITB), CNLTE, ONG",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 15000
    },
    {
        "code": "GT2PKI02",
        "indicateur": "Nombre d'enfants retirés des pires formes de travail et réinsérés",
        "definition": "Enfants retirés ayant bénéficié d'un dispositif de réinsertion.",
        "objectif": "Mesurer l'efficacité intégrée des interventions post-retrait.",
        "formule_type": "cumul_annuel",
        "numerateur_label": "Enfants réinsérés",
        "denominateur_label": None,
        "unite": "enfants",
        "source_verification": "Rapports ITB, CNLTE, ONG, Ministère Affaires Sociales",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 12000
    },
    {
        "code": "GT2PKI03",
        "indicateur": "Pourcentage de prévalence du travail des enfants",
        "definition": "Proportion d'enfants de 5-17 ans en situation de travail au Bénin.",
        "objectif": "Évaluer l'ampleur du phénomène du travail des enfants.",
        "formule_type": "pourcentage",
        "numerateur_label": "Enfants au travail",
        "denominateur_label": "Population 5-17 ans",
        "unite": "%",
        "source_verification": "Enquêtes MICS/INSAE, rapports OIT/UNICEF",
        "responsable": "DGT",
        "frequence": "3-5 ans",
        "valeur_cible": 15
    },
    {
        "code": "GT2PKI04",
        "indicateur": "% d'assurés CNSS payés par virement électronique",
        "definition": "Part des assurés recevant leurs prestations par voie électronique.",
        "objectif": "Moderniser le paiement et améliorer la traçabilité.",
        "formule_type": "pourcentage",
        "numerateur_label": "Assurés payés par voie électronique",
        "denominateur_label": "Total assurés payés",
        "unite": "%",
        "source_verification": "Base de gestion CNSS, rapports financiers",
        "responsable": "CNSS",
        "frequence": "Semestrielle",
        "valeur_cible": 80
    },
    {
        "code": "GT2PKI05",
        "indicateur": "Délai moyen de liquidation des pensions CNSS",
        "definition": "Durée entre dépôt dossier complet et premier versement.",
        "objectif": "Garantir une transition financière rapide aux assurés.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre de dossiers liquidés",
        "unite": "jours",
        "source_verification": "Système de gestion CNSS, rapports Direction Prestations",
        "responsable": "CNSS",
        "frequence": "Trimestrielle",
        "valeur_cible": 45
    },
    {
        "code": "GT2PKI06",
        "indicateur": "Pourcentage de conflictualité dans le secteur public",
        "definition": "Proportion d'entités publiques ayant connu un conflit collectif déclaré.",
        "objectif": "Évaluer l'intensité des tensions sociales dans le secteur public.",
        "formule_type": "pourcentage",
        "numerateur_label": "Entités avec conflit déclaré",
        "denominateur_label": "Total entités secteur public",
        "unite": "%",
        "source_verification": "Registre des préavis de grève, rapports DGT",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 10
    },
    {
        "code": "GT2PKI07",
        "indicateur": "Pourcentage de conflictualité dans le secteur privé",
        "definition": "Proportion d'entreprises ayant connu un conflit collectif déclaré.",
        "objectif": "Évaluer le climat social dans les entreprises privées.",
        "formule_type": "pourcentage",
        "numerateur_label": "Entreprises avec conflit déclaré",
        "denominateur_label": "Total entreprises formelles",
        "unite": "%",
        "source_verification": "Registre des préavis de grève, rapports DGT",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 8
    },
    {
        "code": "GT2PKI08",
        "indicateur": "Pourcentage de représentativité des organisations syndicales",
        "definition": "Proportion des travailleurs adhérant à une organisation syndicale.",
        "objectif": "Évaluer la vitalité du mouvement syndical béninois.",
        "formule_type": "pourcentage",
        "numerateur_label": "Travailleurs syndiqués",
        "denominateur_label": "Total travailleurs formels",
        "unite": "%",
        "source_verification": "Répertoire des organisations syndicales, DGT",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 30
    },
    {
        "code": "GT2PKI09",
        "indicateur": "Pourcentage de règlement des litiges par conciliation",
        "definition": "Proportion des litiges réglés à l'amiable par l'Inspection du Travail.",
        "objectif": "Évaluer l'efficacité de la fonction de conciliation.",
        "formule_type": "pourcentage",
        "numerateur_label": "Litiges conciliés",
        "denominateur_label": "Total litiges",
        "unite": "%",
        "source_verification": "Registres de conciliation ITB, rapports DGT",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 70
    },
    {
        "code": "GT2PKI10",
        "indicateur": "Pourcentage de conformité des entreprises aux normes de sécurité (SST)",
        "definition": "Proportion des entreprises respectant les normes de santé/sécurité.",
        "objectif": "Mesurer l'effectivité de la réglementation SST.",
        "formule_type": "pourcentage",
        "numerateur_label": "Entreprises conformes",
        "denominateur_label": "Total entreprises contrôlées",
        "unite": "%",
        "source_verification": "Rapports de mission inspecteurs ITB, PV de contrôle",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 75
    },
    # NOUVEAU : GT2PKI11
    {
        "code": "GT2PKI11",
        "indicateur": "Pourcentage de travail non autorisé pour les enfants de 5 à 14 ans",
        "definition": "Proportion d'enfants de 5 à 14 ans exerçant une activité économique illicite au regard de la législation béninoise (âge minimum d'admission à l'emploi fixé à 15 ans).",
        "objectif": "Quantifier la part des enfants en âge scolaire obligatoire soumis à un travail illégal, évaluer le respect de la Convention OIT n°138.",
        "formule_type": "pourcentage",
        "numerateur_label": "Enfants de 5-14 ans en travail non autorisé",
        "denominateur_label": "Population totale des enfants de 5-14 ans",
        "unite": "%",
        "source_verification": "Enquêtes MICS/INSAE, EMICOV, rapports ITB/CNLTE, RGPH",
        "responsable": "DGT",
        "frequence": "3-5 ans",
        "valeur_cible": 10
    },
    # NOUVEAU : GT2PKI12 (remplace l'ancien GT2PKI11)
    {
        "code": "GT2PKI12",
        "indicateur": "Taux de conformité au droit du travail des enfants",
        "definition": "Proportion des entreprises, ménages employeurs et unités de production contrôlés dans lesquels aucune infraction aux dispositions légales régissant le travail des enfants n'a été constatée, ou dans lesquels les infractions ont été régularisées dans le délai imparti.",
        "objectif": "Mesurer l'effectivité de l'application des normes légales de protection des enfants au travail dans les secteurs contrôlés par l'Inspection du Travail.",
        "formule_type": "pourcentage",
        "numerateur_label": "Entreprises/unités sans infraction ou ayant régularisé",
        "denominateur_label": "Total entreprises/unités contrôlées",
        "unite": "%",
        "source_verification": "Rapports de mission ITB (volet travail des enfants), PV d'infractions, rapport CNLTE, données PNAETEHAR",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 80
    },
    # NOUVEAU : GT2PKI13
    {
        "code": "GT2PKI13",
        "indicateur": "Taux de conflictualité ayant donné lieu à une fermeture d'entreprise",
        "definition": "Proportion des conflits collectifs du travail ayant conduit à la fermeture temporaire ou définitive de l'entreprise concernée.",
        "objectif": "Mesurer l'intensité et la gravité des conflits sociaux dans le tissu économique béninois.",
        "formule_type": "pourcentage",
        "numerateur_label": "Conflits ayant entraîné une fermeture",
        "denominateur_label": "Total conflits collectifs enregistrés",
        "unite": "%",
        "source_verification": "Registre national des conflits collectifs ITB, PV de conciliation, RCCM, rapports DGT",
        "responsable": "DGT",
        "frequence": "Annuelle",
        "valeur_cible": 2
    },
    
    # ========== FONCTION PUBLIQUE (GT3PKI01 à GT3PKI16) ==========
    {
        "code": "GT3PKI01",
        "indicateur": "Taux de numérisation des archives des dossiers du personnel de l'État",
        "definition": "Proportion des dossiers agents numérisés dans le SIGRH.",
        "objectif": "Sécuriser les dossiers et faciliter la gestion des carrières.",
        "formule_type": "pourcentage",
        "numerateur_label": "Dossiers numérisés",
        "denominateur_label": "Total dossiers agents",
        "unite": "%",
        "source_verification": "Base SIGRH, rapports Direction Archivage",
        "responsable": "DGFP",
        "frequence": "Semestrielle",
        "valeur_cible": 100
    },
    {
        "code": "GT3PKI02",
        "indicateur": "Délai de parution des actes de carrière des agents de l'État",
        "definition": "Délai entre soumission dossier et publication de l'acte.",
        "objectif": "Réduire les retards et sécuriser les droits des agents.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre d'actes traités",
        "unite": "jours",
        "source_verification": "SI gestion des actes, Journal Officiel",
        "responsable": "DGFP",
        "frequence": "Trimestrielle",
        "valeur_cible": 30
    },
    {
        "code": "GT3PKI03",
        "indicateur": "Taux du Turn-over dans la fonction publique",
        "definition": "Proportion d'agents ayant quitté leur poste sur une période.",
        "objectif": "Mesurer la stabilité et le renouvellement des effectifs.",
        "formule_type": "pourcentage",
        "numerateur_label": "Nombre de départs",
        "denominateur_label": "Effectif total",
        "unite": "%",
        "source_verification": "Fichier mouvements DGFP, SIGRH",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 5
    },
    {
        "code": "GT3PKI04",
        "indicateur": "Pourcentage de procès gagnés par l'État en matière de contentieux de la fonction publique",
        "definition": "Proportion des affaires contentieuses gagnées par l'État.",
        "objectif": "Évaluer la qualité de la défense juridique de l'État.",
        "formule_type": "pourcentage",
        "numerateur_label": "Procès gagnés",
        "denominateur_label": "Total procès jugés",
        "unite": "%",
        "source_verification": "Greffe Cour Suprême, Direction Affaires Juridiques",
        "responsable": "SA",
        "frequence": "Annuelle",
        "valeur_cible": 75
    },
    {
        "code": "GT3PKI05",
        "indicateur": "Délai moyen de la procédure disciplinaire par instance disciplinaire",
        "definition": "Durée entre déclenchement procédure et décision définitive.",
        "objectif": "Garantir une procédure équitable dans des délais raisonnables.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre de procédures",
        "unite": "jours",
        "source_verification": "Registres instances disciplinaires, Direction Juridique",
        "responsable": "DGFP",
        "frequence": "Semestrielle",
        "valeur_cible": 60
    },
    {
        "code": "GT3PKI06",
        "indicateur": "Délai moyen de proclamation des résultats des concours",
        "definition": "Délai entre fin des épreuves et proclamation des résultats.",
        "objectif": "Évaluer la célérité administrative du recrutement.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre de concours",
        "unite": "jours",
        "source_verification": "PV jurys de concours, communiqués officiels",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 45
    },
    {
        "code": "GT3PKI07",
        "indicateur": "Délai moyen de liquidation et de remise des livrets de pension aux agents de l'État admis à la retraite (FNRB)",
        "definition": "Délai entre admission à la retraite et remise du livret.",
        "objectif": "Garantir une transition financière rapide aux retraités.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre de dossiers",
        "unite": "jours",
        "source_verification": "Base de données FNRB, rapports trimestriels",
        "responsable": "FNRB",
        "frequence": "Trimestrielle",
        "valeur_cible": 30
    },
    {
        "code": "GT3PKI08",
        "indicateur": "Nombre de pièces constitutives du dossier de retraite et de pension des agents de l'État",
        "definition": "Nombre de documents requis pour constituer un dossier de retraite.",
        "objectif": "Mesurer la simplification administrative du dossier.",
        "formule_type": "somme",
        "numerateur_label": "Nombre de pièces",
        "denominateur_label": None,
        "unite": "pièces",
        "source_verification": "Guide officiel FNRB/MTFP, circulaires",
        "responsable": "FNRB",
        "frequence": "Annuelle",
        "valeur_cible": 10
    },
    {
        "code": "GT3PKI09",
        "indicateur": "Délai de notification des actes d'admission à la retraite aux agents de l'État",
        "definition": "Délai entre date de départ et notification officielle.",
        "objectif": "Permettre aux agents de préparer sereinement leur transition.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre d'agents",
        "unite": "jours",
        "source_verification": "Registre DGFP, base SIGRH, rapports FNRB",
        "responsable": "DGFP",
        "frequence": "Semestrielle",
        "valeur_cible": 15
    },
    {
        "code": "GT3PKI010",
        "indicateur": "% des agents publics ayant souscrit au formulaire du code d'éthique",
        "definition": "Proportion d'agents ayant signé le Code d'Éthique.",
        "objectif": "Promouvoir l'intégrité dans la fonction publique.",
        "formule_type": "pourcentage",
        "numerateur_label": "Agents ayant souscrit",
        "denominateur_label": "Total agents actifs",
        "unite": "%",
        "source_verification": "Base des signatures DGRH, SIGRH",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 100
    },
    {
        "code": "GT3PKI11",
        "indicateur": "Nombre d'agents recrutés dans l'Administration publique (2006-2016 et 2016-2026)",
        "definition": "Nombre cumulatif d'agents recrutés dans la fonction publique.",
        "objectif": "Évaluer la capacité de renouvellement des effectifs.",
        "formule_type": "cumul_annuel",
        "numerateur_label": "Agents recrutés dans l'année",
        "denominateur_label": None,
        "unite": "agents",
        "source_verification": "Fichier des recrutements DGRH, Journal Officiel",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 25000
    },
    {
        "code": "GT3PKI12",
        "indicateur": "Délai moyen de mise à disposition des ministères des agents nouvellement recrutés",
        "definition": "Délai entre résultats du concours et prise de service.",
        "objectif": "Réduire la période d'inactivité post-recrutement.",
        "formule_type": "moyenne",
        "numerateur_label": "Somme des délais",
        "denominateur_label": "Nombre de nouveaux recrutés",
        "unite": "jours",
        "source_verification": "Registre des affectations DGRH",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 30
    },
    {
        "code": "GT3PKI13",
        "indicateur": "% des agents nouvellement recrutés ayant souscrit au code d'éthique",
        "definition": "Proportion de nouveaux recrutés ayant signé le Code d'Éthique.",
        "objectif": "Inculquer les valeurs de service public dès l'entrée.",
        "formule_type": "pourcentage",
        "numerateur_label": "Nouveaux recrutés signataires",
        "denominateur_label": "Total nouveaux recrutés",
        "unite": "%",
        "source_verification": "Base des signatures DGRH, rapports formation",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 100
    },
    {
        "code": "GT3PKI14",
        "indicateur": "Nombre d'agents recrutés dans la fonction publique par secteur (2016-2026)",
        "definition": "Décompte des recrutements ventilé par secteur ministériel.",
        "objectif": "Analyser la cohérence entre recrutements et besoins sectoriels.",
        "formule_type": "cumul_annuel",
        "numerateur_label": "Agents recrutés par ministère",
        "denominateur_label": None,
        "unite": "agents",
        "source_verification": "Fichier national des recrutements DGRH, rapports sectoriels",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 0
    },
    # NOUVEAU : GT3PKI15 (remplace l'ancien GT3PKI15 - Taux d'absentéisme)
    {
        "code": "GT3PKI15",
        "indicateur": "Nombre de personnes handicapées recrutées dans la fonction publique",
        "definition": "Nombre cumulatif de personnes en situation de handicap (PSH) recrutées dans la fonction publique béninoise, conformément aux quotas légaux.",
        "objectif": "Évaluer le respect des engagements d'inclusion des personnes handicapées dans la fonction publique.",
        "formule_type": "cumul_annuel",
        "numerateur_label": "PSH recrutées dans l'année",
        "denominateur_label": None,
        "unite": "personnes",
        "source_verification": "Registre DGRH, suivi des quotas Affaires Sociales",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 1000
    },
    # NOUVEAU : GT3PKI16
    {
        "code": "GT3PKI16",
        "indicateur": "Ratio d'encadrement par catégorie dans la Fonction Publique",
        "definition": "Rapport entre le nombre d'agents d'encadrement d'une catégorie hiérarchique donnée (A, B ou C) et le nombre total d'agents relevant de la catégorie ou du corps placé sous leur autorité directe (A/B, B/C, A+B/C).",
        "objectif": "Évaluer l'adéquation de la structure hiérarchique de la Fonction Publique aux exigences de pilotage des politiques publiques.",
        "formule_type": "ratio",
        "numerateur_label": "Agents catégorie supérieure",
        "denominateur_label": "Agents catégorie inférieure",
        "unite": "ratio",
        "source_verification": "Fichier statistique DGFP, SIGRH, Annuaire statistique FP",
        "responsable": "DGFP",
        "frequence": "Annuelle",
        "valeur_cible": 1.5
    },
]

print("=" * 70)
print("IMPORTATION DES INDICATEURS DU BILAN DECENNAL MTFP")
print("=" * 70)

# Supprimer les anciens KPIs
anciens = KPI.query.count()
KPI.query.delete()
db.session.commit()
print(f"\n🗑️ {anciens} anciens indicateurs supprimés")

print("\n📥 Ajout des nouveaux indicateurs...\n")

compteur = 0
for k in indicateurs:
    # Déterminer l'ID du groupe
    code_prefix = k["code"][:4]  # GT1P, GT2P, GT3P
    if "GT1" in code_prefix:
        groupe_id = 1
    elif "GT2" in code_prefix:
        groupe_id = 2
    else:
        groupe_id = 3
    
    kpi = KPI(
        axe_strategique="PAG 2 (2021-2026)",
        groupe_id=groupe_id,
        code=k["code"],
        indicateur=k["indicateur"],
        definition=k["definition"],
        objectif=k["objectif"],
        valeur_cible=k["valeur_cible"],
        valeur_atteinte=0,
        unite=k["unite"],
        formule_type=k["formule_type"],
        numerateur_label=k["numerateur_label"],
        denominateur_label=k["denominateur_label"],
        source_verification=k["source_verification"],
        responsable=k["responsable"],
        frequence_collecte=k["frequence"],
        numerateur_valeur=0,
        denominateur_valeur=0,
        observations=""
    )
    db.session.add(kpi)
    compteur += 1
    print(f"  ✅ {k['code']} - {k['indicateur'][:55]}...")

db.session.commit()

print(f"\n" + "=" * 70)
print(f"✅ {compteur} indicateurs importés avec succès !")
print("=" * 70)

# Vérification par groupe
print("\n📊 RÉPARTITION PAR GROUPE THÉMATIQUE:")
for g in GroupeThematique.query.all():
    count = KPI.query.filter_by(groupe_id=g.id).count()
    print(f"   📌 Groupe {g.id} - {g.nom}: {count} indicateurs")

# Récapitulatif par type de formule
print("\n📐 RÉPARTITION PAR TYPE DE FORMULE:")
types = {}
for k in KPI.query.all():
    t = k.formule_type or "non defini"
    types[t] = types.get(t, 0) + 1
for t, count in sorted(types.items()):
    print(f"   📊 {t}: {count}")

print("\n✨ Importation terminée !")
exit()