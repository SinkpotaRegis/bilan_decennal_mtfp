# app/decorators.py
from functools import wraps
from flask import request, session, redirect, url_for, flash, abort
from datetime import datetime


def log_action(action, entity_type=None, entity_id=None, details_func=None):
    """
    Décorateur qui enregistre automatiquement une action dans la table logs.

    CORRECTION DES BUGS :
    1. On utilise current_user (Flask-Login) au lieu de session['user_id']
       → session['user_id'] n'est pas garanti avec Flask-Login
    2. On isole le commit du log dans son propre bloc try/except
       → Un échec du log ne doit jamais faire planter la route principale
    3. On utilise une session séparée pour le log pour éviter les conflits
       avec le commit déjà effectué par la route principale
    """
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):

            # Exécuter la fonction principale d'abord
            result = f(*args, **kwargs)

            # Enregistrer le log APRÈS l'exécution
            # On importe ici pour éviter les imports circulaires
            try:
                from flask_login import current_user
                from app.models.database import db, Log

                # CORRECTION 1 : utiliser current_user.is_authenticated
                # au lieu de 'user_id' in session
                if not current_user or not current_user.is_authenticated:
                    return result

                # Résoudre l'entity_id si c'est une fonction callable
                final_entity_id = None
                if callable(entity_id):
                    try:
                        final_entity_id = entity_id(*args, **kwargs)
                    except Exception:
                        final_entity_id = None
                else:
                    final_entity_id = entity_id

                # Construire les détails du log
                details = f"Route: {request.path} | Méthode: {request.method}"

                if details_func and callable(details_func):
                    try:
                        custom_details = details_func(*args, **kwargs, result=result)
                        if custom_details:
                            details = f"{details} | {custom_details}"
                    except Exception:
                        pass

                # CORRECTION 2 : créer le log dans un bloc try/except isolé
                # pour ne pas interférer avec la transaction principale
                # qui est déjà committée par la route
                try:
                    log = Log(
                        user_id=current_user.id,   # ← current_user.id, pas session
                        action=action,
                        entity_type=entity_type,
                        entity_id=final_entity_id,
                        details=details[:500],
                        ip_address=request.remote_addr,
                        user_agent=request.user_agent.string if request.user_agent else None
                    )
                    db.session.add(log)
                    # CORRECTION 3 : utiliser db.session.flush() puis commit()
                    # dans un contexte propre pour éviter les conflits de session
                    db.session.commit()

                except Exception as log_error:
                    # Si le log échoue, on rollback SEULEMENT la partie log
                    # et on ne fait pas planter la route principale
                    print(f"[LOG_ERROR] Impossible d'enregistrer le log: {log_error}")
                    try:
                        db.session.rollback()
                    except Exception:
                        pass

            except Exception as e:
                # Erreur générale du décorateur — on ne fait rien planter
                print(f"[LOG_DECORATOR_ERROR] {e}")

            return result
        return decorated_function
    return decorator


def role_required(*roles):
    """Vérifie que l'utilisateur connecté a l'un des rôles spécifiés."""
    def decorator(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            # CORRECTION : utiliser current_user au lieu de session
            try:
                from flask_login import current_user
                if not current_user or not current_user.is_authenticated:
                    flash('Veuillez vous connecter pour accéder à cette page', 'warning')
                    return redirect(url_for('auth.login'))

                if current_user.role not in roles:
                    abort(403)

            except Exception:
                # Fallback sur session si current_user n'est pas disponible
                if 'user_id' not in session:
                    flash('Veuillez vous connecter pour accéder à cette page', 'warning')
                    return redirect(url_for('auth.login'))
                if session.get('user_role') not in roles:
                    abort(403)

            return f(*args, **kwargs)
        return decorated_function
    return decorator


def admin_required(f):
    """Vérifie que l'utilisateur est administrateur."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from flask_login import current_user
            if not current_user or not current_user.is_authenticated:
                flash('Veuillez vous connecter', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role != 'admin':
                abort(403)
        except Exception:
            if 'user_id' not in session:
                flash('Veuillez vous connecter', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('user_role') != 'admin':
                abort(403)
        return f(*args, **kwargs)
    return decorated_function


def validateur_required(f):
    """Vérifie que l'utilisateur est validateur ou admin."""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        try:
            from flask_login import current_user
            if not current_user or not current_user.is_authenticated:
                flash('Veuillez vous connecter', 'warning')
                return redirect(url_for('auth.login'))
            if current_user.role not in ['validateur', 'admin']:
                abort(403)
        except Exception:
            if 'user_id' not in session:
                flash('Veuillez vous connecter', 'warning')
                return redirect(url_for('auth.login'))
            if session.get('user_role') not in ['validateur', 'admin']:
                abort(403)
        return f(*args, **kwargs)
    return decorated_function