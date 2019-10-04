from . import relation_query
from ..add_question import add_question

def get_answer(input_json, cate):
	_data = input_json['data']
	_json = dict()
	
	if cate == "sia":
		#sia 활용한 발화 GET
		_json['hint'] = relation_query.get_sia_data(_data)
	else:
		#amumal 발화 GET
		_json['hint'] = relation_query.get_amumal_data(_data)


	r_json = add_question.basic_add_question(input_json,_json)

	return_json = { 'appId':'dasom2',
					'clientId':input_json['clientId'],
					'domain': 'asr',
					'hint' : r_json['hint'],
					'data': r_json['data']}

	return return_json



