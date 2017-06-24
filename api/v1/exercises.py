from flask import request
from ..models import db, Exercise
from ..decorators import json, collection, etag
from . import api


@api.route('/exercises/', methods=['GET'])
@etag
@json
@collection(Exercise)
def get_exercises():
    return Exercise.query


@api.route('/exercises/<int:id>', methods=['GET'])
@etag
@json
def get_exercise(id):
    return Exercise.query.get_or_404(id)


@api.route('/exercises/', methods=['POST'])
@json
def new_exercise():
    exercise_ = Exercise().import_data(request.get_json(force=True))
    db.session.add(exercise_)
    db.session.commit()
    return {}, 201, {'Location': exercise_.get_url()}


@api.route('/exercises/<int:id>', methods=['DELETE'])
@json
def delete_exercise(id):
    exercise_ = Exercise.query.get_or_404(id)
    db.session.delete(exercise_)
    db.session.commit()
    return {}
