import uuid

from flask import Blueprint, redirect, render_template, make_response, request
from flask_login import current_user, login_required

from db.models.fragments import Fragment
from db.session_factory import create_session
from web.data.add_fragment_form import AddFragmentForm

fragment_bp = Blueprint('fragment', __name__)


@fragment_bp.route('/add_fragment', methods=['POST', 'GET'])
@login_required
def add_fragment():
    form = AddFragmentForm()
    if form.validate_on_submit():
        session = create_session()
        fragment = Fragment(
            id=str(uuid.uuid4()),  # SQLite не поддерживает UUID нативно
            user_id=current_user.id,
            filename=form.filename.data,
            content=form.content.data
        )
        session.add(fragment)
        session.commit()
        session.close()
        return redirect(f'/fragments/{fragment.id}')
    return render_template('add_fragment.html', form=form)


@fragment_bp.route('/fragments/<fragment_id>', methods=['GET'])
def get_fragment(fragment_id):
    session = create_session()
    fragment = session.get(Fragment, fragment_id)
    session.close()
    if fragment:
        return render_template('fragment.html', fragment=fragment)
    return make_response({'error': 'No fragments found'}, 404)


@fragment_bp.route('/edit_fragment/<fragment_id>', methods=['POST', 'GET'])
@login_required
def edit_fragment(fragment_id):
    session = create_session()
    fragment = session.get(Fragment, fragment_id)
    form = AddFragmentForm()
    if fragment:
        if form.validate_on_submit():
            fragment.filename = form.filename.data
            fragment.content = form.content.data
            session.commit()
            session.close()
            return redirect(f'/fragments/{fragment_id}')
        if request.method == 'GET':
            form.filename.data = fragment.filename  # Чтобы при старте редактирования сразу же отображался текст фрагмента
            form.content.data = fragment.content
    session.close()
    return render_template('edit_fragment.html', form=form)


@fragment_bp.route('/delete_fragment/<fragment_id>')
@login_required
def delete_fragment(fragment_id):
    session = create_session()
    fragment = session.get(Fragment, fragment_id)
    if fragment and fragment.user_id == current_user.id:
        session.delete(fragment)
        session.commit()
        session.close()
        return redirect('/')
    session.close()
    return make_response({'error': 'No fragments found'}, 404)
