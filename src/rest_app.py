#!flask/bin/python
import six
import sys
from flask import Flask, jsonify, abort, request, make_response, url_for
# from flask_httpauth import HTTPBasicAuth
from database import DatabaseHelper
from bson.json_util import dumps
from flask_cors import CORS, cross_origin

import json
from bson import ObjectId

# class JSONEncoder(json.JSONEncoder):
#     def default(self, o):
#         if isinstance(o, ObjectId):
#             return str(o)
#         return json.JSONEncoder.default(self, o)


def make_shot_data(shot_data):
    new_task = {}
    for field in shot_data:
        if field == '_id':
            # new_task['uri'] = url_for('get_task', task_id=task['id'],
            #                           _external=True)
            pass
        else:
            new_task[field] = shot_data[field]
    return new_task

app = Flask(__name__, static_url_path="")
# auth = HTTPBasicAuth()
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

db = DatabaseHelper()

@app.route('/xray/sherlock', methods=['GET'])
@cross_origin()
def get_sherlock():
    sherlock_shots = db.retrieve_sherlock()
    return jsonify({'shots': [make_shot_data(doc) for doc in sherlock_shots]})

@app.route('/xray/lotr', methods=['GET'])
@cross_origin()
def get_lotr():
    lotr_shots = db.retrieve_lotr()
    return jsonify({'shots': [make_shot_data(doc) for doc in lotr_shots]})

if __name__ == '__main__':
    app.run(debug=True)




# @auth.verify_password
# def verify_password(username, password):
#     return db.check_password_hash_for_user(username, password)


# @auth.error_handler
# def unauthorized():
#     # return 403 instead of 401 to prevent browsers from displaying the default
#     # auth dialog
#     return make_response(jsonify({'error': 'Unauthorized access'}), 403)


# @app.errorhandler(400)
# def bad_request(error):
#     return make_response(jsonify({'error': 'Bad request'}), 400)


# @app.errorhandler(404)
# def not_found(error):
#     return make_response(jsonify({'error': 'Not found'}), 404)


# def make_public_task(task):
#     new_task = {}
#     for field in task:
#         if field == 'id':
#             new_task['uri'] = url_for('get_task', task_id=task['id'],
#                                       _external=True)
#         else:
#             new_task[field] = task[field]
#     return new_task


# @app.route('/todo/api/v1.0/tasks', methods=['GET'])
# @auth.login_required
# def get_tasks():
#     tasks = db.retrieve_tasks()
#     return jsonify({'tasks': [make_public_task(task) for task in tasks]})


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['GET'])
# @auth.login_required
# def get_task(task_id):
#     tasks = db.retrieve_tasks()
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     return jsonify({'task': make_public_task(task[0])})


# @app.route('/todo/api/v1.0/tasks', methods=['POST'])
# @auth.login_required
# def create_task():
#     tasks_list = []
#     tasks = db.retrieve_tasks()
#     for task in tasks:
#         tasks_list.append(task)
#     if not request.json or 'title' not in request.json:
#         abort(400)
#     task = {
#         'id': tasks_list[-1]['id'] + 1,
#         'title': request.json['title'],
#         'description': request.json.get('description', ""),
#         'done': False
#     }
#     db.add_task_to_db(task)
#     task = db.retrieve_task_with_title(request.json['title'])
#     return jsonify({'task': make_public_task(task)}), 201


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['PUT'])
# @auth.login_required
# def update_task(task_id):
#     tasks = db.retrieve_tasks()
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     if not request.json:
#         abort(400)
#     if 'title' in request.json and \
#             not isinstance(request.json['title'], six.string_types):
#         abort(400)
#     if 'description' in request.json and \
#             not isinstance(request.json['description'], six.string_types):
#         abort(400)
#     if 'done' in request.json and type(request.json['done']) is not bool:
#         abort(400)
#     task[0]['title'] = request.json.get('title', task[0]['title'])
#     task[0]['description'] = request.json.get('description',
#                                               task[0]['description'])
#     task[0]['done'] = request.json.get('done', task[0]['done'])
#     db.find_and_update_task(task[0])
#     return jsonify({'task': make_public_task(task[0])})


# @app.route('/todo/api/v1.0/tasks/<int:task_id>', methods=['DELETE'])
# @auth.login_required
# def delete_task(task_id):
#     tasks = db.retrieve_tasks()
#     task = [task for task in tasks if task['id'] == task_id]
#     if len(task) == 0:
#         abort(404)
#     db.remove_task(task[0])
#     return jsonify({'result': True})


