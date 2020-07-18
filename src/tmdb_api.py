import tmdbsimple as tmdb
from pprint import pprint

import shutil
import requests

tmdb.API_KEY = '73f88711a1bbedabc2a94deef288a168'

PROFILE_ROOT_URL = 'https://image.tmdb.org/t/p/original'
PROFILE_ROOT_PATH = 'cast/'

"""
Movies:
3 idiots
the lord of the rings fellowship of the ring
sherlock holmes
forrest gump
1917


I am mother
pacific rim
pirates of the caribbean
"""

def getMovie(movie):
    search = tmdb.Search()
    result = search.movie(query=movie)
    if len(result['results']) <= 0:
        print('did not find movie: ' + movie)
        return []

    id = result['results'][0]['id']
    movie = tmdb.Movies(id)
    res = movie.info()
    return res

def getCast(movie):
    search = tmdb.Search()
    result = search.movie(query=movie)
    if len(result['results']) <= 0:
        print('did not find movie: ' + movie)
        return []
    
    id = result['results'][0]['id']
    movie = tmdb.Movies(id)
    res = movie.info()
    credits = movie.credits()
    cast = credits['cast']
    return cast


def getCastImage(cast):
    profile_path = cast['profile_path']
    name = cast['name']
    
    if profile_path == None:
        print("no image found for: " + name)
        return None
        
    url = PROFILE_ROOT_URL + profile_path
    response = requests.get(url, stream=True)
    return response.raw

def saveCastImage(cast):
    img = getCastImage(cast)
    if img == None:
        return
    with open(PROFILE_ROOT_PATH + cast['name'] + '.png', 'wb') as out_file:
        shutil.copyfileobj(img, out_file)

def getCastInfo(cast):
    search = tmdb.Search()
    name = cast['name']
    result = search.person(query=name)
    if len(result['results']) <= 0:
        print('did not find person: ' + name)
        return []
    
    id = result['results'][0]['id']
    print(id)
    person = tmdb.People(id)
    res = person.info()
    return res

if __name__ == '__main__':
	print(getMovie('1917'))


"""
{'cast_id': 37,
  'character': 'Captain Jack Sparrow',
  'credit_id': '52fe4212c3a36847f80018c3',
  'gender': 2,
  'id': 85,
  'name': 'Johnny Depp',
  'order': 0,
  'profile_path': '/kbWValANhZI8rbWZXximXuMN4UN.jpg'
}
"""

"""
profile path
https://image.tmdb.org/t/p/original/kbWValANhZI8rbWZXximXuMN4UN.jpg

"""

"""
https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=<<api_key>>
https://api.themoviedb.org/3/movie/{movie_id}/credits?api_key=<<api_key>>

https://api.themoviedb.org/3/search/movie?api_key=73f88711a1bbedabc2a94deef288a168&language=en-US&page=1&include_adult=false

https://api.themoviedb.org/3/movie/122917/credits?api_key=73f88711a1bbedabc2a94deef288a168

SEARCH FOR MOVIE NAME:
https://api.themoviedb.org/3/search/movie?api_key=73f88711a1bbedabc2a94deef288a168&query=the+hobbit&language=en-US&page=1&include_adult=false

GET PROFILE FROM PROFILE PATH
https://image.tmdb.org/t/p/original/
"""

"""
GET PERSON INFO
https://api.themoviedb.org/3/person/37?api_key=73f88711a1bbedabc2a94deef288a168&language=en-US
"""