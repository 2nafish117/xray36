import bcrypt, sys
import pymongo
from pymongo import MongoClient
from pymongo import errors
import gridfs

class Database(object):
	def __init__(self):
		try:
			self.client = MongoClient()

			self.movies = self.client.xray.movies
			self.shots = self.client.xray.shots
			self.actors = self.client.xray.actors
			self.fs = gridfs.GridFS(self.client.xray)
		except errors.ServerSelectionTimeoutError as err:
			print(err)

	def __del__(self):
		self.client.close()

	def reset(self):
		self.movies.drop()
		self.actors.drop()
		self.shots.drop()

	# movies 

	def movies_find(self, query):
		return self.movies.find(query)
	
	def movies_findone(self, query):
		return self.movies.find(query)

	def movies_findall(self):
		return self.movies.find({})
	
	def movies_insertone(self, movie):
		return self.movies.insert_one(movie)
	
	def movies_insertone_unique(self, movie):
		if self.movies_findone({
			'movie_name': movie['movie_name'],
			'video_path': movie['video_path'],
		}).count() > 0:
			print('movie with name ' + movie['movie_name'] + ' already exists, not inserting')
			return
		return self.movies.insert_one(movie)

	def movies_createindex(self):
		return self.movies.create_index([
			('movie_name', pymongo.TEXT),
			('overview', pymongo.TEXT),
			('genres', pymongo.TEXT),
		])
	
	# shots

	def shots_find(self, query):
		return self.shots.find(query)

	def shots_findone(self, query):
		return self.shots.find(query)
	
	def shots_findall(self):
		return self.shots.find({})

	def shots_insertone(self, shot):
		return self.shots.insert_one(shot)
	
	def shots_updateone(self, shot_id, update):
		return self.shots.replace_one({'_id': shot_id}, update)
	
	def shots_insertone_unique(self, shot):
		if self.shots_findone({
			'movie_name': shot['movie_name'],
			'video_path': shot['video_path'],
		}).count() > 0:
			print('shot of ' + shot['movie_name'] + ' already exists, not inserting')
			return
		return self.shots.insert_one(shot)

	# actor

	def actors_find(self, query):
		return self.actors.find(query)

	def actors_findone(self, query):
		return self.actors.find(query)
	
	def actors_findall(self):
		return self.actors.find({})

	def actors_insertone(self, actor):
		return self.actors.insert_one(actor)
	
	def actors_insertone_unique(self, actor):
		if self.actors_findone(actor).count() > 0:
			print('actor with name ' + actor['name'] + ' already exists, not inserting')
			return
		return self.actors.insert_one(actor)

	def actors_createindex(self):
		return self.actors.create_index([
			('name', pymongo.TEXT),
			('biography', pymongo.TEXT),
		])

# class DatabaseHelper(object):
#     def __init__(self):
#         try:
#             self.client = MongoClient()
#             self.db = self.client.xray
#             self.sherlock = self.db.sherlock
#             self.lotr = self.db.lotr_bilbo_gandalf
#         except errors.ServerSelectionTimeoutError as err:
#             print(err)

#     def retrieve_sherlock(self):
#         return self.sherlock.find({})

#     def retrieve_lotr(self):
#         return self.lotr.find({})

	# def retrieve_tasks(self):
	#     return self.tasks.find({}, {'_id': 0})

	# def retrieve_task_with_title(self, title):
	#     return self.tasks.find_one({'title': title}, {'_id': 0})

	# def retrieve_task_with_id(self, id_):
	#     return self.tasks.find_one({'id': id_}, {'_id': 0})

	# def find_and_update_task(self, task):
	#     id_ = task['id']
	#     tasks = self.retrieve_tasks()
	#     try:
	#         task_to_change = next(task for task in tasks if task['id'] == id_)
	#         self._update_task(id_, task, task_to_change)
	#     except:
	#         raise ValueError("Task was not updated")

	# def _update_task(self, id_, task, task_to_change):
	#     for key, value in task_to_change.items():
	#         for k, new_value in task.items():
	#             if key == k and value != new_value:
	#                 self.tasks.update({'id': id_}, {'$set': {key: new_value}})

	# def remove_task(self, task):
	#     id_ = task['id']
	#     task_to_remove = self.retrieve_task_with_id(id_)
	#     if task_to_remove == task:
	#         self.tasks.remove({'id': id_})
	#     else:
	#         raise ValueError("Task was not found!")

	# def retrieve_users(self):
	#     return self.users.find({}, {'_id': 0})

	# def retrieve_user_by_username(self, username):
	#     return self.users.find_one({'username': username}, {'_id': 0})


# class TestDB(DatabaseHelper):
#     def __init__(self):
#         try:
#             self.client = MongoClient()
#             self.db = self.client.test
#             self.tasks = self.db.tasks
#             self.users = self.db.users
#         except errors.ServerSelectionTimeoutError as err:
#             print(err)

#     def create_test_users_to_test_db(self):
#         self.create_non_existing_user_to_database('mojo', 'python')
#         self.create_non_existing_user_to_database('kojo', 'python')

#     def remove_test_users_from_db(self):
#         self.users.remove({})


# if __name__ == "__main__":
#     database = DatabaseHelper()
#     sher = database.retrieve_sherlock()
#     print(sher)