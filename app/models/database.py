from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import UserMixin
from enum import Enum

db = SQLAlchemy()


class RoleEnum(Enum):
    """Énumération des rôles d'utilisateur disponibles"""
    COLLECTEUR = 'collecteur'
    VALIDATEUR = 'validateur'
    ADMIN = 'admin'


class GroupeThematique(db.Model):
    __tablename__ = 'groupes_thematiques'
    id = db.Column(db.Integer, primary_key=True)
    nom = db.Column(db.String(100), nullable=False)
    code = db.Column(db.String(20), unique=True)
    description = db.Column(db.Text)
    president = db.Column(db.String(150))
    rapporteur = db.Column(db.String(150))
    structures = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'nom': self.nom,
            'code': self.code,
            'description': self.description,
            'president': self.president,
            'rapporteur': self.rapporteur,
            'structures': self.structures.split(',') if self.structures else []
        }


class KPI(db.Model):
    __tablename__ = 'kpis'
    id = db.Column(db.Integer, primary_key=True)
    axe_strategique = db.Column(db.String(200))
    groupe_id = db.Column(db.Integer, db.ForeignKey('groupes_thematiques.id'))
    code = db.Column(db.String(20))
    indicateur = db.Column(db.String(300), nullable=False)
    definition = db.Column(db.Text)
    objectif = db.Column(db.Text)
    valeur_cible = db.Column(db.Float)
    valeur_atteinte = db.Column(db.Float)
    unite = db.Column(db.String(50))
    source_verification = db.Column(db.String(200))
    responsable = db.Column(db.String(150))
    observations = db.Column(db.Text)
    fichier_pdf = db.Column(db.String(500))
    frequence_collecte = db.Column(db.String(50))

    formule_type = db.Column(db.String(50))
    numerateur_label = db.Column(db.String(200))
    denominateur_label = db.Column(db.String(200))
    numerateur_valeur = db.Column(db.Float, default=0)
    denominateur_valeur = db.Column(db.Float, default=0)
    preuve_numerique = db.Column(db.String(500))
    
    facteurs_explicatifs = db.Column(db.Text)
    benchmarking = db.Column(db.Text)
    recommandations = db.Column(db.Text)

    def get_resultat_label(self):
        formule_type = (self.formule_type or '').lower()
        indicateur = (self.indicateur or '').lower()
        unite = (self.unite or '').lower()

        if formule_type == 'pourcentage':
            return 'Taux' if 'taux' in indicateur else 'Pourcentage'
        if formule_type == 'ratio':
            return 'Ratio'
        if formule_type == 'moyenne':
            if 'délai' in indicateur or 'delai' in indicateur or 'jour' in unite:
                return 'Délai moyen'
            return 'Moyenne'
        if formule_type in ('somme', 'cumul_annuel', 'nombre'):
            return 'Nombre'
        if formule_type in ('score_externe', 'indice'):
            return 'Indice'
        if formule_type == 'tcac':
            return 'TCAC'
        return 'Résultat'

    def get_resultat_unite(self):
        formule_type = (self.formule_type or '').lower()
        unite = (self.unite or '').strip()
        unite_lower = unite.lower()
        indicateur = (self.indicateur or '').lower()

        if formule_type == 'pourcentage':
            return '%'
        if formule_type == 'moyenne' and ('délai' in indicateur or 'delai' in indicateur or 'jour' in unite_lower):
            return unite or 'jours'
        if formule_type in ('somme', 'cumul_annuel', 'nombre', 'score_externe', 'indice', 'tcac'):
            return unite
        if formule_type == 'ratio':
            return unite
        return unite

    def calculer_valeur(self, numerateur=None, denominateur=None):
        numerateur = self.numerateur_valeur if numerateur is None else numerateur
        denominateur = self.denominateur_valeur if denominateur is None else denominateur
        formule_type = (self.formule_type or '').lower()

        if formule_type == 'pourcentage' and denominateur and denominateur > 0:
            return (numerateur / denominateur) * 100
        elif formule_type in ('somme', 'cumul_annuel', 'nombre', 'score_externe', 'indice'):
            return numerateur
        elif formule_type in ('moyenne', 'ratio') and denominateur and denominateur > 0:
            return numerateur / denominateur
        elif formule_type == 'tcac':
            return self.valeur_atteinte
        else:
            return self.valeur_atteinte

    def get_seuil_performance(self, taux):
        if taux >= 80:
            return {'niveau': 'Satisfaisant', 'icone': '🟢', 'classe': 'status-success'}
        elif taux >= 60:
            return {'niveau': 'Acceptable', 'icone': '🟡', 'classe': 'status-warning'}
        elif taux >= 40:
            return {'niveau': 'À surveiller', 'icone': '🟠', 'classe': 'status-warning'}
        else:
            return {'niveau': 'Critique', 'icone': '🔴', 'classe': 'status-danger'}

    def to_dict(self):
        taux = (self.calculer_valeur() / self.valeur_cible * 100) if self.valeur_cible and self.valeur_cible > 0 else 0
        seuil = self.get_seuil_performance(taux)
        return {
            'id': self.id,
            'groupe_id': self.groupe_id,
            'code': self.code,
            'indicateur': self.indicateur,
            'definition': self.definition,
            'objectif': self.objectif,
            'valeur_cible': self.valeur_cible,
            'valeur_atteinte': self.calculer_valeur(),
            'taux_atteinte': round(taux, 1),
            'unite': self.unite,
            'source_verification': self.source_verification,
            'responsable': self.responsable,
            'observations': self.observations,
            'fichier_pdf': self.fichier_pdf,
            'formule_type': self.formule_type,
            'resultat_label': self.get_resultat_label(),
            'resultat_unite': self.get_resultat_unite(),
            'numerateur_label': self.numerateur_label,
            'denominateur_label': self.denominateur_label,
            'numerateur_valeur': self.numerateur_valeur,
            'denominateur_valeur': self.denominateur_valeur,
            'frequence_collecte': self.frequence_collecte,
            'preuve_numerique': self.preuve_numerique,
            'facteurs_explicatifs': self.facteurs_explicatifs,
            'benchmarking': self.benchmarking,
            'recommandations': self.recommandations,
            'seuil_niveau': seuil['niveau'],
            'seuil_icone': seuil['icone'],
            'seuil_classe': seuil['classe']
        }


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True, nullable=False)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(50), default=RoleEnum.COLLECTEUR.value, nullable=False)
    structure = db.Column(db.String(200))
    direction = db.Column(db.String(100))  # Ajouté pour filtrer par direction
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    last_login = db.Column(db.DateTime)  # Ajouté
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))  # Ajouté

    def to_dict(self):
        return {
            'id': self.id,
            'username': self.username,
            'email': self.email,
            'role': self.role,
            'structure': self.structure,
            'direction': self.direction,
            'is_active': self.is_active
        }


class CommentaireAnnuel(db.Model):
    __tablename__ = 'commentaires_annuels'
    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('kpis.id'))
    annee = db.Column(db.Integer, nullable=False)
    commentaire = db.Column(db.Text)
    date_ajout = db.Column(db.String(50))
    ajoute_par = db.Column(db.String(100))


class PreuveDocumentaire(db.Model):
    __tablename__ = 'preuves_documentaires'
    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('kpis.id'))
    annee = db.Column(db.Integer, nullable=False)
    titre = db.Column(db.String(200))
    type_fichier = db.Column(db.String(50))
    chemin_fichier = db.Column(db.String(500))
    url_sharepoint = db.Column(db.String(500))
    date_ajout = db.Column(db.String(50))
    ajoute_par = db.Column(db.String(100))


class KPISAnnuel(db.Model):
    __tablename__ = 'kpis_annuels'
    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('kpis.id'))
    annee = db.Column(db.Integer, nullable=False)
    numerateur_valeur = db.Column(db.Float, default=0)
    denominateur_valeur = db.Column(db.Float, default=0)
    valeur_calculee = db.Column(db.Float, default=0)
    commentaire = db.Column(db.Text)
    direction_concernee = db.Column(db.String(200))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'))

    def to_dict(self):
        return {
            'id': self.id,
            'kpi_id': self.kpi_id,
            'annee': self.annee,
            'numerateur': self.numerateur_valeur,
            'denominateur': self.denominateur_valeur,
            'valeur': self.valeur_calculee,
            'commentaire': self.commentaire,
            'direction_concernee': self.direction_concernee,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'created_by': self.created_by
        }


class SeuilPerformance(db.Model):
    __tablename__ = 'seuils_performance'
    id = db.Column(db.Integer, primary_key=True)
    kpi_id = db.Column(db.Integer, db.ForeignKey('kpis.id'), unique=True)
    seuil_bas = db.Column(db.Float, default=40)
    seuil_moyen = db.Column(db.Float, default=60)
    seuil_haut = db.Column(db.Float, default=80)
    interpretation_bas = db.Column(db.Text)
    interpretation_moyen = db.Column(db.Text)
    interpretation_haut = db.Column(db.Text)

    def to_dict(self):
        return {
            'id': self.id,
            'kpi_id': self.kpi_id,
            'seuil_bas': self.seuil_bas,
            'seuil_moyen': self.seuil_moyen,
            'seuil_haut': self.seuil_haut,
            'interpretation_bas': self.interpretation_bas,
            'interpretation_moyen': self.interpretation_moyen,
            'interpretation_haut': self.interpretation_haut
        }


class Log(db.Model):
    """Table des logs de journalisation - Version complète"""
    __tablename__ = 'logs'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    action = db.Column(db.String(50), nullable=False)
    entity_type = db.Column(db.String(50))
    entity_id = db.Column(db.Integer)
    details = db.Column(db.Text)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(256))  # ← AJOUTÉ : navigateur de l'utilisateur
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relations
    user = db.relationship('User', backref='logs')
    
    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'user_name': self.user.username if self.user else None,
            'action': self.action,
            'entity_type': self.entity_type,
            'entity_id': self.entity_id,
            'details': self.details,
            'ip_address': self.ip_address,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }
    
    def __repr__(self):
        return f'<Log {self.action} by user {self.user_id} at {self.created_at}>'


class Validation(db.Model):
    """Table des validations des KPI"""
    __tablename__ = 'validations'
    
    id = db.Column(db.Integer, primary_key=True)
    kpi_code = db.Column(db.String(20), nullable=False)
    annee = db.Column(db.Integer)
    periode = db.Column(db.String(10))
    validateur_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    statut = db.Column(db.String(20), default='en_attente')
    commentaire = db.Column(db.Text)
    ancienne_valeur = db.Column(db.Float)
    nouvelle_valeur = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relations
    validateur = db.relationship('User', backref='validations')
    
    def to_dict(self):
        return {
            'id': self.id,
            'kpi_code': self.kpi_code,
            'annee': self.annee,
            'periode': self.periode,
            'statut': self.statut,
            'commentaire': self.commentaire,
            'ancienne_valeur': self.ancienne_valeur,
            'nouvelle_valeur': self.nouvelle_valeur,
            'created_at': self.created_at.strftime('%Y-%m-%d %H:%M:%S') if self.created_at else None
        }