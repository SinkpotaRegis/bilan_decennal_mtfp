"""
Script de nettoyage et reconfiguration de GT3PKI16 - Taux d'encadrement par catégorie
Supprime toutes les données liées à cet indicateur et le reconfigure correctement
"""

from app import create_app
from app.models.database import db, KPI, KPISAnnuel, PreuveDocumentaire, CommentaireAnnuel, SeuilPerformance

app = create_app()
ctx = app.app_context()
ctx.push()

code_kpi = 'GT3PKI16'

# Récupérer l'indicateur
kpi = KPI.query.filter_by(code=code_kpi).first()

if not kpi:
    print(f"❌ Indicateur {code_kpi} non trouvé")
    ctx.pop()
    exit()

print(f"✅ Indicateur trouvé: {kpi.code} - {kpi.indicateur}")
print(f"   ID: {kpi.id}")

# ============================================================
# 1. SUPPRESSION DE TOUTES LES DONNÉES LIÉES
# ============================================================

print("\n🗑️ Suppression des données liées...")

# Supprimer les preuves documentaires
preuves = PreuveDocumentaire.query.filter_by(kpi_id=kpi.id).all()
print(f"   - {len(preuves)} preuve(s) documentaire(s) supprimée(s)")
for p in preuves:
    db.session.delete(p)

# Supprimer les commentaires annuels
commentaires = CommentaireAnnuel.query.filter_by(kpi_id=kpi.id).all()
print(f"   - {len(commentaires)} commentaire(s) annuel(s) supprimé(s)")
for c in commentaires:
    db.session.delete(c)

# Supprimer les valeurs annuelles (KPISAnnuel)
valeurs = KPISAnnuel.query.filter_by(kpi_id=kpi.id).all()
print(f"   - {len(valeurs)} valeur(s) annuelle(s) supprimée(s)")
for v in valeurs:
    db.session.delete(v)

# Supprimer les seuils de performance
seuil = SeuilPerformance.query.filter_by(kpi_id=kpi.id).first()
if seuil:
    print(f"   - Seuil de performance supprimé")
    db.session.delete(seuil)

db.session.commit()
print("\n✅ Toutes les données liées ont été supprimées")

# ============================================================
# 2. RECONFIGURATION DE L'INDICATEUR
# ============================================================

print("\n📝 Reconfiguration de l'indicateur...")

kpi.indicateur = "Taux d'encadrement par catégorie dans la Fonction Publique"
kpi.definition = """Proportion des effectifs de la Fonction Publique par catégorie hiérarchique (A, B, C), exprimée en pourcentage de l'effectif total. 
L'indicateur permet de mesurer la répartition des agents entre :
- Catégorie A : Encadrement supérieur (cadres de conception et de direction)
- Catégorie B : Maîtrise (cadres d'application et de supervision)
- Catégorie C : Exécution (agents d'exécution)"""

kpi.objectif = """Évaluer la structure hiérarchique de la Fonction Publique et orienter les politiques de recrutement pour garantir un équilibre organisationnel optimal. 
Un déséquilibre (trop peu de cadres ou pyramide inversée) peut nuire à la qualité des services rendus."""

kpi.formule_type = "pourcentage"
kpi.numerateur_label = "Effectif de la catégorie concernée"
kpi.denominateur_label = "Effectif total (A+B+C)"
kpi.resultat_label = "Taux"
kpi.resultat_unite = "%"
kpi.unite = "%"
kpi.valeur_cible = 35.0
kpi.frequence_collecte = "Annuelle"
kpi.source_verification = "Direction Générale de la Fonction Publique (DGFP) - fichier statistique des effectifs, Système d'Information de Gestion des Ressources Humaines (SIGRH), Annuaire statistique de la Fonction Publique"
kpi.responsable = "DGFP"
kpi.validation_status = "en_attente"
kpi.observations = ""
kpi.facteurs_explicatifs = ""
kpi.benchmarking = ""
kpi.recommandations = ""

db.session.commit()

print("\n📊 Nouvelle configuration :")
print(f"   - Intitulé: {kpi.indicateur}")
print(f"   - Formule type: {kpi.formule_type}")
print(f"   - Unité: {kpi.unite}")
print(f"   - Numérateur: {kpi.numerateur_label}")
print(f"   - Dénominateur: {kpi.denominateur_label}")
print(f"   - Valeur cible: {kpi.valeur_cible}%")

# ============================================================
# 3. AJOUT DES SEUILS DE PERFORMANCE (optionnel)
# ============================================================

print("\n📈 Ajout des seuils de performance...")

nouveau_seuil = SeuilPerformance(
    kpi_id=kpi.id,
    seuil_bas=30.0,
    seuil_moyen=50.0,
    seuil_haut=70.0,
    interpretation_bas="Structure déséquilibrée - Trop peu d'agents dans cette catégorie par rapport aux besoins",
    interpretation_moyen="Structure acceptable - Des efforts sont encore nécessaires",
    interpretation_haut="Structure satisfaisante - Bon équilibre des effectifs"
)
db.session.add(nouveau_seuil)
db.session.commit()

print(f"   ✅ Seuils ajoutés : bas={nouveau_seuil.seuil_bas}%, moyen={nouveau_seuil.seuil_moyen}%, haut={nouveau_seuil.seuil_haut}%")

# ============================================================
# 4. VÉRIFICATION FINALE
# ============================================================

print("\n" + "=" * 60)
print("📊 VÉRIFICATION FINALE")
print("=" * 60)

# Vérifier le KPI
kpi_verif = KPI.query.filter_by(code=code_kpi).first()
print(f"\n📌 KPI :")
print(f"   ID: {kpi_verif.id}")
print(f"   Code: {kpi_verif.code}")
print(f"   Intitulé: {kpi_verif.indicateur}")
print(f"   Formule type: {kpi_verif.formule_type}")
print(f"   Unité: {kpi_verif.unite}")

# Vérifier les seuils
seuil_verif = SeuilPerformance.query.filter_by(kpi_id=kpi.id).first()
if seuil_verif:
    print(f"\n📈 Seuils de performance :")
    print(f"   Seuil bas: {seuil_verif.seuil_bas}%")
    print(f"   Seuil moyen: {seuil_verif.seuil_moyen}%")
    print(f"   Seuil haut: {seuil_verif.seuil_haut}%")

# Vérifier qu'il n'y a plus de données annuelles
valeurs_restantes = KPISAnnuel.query.filter_by(kpi_id=kpi.id).count()
print(f"\n📊 Données annuelles restantes: {valeurs_restantes}")

print("\n" + "=" * 60)
print("✨ Configuration terminée avec succès !")
print("=" * 60)

ctx.pop()