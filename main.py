from flask import Flask
from flask_login import LoginManager

from db.models.users import User
from db.session_factory import init_db, create_session
from web.blueprints.fragment import fragment_bp
from web.blueprints.index import index_bp
from web.blueprints.user import user_bp

app = Flask(__name__)
app.config['SECRET_KEY'] = 'nd21pr'
app.config['WTF_CSRF_SECRET_KEY'] = "secret key for forms"

login_manager = LoginManager()
login_manager.init_app(app)


@login_manager.user_loader
def load_user(user_id):
    session = create_session()
    return session.get(User, user_id)


init_db('db/db.sqlite3')
app.register_blueprint(index_bp)
app.register_blueprint(user_bp)
app.register_blueprint(fragment_bp)
app.run()


if __name__ == '__main__':
    app.run()
