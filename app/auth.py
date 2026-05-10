# app/auth.py
from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import check_password_hash, generate_password_hash
from app.models.database import db, User
from app.decorators import log_action  # ← AJOUT

bp = Blueprint('auth', __name__)


@bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        if current_user.role == 'admin':
            return redirect(url_for('api.admin_dashboard'))
        elif current_user.role == 'validateur':
            return redirect(url_for('api.validateur_dashboard'))
        elif current_user.role == 'collecteur':
            return redirect(url_for('api.collecteur_dashboard'))
        return redirect(url_for('api.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        user = User.query.filter_by(username=username).first()
        
        if user and check_password_hash(user.password, password):
            login_user(user)
            
            # LOG de connexion
            from app.models.database import Log
            from datetime import datetime
            try:
                log = Log(
                    user_id=user.id,
                    action='LOGIN',
                    details=f"Connexion réussie depuis {request.remote_addr}",
                    ip_address=request.remote_addr,
                    created_at=datetime.now()
                )
                db.session.add(log)
                db.session.commit()
            except Exception as e:
                print(f"[LOG_ERROR] {e}")
            
            flash(f'Bienvenue {user.username}', 'success')
            
            if user.role == 'admin':
                return redirect(url_for('api.admin_dashboard'))
            elif user.role == 'validateur':
                return redirect(url_for('api.validateur_dashboard'))
            elif user.role == 'collecteur':
                return redirect(url_for('api.collecteur_dashboard'))
            return redirect(url_for('api.dashboard'))
        else:
            flash('Identifiants incorrects', 'danger')
    
    return render_template('login.html')


@bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username         = request.form.get('username', '').strip()
        email            = request.form.get('email', '').strip()
        password         = request.form.get('password', '')
        confirm_password = request.form.get('confirm_password', '')
 
        # "structure" contient maintenant "DPAF,DGT,DGFP"
        # (valeur de l'input caché générée par le JS du formulaire)
        structure_raw = request.form.get('structure', '').strip()
 
        # Nettoyage : retirer les espaces autour de chaque code, supprimer les doublons
        codes = [c.strip() for c in structure_raw.split(',') if c.strip()]
        codes = list(dict.fromkeys(codes))          # supprime les doublons, conserve l'ordre
        structure = ','.join(codes)                  # ex: "DPAF,DGT,DGFP"
 
        # ── Validations ──────────────────────────────────────────────────
        if not username:
            flash("Le nom d'utilisateur est obligatoire.", 'danger')
            return redirect(url_for('auth.register'))
 
        if User.query.filter_by(username=username).first():
            flash("Ce nom d'utilisateur est déjà utilisé.", 'danger')
            return redirect(url_for('auth.register'))
 
        if not email:
            flash("L'adresse email est obligatoire.", 'danger')
            return redirect(url_for('auth.register'))
 
        if User.query.filter_by(email=email).first():
            flash("Cette adresse email est déjà utilisée.", 'danger')
            return redirect(url_for('auth.register'))
 
        if len(password) < 6:
            flash("Le mot de passe doit contenir au moins 6 caractères.", 'danger')
            return redirect(url_for('auth.register'))
 
        if password != confirm_password:
            flash("Les mots de passe ne correspondent pas.", 'danger')
            return redirect(url_for('auth.register'))
 
        if not codes:
            flash("Veuillez sélectionner au moins une direction affectée.", 'danger')
            return redirect(url_for('auth.register'))
 
        # ── Création de l'utilisateur ─────────────────────────────────────
        new_user = User(
            username  = username,
            email     = email,
            password  = generate_password_hash(password),
            role      = 'collecteur',
            structure = structure,      # ex: "DPAF,DGT,DGFP"
            is_active = True,
        )
        db.session.add(new_user)
        db.session.commit()
 
        flash(
            f"Compte créé ! Directions affectées : {structure.replace(',', ', ')}. "
            f"Connectez-vous pour accéder à la plateforme.",
            'success'
        )
        return redirect(url_for('auth.login'))
 
    return render_template('register.html')

@bp.route('/logout')
@login_required
def logout():
    # LOG de déconnexion
    try:
        from app.models.database import Log
        from datetime import datetime
        log = Log(
            user_id=current_user.id,
            action='LOGOUT',
            details=f"Déconnexion de {current_user.username}",
            ip_address=request.remote_addr,
            created_at=datetime.now()
        )
        db.session.add(log)
        db.session.commit()
    except Exception as e:
        print(f"[LOG_ERROR] {e}")
    
    logout_user()
    flash('Déconnexion réussie', 'info')
    return redirect(url_for('auth.login'))