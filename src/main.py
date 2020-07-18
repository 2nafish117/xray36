from flask import Flask, jsonify, request, render_template, abort, make_response, url_for, redirect, Response
from flask_pymongo import PyMongo
from bson.json_util import dumps
from bson import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash
from flask_cors import CORS, cross_origin
from database import Database
import os

# import sys
# import json
# from flask.json import JSONEncoder
# from bson import json_util

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
db = Database()

@app.route('/xray/search/<string:resource>', methods=['GET'])
@cross_origin(origin='*')
def get_search(resource):
	query = request.args.get('query')
	if resource == "movies":
		return dumps(db.movies.find({'$text': {'$search': query}}))
	if resource == "actors":
		return dumps(db.actors.find({'$text': {'$search': query}}))

@app.route('/xray/movies/<string:id>', methods=['GET'])
@cross_origin(origin='*')
def get_movie(id):
	if id == "all":
		mov = db.movies_findall()
		return dumps(mov)

	mov = db.movies_findone({'_id': ObjectId(id)})
	return dumps(mov)

@app.route('/xray/shots/<string:movie_id>', methods=['GET'])
@cross_origin(origin='*')
def get_shots(movie_id):
	if movie_id == "all":
		shot = db.shots_findall()
		return dumps(shot)

	mov = db.movies.find_one({'_id': ObjectId(movie_id)})
	shots = db.shots.find_one({'_id': mov['shots_data']})
	return dumps(shots)

@app.route('/xray/actors/<string:id>', methods=['GET'])
@cross_origin(origin='*')
def get_actor(id):
	if id == "all":
		actors = db.actors_findall()
		return dumps(actors)

	actor = db.actors.find_one({'_id': ObjectId(id)})
	return dumps(actor)

@app.route('/xray/browse/')
@cross_origin(origin='*')
def browse():
	return render_template('index.html')

@app.route('/xray/watch/<string:id>')
@cross_origin(origin='*')
def watch(id):
	return render_template('watch.html', id=id)

if __name__ == '__main__':
	app.run(debug=True)