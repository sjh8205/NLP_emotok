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
		sia_json = relation_query.get_sia_data(triple_dict)
		if sia_json['hint'] == 0:
			response = ner_module.get_ner_hint(input_json)
			_json['data'] = response[0] + ', ' + response[1]
			response = response[2]
			model = "NER"
			if response == 0:
				response = chitchat_rnn.get_response(input_json['query'])
				model = "EMOTOK"
			_json['hint'] = response
		else:
			_json['hint'] = sia_json['hint']
			_json['data'] = sia_json['data']
			model = "SIA"
	else:
		#NER 활용 모듈
		response = ner_module.get_ner_hint(input_json)
		model = "NER"

		if response == 0:
			response = chitchat_rnn.get_response(input_json['query'])
			_json['hint'] = response
			_json['model'] = "EMOTOK"
			return _json
		else:
			_json['hint'] = response[2]
			_json['data'] = response[0] + ', ' + response[1]
			_json['model'] = "NER"
			return _json

	return _json
