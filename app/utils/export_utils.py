def get_kpi_data(kpi_id, db):
    from sqlalchemy import text
    
    result = db.session.execute(
        text('SELECT * FROM kpis WHERE id = :id'),
        {'id': kpi_id}
    )
    kpi = result.fetchone()
    
    if not kpi:
        return None
    
    annuel_result = db.session.execute(
        text('SELECT annee, numerateur_valeur, denominateur_valeur, valeur_calculee, commentaire FROM kpis_annuels WHERE kpi_id = :kpi_id ORDER BY annee'),
        {'kpi_id': kpi_id}
    )
    annuel = annuel_result.fetchall()
    
    docs_result = db.session.execute(
        text('SELECT annee, titre, chemin_fichier, url_sharepoint, date_ajout FROM preuves_documentaires WHERE kpi_id = :kpi_id ORDER BY annee'),
        {'kpi_id': kpi_id}
    )
    documents = docs_result.fetchall()
    
    docs_par_annee = {}
    for doc in documents:
        annee = doc[0]
        if annee not in docs_par_annee:
            docs_par_annee[annee] = []
        docs_par_annee[annee].append({
            'titre': doc[1] or f"Document_{annee}",
            'chemin': doc[2],
            'url': doc[3],
            'date': doc[4]
        })
    
    return {
        'kpi': kpi,
        'annuel': annuel,
        'annees': [row[0] for row in annuel],
        'valeurs': [row[3] for row in annuel],
        'numerateurs': [row[1] for row in annuel],
        'denominateurs': [row[2] for row in annuel],
        'commentaires': [row[4] or '' for row in annuel],
        'documents': docs_par_annee
    }

def get_groupe_nom(groupe_id):
    if groupe_id == 1:
        return "Travail et Sécurité Sociale"
    elif groupe_id == 2:
        return "Fonction Publique"
    else:
        return "Gouvernance et Réformes"