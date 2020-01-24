#건강에 관련된 QA
from .. import pyjosa
from ..sia import relation_query
from . import health_rnn
import os, datetime, random

filename_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/entity_csv/illness_entity.csv'
#filename_1_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/entity_csv/illness_entity_1.csv'
f = open(filename_path,'r',encoding='utf-8')
#f_1 = open(filename_1_path,'r',encoding='utf-8')
illness_list = f.readlines()
#illness_1_list = f_1.readlines()

def get_data(input_json):
	entity_list = []
	query = input_json['query'].replace(' ','')	
	
	#쿼리 내 질병 추출
	for illness in illness_list:
		#illness = illness.split()
		#illness[1] = illness[1].replace('\n','')
		illness = illness.replace('\n','')
		if illness in query:
			entity_list.append(illness)

	'''
	if len(entity_list) != 0:
		for nouns in input_json['nouns']:
	'''		

	_json = dict()
	return_json = dict()
	
	#해당 질병이 있을 때
	if len(entity_list) != 0:
		_json['hint'] = None
		#쿼리에 포함된 음식명에서 가장 긴 질병 추출
		entity = max(entity_list, key=len)
		_json['entity'] = entity
		#SIA 활용
		for morph in input_json['input_list']:
			if morph[0] == "예방" or morph[0] == "예방법":
				_json['relation'] = 'has_prevention'
				_json['server'] = input_json['server']
				sia_json = relation_query.get_sia_data(_json)
				#hint = pyjosa.replace_josa(entity + "(을)를 예방하기 위해 " + hint)
				_json['hint'] = sia_json['hint']
			elif morph[0] == "음식":
				_json['relation'] = 'has_good_food'
				_json['server'] = input_json['server']
				sia_json = relation_query.get_sia_data(_json)
				#hint = pyjosa.replace_josa(entity + "에는 " +food+ "(이)가 좋다고 해요!")
				_json['hint'] = sia_json['hint']

		if _json['hint'] == None:
			relation = random.choice(['has_prevention','has_good_food'])
			_json['relation'] = relation
			_json['server'] = input_json['server']
			sia_json = relation_query.get_sia_data(_json)
		
		if sia_json['hint'] == 0:
			response = health_rnn.get_response(input_json['query'])
			return_json['hint'] = response
			return_json['model'] = 'EMOTOK'
		else:
			return_json['hint'] = sia_json['hint']
			return_json['data'] = sia_json['data']
			return_json['model'] = "SIA"
		return return_json

	else:
		response = health_rnn.get_response(input_json['query'])
		return_json['hint'] = response
		return_json['model'] = "EMOTOK"
		return return_json	
