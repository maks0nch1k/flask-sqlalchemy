import flask
from flask import jsonify, request
from . import db_session
from .jobs import Jobs


blueprint = flask.Blueprint(
    'jobs_api',
    __name__,
    template_folder='templates'
)


@blueprint.route('/api/jobs/<int:jobs_id>', methods=['DELETE'])
def delete_jobs(jobs_id):
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).get(jobs_id)
    if not jobs:
        return jsonify({'error': 'Not found'})
    db_sess.delete(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs', methods=['POST'])
def create_jobs():
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in request.json for key in
                 ["team_leader", "job", "work_size", "collaborators", "is_finished"]):
        return jsonify({'error': 'Bad request'})

    db_sess = db_session.create_session()
    if request.json["id"] in [elem.id for elem in db_sess.query(Jobs).all()]:
        return jsonify({"error": "Id already exists"})

    jobs = Jobs(
        team_leader=request.json['team_leader'],
        job=request.json['job'],
        work_size=request.json['work_size'],
        collaborators=request.json['collaborators'],
        is_finished=request.json['is_finished']
    )
    db_sess.add(jobs)
    db_sess.commit()
    return jsonify({'success': 'OK'})


@blueprint.route('/api/jobs')
def get_jobs():
    db_sess = db_session.create_session()
    jobs = db_sess.query(Jobs).all()
    return jsonify(
        {
            'jobs':
                [item.to_dict(only=["id", "team_leader", "job", "work_size",
                                    "collaborators", "start_date", "end_date", "is_finished"])
                 for item in jobs]
        }
    )


@blueprint.route('/api/jobs/<int:job_id>')
def get_current_job(job_id):
    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).get(job_id)
    if not job:
        return jsonify({"error": "Not found"})
    return jsonify(
        {
            'jobs':
                job.to_dict(only=("id", "team_leader", "job", "work_size",
                                  "collaborators", "start_date", "end_date", "is_finished"))
        }
    )


@blueprint.route('/api/edit_jobs/<int:job_id>', methods=['POST'])
def edit_jobs(job_id):
    if not request.json:
        return jsonify({'error': 'Empty request'})
    elif not all(key in ["id", "team_leader", "job", "work_size", "collaborators", "is_finished"]
                 for key in request.json):

        return jsonify({'error': 'Bad request'})
    if "id" in request.json:
        return jsonify({"error": "You cannot edit id of the job"})

    db_sess = db_session.create_session()
    job = db_sess.query(Jobs).filter(Jobs.id == job_id).first()

    if not job:
        return jsonify({"error": "job not found"})

    if "team_leader" in request.json:
        job.team_leader = request.json["team_leader"]
    if "job" in request.json:
        job.job = request.json["job"]
    if "work_size" in request.json:
        job.work_size = request.json["work_size"]
    if "collaborators" in request.json:
        job.collaborators = request.json["collaborators"]
    if "is_finished" in request.json:
        job.is_finished = request.json["is_finished"]

    db_sess.commit()

    return jsonify({'success': 'OK'})