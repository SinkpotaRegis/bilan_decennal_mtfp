from app import create_app
from app.models.database import db, KPI
from sqlalchemy import text

print("=== AJOUT DES DONNEES D'ANALYSE ===")

app = create_app()
ctx = app.app_context()
ctx.push()

# Données par défaut pour les facteurs explicatifs, benchmarking et recommandations
contenus = {
    'Taux de satisfaction des usagers': {
        'facteurs': "1) Qualite de l'accueil et de l'information au guichet\n2) Delais de traitement des dossiers\n3) Accessibilite des services (CCSP/GSRU)\n4) Formation des agents aux relations publiques",
        'benchmarking': "UEMOA: 55-65% | Senegal: 58% | Cote d'Ivoire: 52% | Objectif PAG Benin 2026: 75%",
        'recommandations': "1) Deployer des enquetes de satisfaction systematiques\n2) Former les agents sur la qualite de service\n3) Digitaliser les procedures pour reduire les delais"
    },
    'Taux de satisfaction des agents': {
        'facteurs': "1) Conditions de travail et equipements\n2) Perspectives de carriere et promotions\n3) Dialogue social et relations hierarchiques\n4) Remunerations et avantages sociaux",
        'benchmarking': "Fonction publique beninoise: ≈65% | Objectif MTFP: 75% | Benchmark regional: 70%",
        'recommandations': "1) Organiser des entretiens annuels de carriere\n2) Ameliorer les conditions de travail\n3) Renforcer le dialogue social"
    },
    'services publics dematerialises': {
        'facteurs': "1) Budget alloue a la DSI\n2) Disponibilite des competences techniques\n3) Couverture reseau\n4) Volonte politique",
        'benchmarking': "Benin numerique 2026: 80% | Rwanda: 95% | Senegal: 45% | Cote d'Ivoire: 38%",
        'recommandations': "1) Finaliser le catalogue des services\n2) Renforcer l'accompagnement des usagers\n3) Assurer l'interoperabilite"
    }
}

compteur = 0
for mot_cle, data in contenus.items():
    kpis = KPI.query.filter(KPI.indicateur.like(f'%{mot_cle}%')).all()
    for kpi in kpis:
        if not kpi.facteurs_explicatifs:
            kpi.facteurs_explicatifs = data['facteurs']
            kpi.benchmarking = data['benchmarking']
            kpi.recommandations = data['recommandations']
            compteur += 1
            print(f"✅ Mis a jour: {kpi.indicateur[:50]}...")

db.session.commit()
print(f"\n✅ {compteur} indicateurs mis a jour")

exit()