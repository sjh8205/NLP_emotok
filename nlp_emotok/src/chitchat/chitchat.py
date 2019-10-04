#여행에 관련된 QA
from .. import pyjosa
from ..sia import relation_query
from ..rb_m import ner_module
from . import chitchat_rnn, chitchat_detail
import os, datetime, random

#return_json
def get_data(input_json):

	triple_dict = chitchat_detail.get_triple(input_json)
	_json = dict()	

	if triple_dict['result'] == 1:
		hint = relation_query.get_sia_data(triple_dict)
		if hint == 0:
			response = ner_module.get_ner_hint(input_json)
			if response == 0:
				response = chitchat_rnn.get_response(input_json['query'])
			_json['hint'] = response
			sia = False
		else:
			_json['hint'] = hint
			_json['entity'] = triple_dict['entity']
			_json['relation'] = triple_dict['relation']
			sia = True
	else:
		#NER 활용 모듈
		response = ner_module.get_ner_hint(input_json)
		
		if response == 0:
			response = chitchat_rnn.get_response(input_json['query'])
		_json['hint'] = response
		sia = False

	return sia, _json


