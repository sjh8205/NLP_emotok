import os

filename_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/entity_csv/entity_chitchat.csv'
entity_file = open(filename_path,'r', encoding='utf-8')
entity_list = entity_file.readlines()

def get_triple(input_json):

	entity_dict = get_entity(input_json['query'])
	
	if entity_dict['result'] == 1:
		triple_dict = get_relation(input_json,entity_dict)
		return triple_dict
	else:
		return entity_dict


def get_entity(_query):
	query = _query.replace(' ','')

	entity_dict = dict()

	for _entity in entity_list:
		_entity = _entity.split(',')
		entity = _entity[0]
		label = _entity[1].replace('\n','')
		if entity in query:
			entity_dict['result'] = 1
			entity_dict['category'] = label
			entity_dict['entity'] = entity
			return entity_dict

	entity_dict['result'] = 0
	return entity_dict

def get_relation(input_json, entity_dict):
	if entity_dict['category'] == "flower":
		triple_dict = flower_relation(input_json, entity_dict)
	elif entity_dict['category'] == "greatman":
		triple_dict = greatman_relation(input_json,entity_dict)
	elif entity_dict['category'] == "popword":
		entity_dict['relation'] = "has_popword_info"
		triple_dict = entity_dict
	elif entity_dict['category'] == "tour":
		triple_dict = tour_relation(input_json, entity_dict)

	return triple_dict

def tour_relation(input_json, triple_dict):
	triple_dict['relation'] = 0
	
	for _input in input_json['input_list']:
		morph = _input[0]
		
		if morph in ["소개","추천"]:
			triple_dict['relation'] = 'has_tour_reco'
		elif morph in ["정보","팁"]:
			triple_dict['relation'] = 'has_tour_info'
		
	if triple_dict['relation'] == 0:
		triple_dict['result'] = 0
	
	return triple_dict

def flower_relation(input_json,triple_dict):
	if triple_dict['entity'] == '국화':
		triple_dict['entity'] = random.choice(['빨간 국화','하얀 국화','노란 국화'])
	
	triple_dict['relation'] = 'has_flower_hint'
	
	return triple_dict	
	
def greatman_relation(input_json,triple_dict):
	triple_dict['relation'] = 0	

	for _input in input_json['input_list']:
		morph = _input[0]
		if morph in ['업적']:
			triple_dict['relation'] = 'has_career_info'
		elif morph in ['소개','누구']:
			triple_dict['relation'] = 'has_intro_info'
		elif morph in ['태어났','생년월일','생일','돌아가']:
			triple_dict['relation'] = 'has_lifetime_info'
		
	if triple_dict['relation'] == 0:
		triple_dict['result'] = 0
		
	return triple_dict

