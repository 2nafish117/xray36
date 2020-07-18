import tmdb_api
from pprint import pprint
import os
import cv2
import scenedetect
from scenedetect.video_manager import VideoManager
from scenedetect.scene_manager import SceneManager
from scenedetect.frame_timecode import FrameTimecode
from scenedetect.stats_manager import StatsManager
from scenedetect.detectors import ContentDetector
from database import Database
import shutil
import face_recognition

	# stage1:
	# get movie name (from user) and video file
	# get cast and movie info
	# open video file
	# segment into shot
	# store in db
	# stage2:
	# find actors in each shot
	# store actors in each shot to db

want_face_rec = True
db = Database()
movie_name = '1917'
video_path = "videos/1917_1.mkv"

def main():
	movie_info = tmdb_api.getMovie(movie_name)
	cast = tmdb_api.getCast(movie_name)
	# pprint(movie_info)
	# pprint(cast[0])
	# pprint(tmdb_api.getCastInfo(cast[0]))
	# for c in cast:
	# 	img = tmdb_api.getCastImage(c)
	# 	info = tmdb_api.getCastInfo(c)
	# 	pprint(info)

	# adding actors into db
	print('getting cast...')
	for actor in cast:
		actor_data = {
			'name': actor['name'],
			'gender': actor['gender'],
			'profile_path': actor['profile_path'],
			# 'image': tmdb_api.getCastImage(actor),
			# 'biography': tmdb_api.getCastInfo(actor)['biography'],
			'biography': ''
		}
		db.actors_insertone_unique(actor_data)
		db.actors_createindex()

	if db.movies_findone({
			'movie_name': movie_info['original_title'],
			'video_path': video_path,
		}).count() <= 0:
		print('processing video to shots...')
		video_manager = VideoManager([video_path])
		stats_manager = StatsManager()
		scene_manager = SceneManager(stats_manager)
		scene_manager.add_detector(ContentDetector(threshold=20.0))
		base_timecode = video_manager.get_base_timecode()

		video_manager.set_downscale_factor(2)
		video_manager.start()
		scene_manager.detect_scenes(frame_source=video_manager, show_progress=True)
		shot_list = scene_manager.get_scene_list(base_timecode)

		# adding shots into db
		print('adding shots to db...')
		shot_data = {
			'movie_name': movie_info['original_title'],
			'video_path': video_path,
			'framerate': video_manager.get_framerate(),
			'encoding': video_path.split('.')[-1]
		}

		shot_list_data = []
		for shot in shot_list:
			shot_list_data.append({
					'start_frame' : shot[0].get_frames(),
					'end_frame' : shot[1].get_frames(),
					'start_time' : shot[0].get_seconds(),
					'end_time' : shot[1].get_seconds(),
					'start_timestamp' : shot[0].get_timecode(),
					'end_timestamp' : shot[1].get_timecode(),
					'actors_in_shot' : []
				}
			)
		
		shot_data['shot_list'] = shot_list_data
		shots_data_id = db.shots_insertone_unique(shot_data).inserted_id
		# adding movies into db
		print('adding movie to db...')
		movie_data = {
			'movie_name': movie_info['original_title'],
			'video_path': video_path,
			'overview': movie_info['overview'],
			'genres': [genre['name'] for genre in movie_info['genres']],
			'poster_path': movie_info['poster_path'],
			'shots_data': shots_data_id
		}
		db.movies_insertone_unique(movie_data)
		db.movies_createindex()

		if want_face_rec:
			print('starting face recog and identification...')
			# do face recog
			# get movie and video file name, get actor id and profile_path from db
			# get all images of all actors needed from tmdb
			# load images of actors into face recog
			# load video file
			# for each frame
			# 	get faces recognised there
			# 	find out which shot it belongs to
			# 	insert the ids of the same actors into the shots collection array
			known_faces_names = []
			known_faces_encodings = []
			for actor in cast:
				name = actor['name']
				path = './cast/' + name + '.png'

				if os.path.exists(path):
					print('found ' + path)
					img = face_recognition.load_image_file(path)
					print('encoding ' + name)
					encodings = face_recognition.face_encodings(img)
					if len(encodings) > 0:
						known_faces_encodings.append(encodings[0])
						known_faces_names.append(name)
					else:
						print('failed encoding ' + name)
				else:
					tmdb_api.saveCastImage(actor)
					print('getting actor image from tmdb ' + path)
					if os.path.exists(path):
						img = face_recognition.load_image_file(path)
						print('encoding ' + name)
						encodings = face_recognition.face_encodings(img)
						if len(encodings) > 0:
							known_faces_encodings.append(encodings[0])
							known_faces_names.append(name)
						else:
							print('failed encoding ' + name)

			# load vid file and face recog
			input_movie = cv2.VideoCapture(video_path)
			input_fps = input_movie.get(cv2.CAP_PROP_FPS)
			input_width  = int(input_movie.get(cv2.CAP_PROP_FRAME_WIDTH))
			input_height = int(input_movie.get(cv2.CAP_PROP_FRAME_HEIGHT))
			output_resolution = (int(input_width / 2.0),int(input_height / 2.0))
			length = int(input_movie.get(cv2.CAP_PROP_FRAME_COUNT))

			# Create an output movie file (make sure resolution/frame rate matches input video!)
			fourcc = cv2.VideoWriter_fourcc(*'XVID')
			output_movie = cv2.VideoWriter('videos/outputs/output_' + video_path.split('/')[-1] + '.avi', fourcc, input_fps, output_resolution)
						
			frame_number = 0
			while True:
				# Grab a single frame of video
				ret, frame = input_movie.read()
				frame_number += 1
				# Quit when the input video file ends
				if not ret:
					break
				print('frame ' + str(frame_number) + '/' + str(length))

				frame = cv2.resize(frame,output_resolution,fx=0,fy=0, interpolation=cv2.INTER_CUBIC)
				# Convert the image from BGR color (which OpenCV uses) to RGB color (which face_recognition uses)
				rgb_frame = frame[:, :, ::-1]

				# Find all the faces and face encodings in the current frame of video
				face_locations = face_recognition.face_locations(rgb_frame)
				face_encodings = face_recognition.face_encodings(rgb_frame, face_locations)
				for face_encoding in face_encodings:
					# See if the face is a match for the known face(s)
					match = face_recognition.compare_faces(known_faces_encodings, face_encoding, tolerance=0.50)
					for i in range(len(match)):
						if match[i]:
							known_name = known_faces_names[i]
							print('found ' + known_name)
							actor_id = db.actors_findone({'name': known_name})[0]['_id']

							###### draw rectanglesin frame ######
							print('locations: ', face_locations)
							for location in face_locations:
								(top, right, bottom, left) = location
								cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)
								# Draw a label with a name below the face
								cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
								font = cv2.FONT_HERSHEY_DUPLEX
								cv2.putText(frame, known_name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)
							###########

							# find out which shot it belongs to
							# insert into that one
							for j in range(len(shot_list_data)):
								if frame_number >= shot_list_data[j]['start_frame'] and frame_number < shot_list_data[j]['end_frame']:
									if actor_id not in shot_list_data[j]['actors_in_shot']:
										shot_list_data[j]['actors_in_shot'].append(actor_id)
				output_movie.write(frame)


			print('updating shots db with actor list...')
			shot_data['shot_list'] = shot_list_data
			db.shots_updateone(shots_data_id, shot_data)
			pass
		print('DONE FACEREC!!')
	else:
		print('movie already in database !!')
		return
	


if __name__ == "__main__":
	main()

"""
SHEMEA ??? 

movie : {
	_id,
	original_title => movie_name,
	video_name,
	overview => description,
	genres => tags
	poster_path => poster_path
	shots_data: _id
}

shots: {
	_id,
	movie_name,
	frame_rate,
	encoding,
	shots_list : [
		{
			actors_in_shot: [ids],
			start_frame: ,
			end_frame ,
			start_time: ,
			end_time: ,
		},
		{
			actors_in_shot: [ids],
			start_frame: ,
			end_frame ,
			start_time: ,
			end_time: ,
			start_timestamp: ,
			end_timestamp: ,
		}
	]
}

actors: {
	_id: ,
	name: ,
	gender: ,
	profile_path: ,
	biography: ,

	5edcacd309b3425e55f9e788
	5edcacd409b3425e55f9e7c9
	5edcacd309b3425e55f9e78c
	5edcacd309b3425e55f9e7b1
}
"""