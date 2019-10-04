#건강에 관련된 QA
from .. import pyjosa
from ..sia import relation_query
from . import health_rnn
import os, datetime, random

filename_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/entity_csv/illness_entity.csv'
f = open(filename_path,'r',encoding='utf-8')
illness_list = f.readlines()

def get_data(input_json):
	entity_list = []
	query = input_json['query'].replace(' ','')	
	
	#쿼리 내 질병 추출
	for illness in illness_list:
		illness = illness.replace('\n','')
		if illness in query:
			entity_list.append(illness)

	_json = dict()
	
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
				hint = relation_query.get_sia_data(_json)
				hint = pyjosa.replace_josa(entity + "(을)를 예방하기 위해 " + hint)
				_json['hint'] = hint
			elif morph[0] == "음식":
				_json['relation'] = 'has_good_food'
				food = relation_query.get_sia_data(_json)
				hint = pyjosa.replace_josa(entity + "에는 " +food+ "(이)가 좋다고 해요!")
				_json['hint'] = hint

		if _json['hint'] == None:
			relation = random.choice(['has_prevention','has_good_food'])
			print(relation)
			_json['relation'] = relation
			if relation == 'has_prevention':
				hint = relation_query.get_sia_data(_json)
				hint = pyjosa.replace_josa(entity + "(을)를 예방하기 위해 " + hint)
				_json['hint'] = hint
			else:
				food = relation_query.get_sia_data(_json)
				hint = pyjosa.replace_josa(entity + "에는 " +food+ "(이)가 좋다고 해요!")
				_json['hint'] = hint
		
		sia = True
		return sia, _json
	else:
		response = health_rnn.get_response(input_json['query'])
		_json['hint'] = response
		sia = False
		return sia, _json	
