from app import create_app
from app.models.database import db, KPI
from sqlalchemy import text

app = create_app()
ctx = app.app_context()
ctx.push()

print("=== VÉRIFICATION DES DONNÉES ===\n")

# Compter les KPIs
total_kpis = KPI.query.count()
print(f"📊 Total KPIs: {total_kpis} (devrait être 41)")

# Vérifier les colonnes d'analyse
kpis_avec_facteurs = KPI.query.filter(KPI.facteurs_explicatifs.isnot(None)).count()
kpis_avec_benchmarking = KPI.query.filter(KPI.benchmarking.isnot(None)).count()
kpis_avec_recommandations = KPI.query.filter(KPI.recommandations.isnot(None)).count()

print(f"\n📋 Données d'analyse:")
print(f"   - Facteurs explicatifs: {kpis_avec_facteurs}/41")
print(f"   - Benchmarking: {kpis_avec_benchmarking}/41")
print(f"   - Recommandations: {kpis_avec_recommandations}/41")

# Vérifier les groupes
groupes = db.session.execute(text("SELECT id, nom FROM groupes_thematiques")).fetchall()
print(f"\n🏷️ Groupes thématiques:")
for g in groupes:
    count = KPI.query.filter_by(groupe_id=g[0]).count()
    print(f"   - {g[1]}: {count} indicateurs")

# Vérifier les types d'indicateurs
types = db.session.execute(text("SELECT formule_type, COUNT(*) FROM kpis GROUP BY formule_type")).fetchall()
print(f"\n📐 Types d'indicateurs:")
for t in types:
    print(f"   - {t[0]}: {t[1]}")

exit()