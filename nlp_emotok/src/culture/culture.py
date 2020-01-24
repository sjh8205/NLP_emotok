#노래에 관련된 QA
from ..sia import relation_query
from . import culture_rnn
import random

def get_data(input_json):

	_json = dict()
	_json['entity'] = None
	_json['relation'] = None

	for morph in input_json['input_list']:
		if morph[0] == '노래':
			_json['relation'] = 'has_song_info'
			_json['entity'] = get_music_time(input_json)
		elif morph[0] == '음악':
			_json['relation'] = 'has_music_info'
			_json['entity'] = get_music_time(input_json)
		elif morph[0] == '드라마':
			_json['relation'] = 'has_drama_info'
			_json['entity'] = '드라마'
		elif morph[0] == '영화':
			_json['relation'] = 'has_movie_info'
			_json['entity'] = '영화'
		elif morph[0] == '아이돌':
			_json['relation'] = 'has_idol_era'
			_json['entity'] = get_idol_time(input_json)

	if _json['entity'] == None:
		response = culture_rnn.get_response(input_json['query'])
		_json['hint'] = response
		_json['model'] = "EMOTOK"
		return _json
	else:
		_json['server'] = input_json['server']	
		sia_json = relation_query.get_sia_data(_json)
		sia_json['model'] = "SIA"

		if sia_json['hint'] == 0:
			response = culture_rnn.get_response(input_json['query'])
			sia_json['hint'] = response
			sia_json['model'] = "EMOTOK"
		
		return sia_json

def get_idol_time(input_json):
	entity = None	

	for morph in input_json['input_list']:
		if "90" in morph[0]:
			entity = '1990년도'
		elif "00" in morph[0]:
			entity = '2000년도'
		elif "10" in morph[0]:
			entity = '2010년도'

	if entity == None:
		entity = random.choice(['1990년도','2000년도','2010년도'])

	return entity

def get_music_time(input_json):
	entity = None	

	for morph in input_json['input_list']:
		if "60" in morph[0]:
			entity = '1960년도'
		elif "70" in morph[0]:
			entity = '1970년도'
		elif "80" in morph[0]:
			entity = '1980년도'

	if entity == None:
		entity = random.choice(['1960년도','1970년도','1980년도'])

	return entity
