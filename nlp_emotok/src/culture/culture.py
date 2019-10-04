#노래에 관련된 QA
from ..sia import relation_query
from . import culture_rnn
import random

def get_data(input_json):

	_json = dict()
	_json['entity'] = None
	_json['relation'] = None

	for morph in input_json['input_list']:
		if "60" in morph[0]:
			_json['entity'] = '1960년도'
		elif "70" in morph[0]:
			_json['entity'] = '1970년도'
		elif "80" in morph[0]:
			_json['entity'] = '1980년도'
		elif morph[0] == '노래':
			_json['relation'] = 'has_song_info'
		elif morph[0] == '음악':
			_json['relation'] = 'has_music_info' 

	if _json['entity'] == None:
		sia = False
		response = culture_rnn.get_response(input_json['query'])
		_json['hint'] = response
		return sia, _json
	else:
		if _json['relation'] == None:
			_json['relation'] = random.choice(['has_song_info','has_music_info'])
		
		hint = relation_query.get_sia_data(_json)
		_json['hint'] = hint
		sia = True
		return sia, _json
