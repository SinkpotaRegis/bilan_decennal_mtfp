
# app/__init__.py
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# NE PAS CREER db ICI - on va l'importer depuis models
import os
from flask import Flask
from flask_cors import CORS
from flask_login import LoginManager
from app.models.database import db, User
from sqlalchemy import text


login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    # app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bilan_decennal.db'
        # Configuration de la base de données selon l'environnement
    if os.environ.get('RENDER'):
        # Sur Render, utilise un fichier temporaire (disque éphémère)
        db_path = '/tmp/bilan_decennal.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
    else:
        # Environnement local
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///bilan_decennal.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.secret_key = 'mtfp-bilan-2026-secret-key'
    
    CORS(app)
    
    # IMPORTANT : Utiliser db depuis models
    from app.models.database import db
    db.init_app(app)
    
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    login_manager.login_message = 'Veuillez vous connecter pour accéder à cette page'

    @login_manager.user_loader
    def load_user(user_id):
        from app.models.database import User
        return User.query.get(int(user_id))

    # IMPORT DES BLUEPRINTS
    from app.routes.api import bp as api_bp
    app.register_blueprint(api_bp)
    
    from app.auth import bp as auth_bp
    app.register_blueprint(auth_bp)

    with app.app_context():
        db.create_all()
        
        # Initialisation des groupes
        from app.models.database import GroupeThematique
        if GroupeThematique.query.count() == 0:
            groupes = [
                GroupeThematique(nom="Travail et Securite Sociale", code="GT_TRAVAIL"),
                GroupeThematique(nom="Fonction Publique", code="GT_FP"),
                GroupeThematique(nom="Gouvernance et Reformes", code="GT_GOUV"),
            ]
            db.session.add_all(groupes)
            db.session.commit()
        
        # Création admin
        from app.models.database import User
        from werkzeug.security import generate_password_hash
        admin = User.query.filter_by(username='admin').first()
        if not admin:
            admin = User(
                username='admin',
                email='admin@mtfp.bj',
                password=generate_password_hash('admin123'),
                role='admin',
                structure='DPAF'
            )
            db.session.add(admin)
            db.session.commit()
            print("✅ Admin créé: admin / admin123")
    
    return app
    
    return app

def init_database():
    from app.models.database import GroupeThematique, KPI
    
    if GroupeThematique.query.count() == 0:
        groupes = [
            GroupeThematique(nom="Travail et Securite Sociale", code="GT_TRAVAIL"),
            GroupeThematique(nom="Fonction Publique", code="GT_FP"),
            GroupeThematique(nom="Gouvernance et Reformes", code="GT_GOUV"),
        ]
        db.session.add_all(groupes)
        db.session.commit()
