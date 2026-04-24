from flask import Blueprint, render_template, redirect
from flask_login import current_user

from db.models.fragments import Fragment
from db.session_factory import create_session

index_bp = Blueprint('index', __name__)


@index_bp.route('/')
def index():
    session = create_session()
    if current_user.is_authenticated:
        fragments = session.query(Fragment).filter(Fragment.user_id == current_user.id).all()
    else:
        fragments = []
    session.close()
    return render_template('index.html', fragments=fragments)
