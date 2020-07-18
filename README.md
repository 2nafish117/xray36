# xray36

System that preprocesses a movie and generates metadata describing the actors in each shot.
Frontend pulls the cached/preprocessed data from mongodb and serves it like a streaming service. 

input video files goes in `videos/`
the cast profile images are downloaded to `cast/`
shots and movie metadata is added to mongodb collections

## Requirements

1. Python3.6
2. Dlib for python (with cuda preferably)
3. mongodb and pymongo
4. opencv
5. pyscenedetect
  
