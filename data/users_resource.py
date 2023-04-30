from . import db_session
from .users import User
from flask_restful import abort, Resource
from flask import jsonify
from users_resource_parser import parser


def abort_if_users_not_found(user_id):
    session = db_session.create_session()
    user = session.query(User).get(User)
    if not user:
        abort(404, message=f"News {user_id} not found")


class UsersResource(Resource):
    def get(self, user_id):
        abort_if_users_not_found(User)
        session = db_session.create_session()
        news = session.query(User).get(user_id)
        return jsonify({'user': news.to_dict(
            only=('name', 'surname', 'age', 'position',
                  'speciality', 'address', 'email', 'city_from'))})

    def delete(self, user_id):
        abort_if_users_not_found(user_id)
        session = db_session.create_session()
        user = session.query(User).get(user_id)
        session.delete(user)
        session.commit()
        return jsonify({'success': 'OK'})


class UsersListResource(Resource):
    def get(self):
        session = db_session.create_session()
        users = session.query(User).all()
        return jsonify({'users': [item.to_dict(
            only=('name', 'surname', 'age', 'position',
                  'speciality', 'address', 'email', 'city_from')) for item in users]})

    def post(self):
        args = parser.parse_args()
        session = db_session.create_session()
        user = User(
            surname=args['surname'],
            name=args['name'],
            age=args['age'],
            position=args['position'],
            speciality=args['speciality'],
            address=args['address'],
            email=args['email'],
            hashed_password=args['hashed_password'],
            city_from=args['city_from']
        )
        session.add(user)
        session.commit()
        return jsonify({'success': 'OK'})