import flask
from flask import jsonify, request
from . import db_session
from .users import User


blueprint = flask.Blueprint(
    'user_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/users')
def get_all_users():
    db_sess = db_session.create_session()
    users = db_sess.query(User).all()
    return jsonify(
        {
            'users':
                [item.to_dict(only=["id", "surname", "name", "age",
                                    "position", "speciality", "address", "email"])
                 for item in users]
        }
    )


@blueprint.route('/api/users/<int:user_id>')
def get_current_user(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({"error": "User not found"})
    return jsonify(
        {
            'user':
                user.to_dict(only=["id", "surname", "name", "age",
                                   "position", "speciality", "address", "email"])
        }
    )


@blueprint.route('/api/users', methods=['POST'])
def create_user():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["surname", "name", "age", "position", "speciality", "address", "hashed_password", "email"]):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()

    user = User(
        surname=request.json['surname'],
        name=request.json['name'],
        age=request.json['age'],
        position=request.json['position'],
        speciality=request.json['speciality'],
        address=request.json['address'],
        hashed_password=request.json["hashed_password"],
        email=request.json['email']
    )
    db_sess.add(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/edit_users/<int:user_id>', methods=['POST'])
def edit_user(user_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in ["id", "surname", "name", "age", "position",
                         "speciality", "address", "hashed_password", "email"]
                 for key in request.json):
        return jsonify({'error': 'Bad request'})

    if "id" in request.json:
        return jsonify({"error": "You cannot edit id of the job"})

    db_sess = db_session.create_session()
    user = db_sess.query(User).filter(User.id == user_id).first()

    if not user:
        return jsonify({"error": "job not found"})

    if "surname" in request.json:
        user.surname = request.json["surname"]
    if "name" in request.json:
        user.name = request.json["name"]
    if "age" in request.json:
        user.age = request.json["age"]
    if "position" in request.json:
        user.position = request.json["position"]
    if "speciality" in request.json:
        user.speciality = request.json["speciality"]
    if "address" in request.json:
        user.address = request.json["address"]
    if "email" in request.json:
        user.email = request.json["email"]
    if "hashed_password" in request.json:
        user.hashed_password = request.json["hashed_password"]

    db_sess.commit()

    return jsonify({'success': 'OK'})


@blueprint.route('/api/users/<int:user_id>', methods=['DELETE'])
def delete_jobs(user_id):
    db_sess = db_session.create_session()
    user = db_sess.query(User).get(user_id)
    if not user:
        return jsonify({'error': 'Not found'})
    db_sess.delete(user)
    db_sess.commit()
    return jsonify({'success': 'OK'})