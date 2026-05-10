# =============================================================================
#  app/routes/__init__.py
#  Point d'entrée du blueprint "api" — regroupe toutes les routes
# =============================================================================
from flask import Blueprint, jsonify, request, render_template, \
                  send_file, flash, redirect, url_for, current_app
from flask_login import login_required, current_user
from functools import wraps
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash
from sqlalchemy import text
from datetime import datetime
import os

from app.models.database import (
    db, GroupeThematique, KPI, User, Log, RoleEnum,
    Validation, CommentaireAnnuel, KPISAnnuel
)
from app.decorators import log_action, admin_required
from app.kpi_mapping import (
    KPI_META, get_kpis_pour_collecteur,
    get_direction_du_kpi, DIRECTION_LABELS
)

# ── Blueprint ──────────────────────────────────────────────────────────────────
bp = Blueprint('api', __name__)

# ── Constantes ─────────────────────────────────────────────────────────────────
VALID_KPI_CODES = (
    {f'gt1pki{j:02d}' for j in range(1, 16)} |
    {f'gt2pki{j:02d}' for j in [1,2,4,5,6,7,8,9,10]} |
    {f'gt3pki{j:02d}' for j in range(1, 22)}
)
RECAP_VALIDATION_STATUSES = {'en_attente', 'valide', 'relance', 'annule'}

UPLOAD_FOLDER     = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', '..', 'uploads')
ALLOWED_EXTENSIONS = {'pdf','doc','docx','xls','xlsx','ppt','pptx',
                      'jpg','jpeg','png','gif','mp4','zip','csv','txt'}
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


# ── Routes de base ─────────────────────────────────────────────────────────────
@bp.route('/')
def dashboard():
    return render_template('dashboard.html')


# ── API groupes ─────────────────────────────────────────────────────────────────
@bp.route('/api/groupes')
def get_groupes():
    groupes = GroupeThematique.query.all()
    return jsonify([g.to_dict() for g in groupes])


# ── API KPIs ────────────────────────────────────────────────────────────────────
@bp.route('/api/kpis')
def get_kpis():
    groupe_id = request.args.get('groupe_id')
    query = KPI.query
    if groupe_id:
        query = query.filter_by(groupe_id=groupe_id)
    return jsonify([k.to_dict() for k in query.all()])


@bp.route('/api/kpis/global')
def get_kpis_global():
    kpis = KPI.query.all()
    if not kpis:
        return jsonify({'total_kpis': 0, 'taux_global': 0,
                        'kpis_atteints': 0, 'kpis_critiques': 0})
    taux_moyen = sum(k.to_dict()['taux_atteinte'] for k in kpis) / len(kpis)
    return jsonify({
        'total_kpis':     len(kpis),
        'kpis_atteints':  sum(1 for k in kpis if k.to_dict()['taux_atteinte'] >= 100),
        'kpis_critiques': sum(1 for k in kpis if k.to_dict()['taux_atteinte'] < 40),
        'taux_global':    round(taux_moyen, 1)
    })


# ── Importation du reste des routes ────────────────────────────────────────────
# api.py contient toutes les routes détaillées (KPI, admin, collecteur, etc.)
# Il est importé par app/__init__.py via :  from app.routes.api import bp as api_bp