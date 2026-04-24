from flask import Blueprint, redirect, render_template
from flask_login import login_user, login_required, current_user, logout_user

from db.models.users import User
from db.session_factory import create_session
from web.data.login_form import LoginForm
from web.data.register_form import RegisterForm

user_bp = Blueprint('user', __name__)


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        session = create_session()
        user = session.query(User).filter_by(email=form.email.data).first()
        if user and user.check_hashed_password(form.password.data):
            login_user(user, remember=form.remember_me.data)
            return redirect('/')
        return render_template('login.html', message='Wrong email or password', form=form)
    return render_template('login.html', form=form)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        session = create_session()
        user = User(
            email=form.email.data,
            username=form.username.data,
        )
        user.set_hashed_password(form.password.data)
        session.add(user)
        session.commit()
        return redirect('/login')
    return render_template('register.html', message='All fields must be filled', form=form)


@user_bp.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect('/')
