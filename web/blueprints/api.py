from flask import Blueprint
from flask_restful import Api, Resource
import uuid
from db.models.fragments import Fragment
from db.session_factory import create_session

api_bp = Blueprint('api', __name__, url_prefix='/api')
api = Api(api_bp)


class FragmentListAPI(Resource):
    def get(self):
        session = create_session()
        fragments = session.query(Fragment).all()
        session.close()
        return [{'id': f.id, 'filename': f.filename, 'content': f.content, 'user_id': f.user_id} for f in fragments]

    def post(self):
        from flask import request
        data = request.json
        session = create_session()
        fragment = Fragment(
            id=str(uuid.uuid4()),
            filename=data.get('filename'),
            content=data.get('content'),
            user_id=data.get('user_id')
        )
        session.add(fragment)
        session.commit()
        fragment_id = fragment.id
        session.close()
        return {'id': fragment.id}, 201


class FragmentDetailAPI(Resource):
    def get(self, fragment_id):
        session = create_session()
        fragment = session.get(Fragment, fragment_id)
        session.close()
        if fragment:
            return {'id': fragment.id, 'filename': fragment.filename, 'content': fragment.content}
        return {'error': 'Not found'}, 404

    def put(self, fragment_id):
        from flask import request
        data = request.json
        session = create_session()
        fragment = session.get(Fragment, fragment_id)
        if fragment:
            fragment.filename = data.get('filename', fragment.filename)
            fragment.content = data.get('content', fragment.content)
            session.commit()
            session.close()
            return {'message': 'Updated'}
        return {'error': 'Not found'}, 404

    def delete(self, fragment_id):
        session = create_session()
        fragment = session.get(Fragment, fragment_id)
        if fragment:
            session.delete(fragment)
            session.commit()
            session.close()
            return {'message': 'Deleted'}, 200
        return {'error': 'Not found'}, 404


api.add_resource(FragmentListAPI, '/fragments')
api.add_resource(FragmentDetailAPI, '/fragments/<string:fragment_id>')
