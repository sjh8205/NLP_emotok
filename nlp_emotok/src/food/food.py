#음식에 관련된 QA
from . import food_rnn
from .. import pyjosa
from ..sia import relation_query
import os, datetime

filename_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/entity_csv/food_entity.csv'
f = open(filename_path,'r',encoding='utf-8')
food_list = f.readlines()

now = datetime.datetime.now()
nowDate = now.strftime('%m')
nowDate = int(nowDate)

def get_data(input_json):
	property_dic = {'보관':'has_storage_info','구매':'has_purchase_info','구입':'has_purchase_info',
                    '효능':'has_goods_info','손질':'has_refine_info','소개':'has_intro_info','열량':'has_cal_info','칼로리':'has_cal_info'}
	entity_list = []
	query = input_json['query'].replace(' ','')	
	
	#쿼리 내 음식명 추출
	for food in food_list:
		food = food.replace('\n','')
		if food in query:
			entity_list.append(food)

	_json = dict()
	return_json = dict()
	#음식명 없을 때
	if len(entity_list) == 0:
		if "제철" in query:
			_json['relation'] = "has_season_food"
			_json['entity'] = get_season(input_json['input_list'])
			sia_json = relation_query.get_sia_data(_json)
			
			if sia_json['hint'] == 0:
				response = food_rnn.get_response(input_json['query'])
				model = "EMOTK"
				return_json['hint'] = response
			else:
				#hint = pyjosa.replace_josa(_json['entity'] + " 제철음식으로는 " + sia_json['hint'] + "(이)가 있어요!")
				return_json['hint'] = sia_json['hint']
				return_json['data'] = sia_json['data']
				return_json['model'] = "SIA"
			return return_json
			
	#음식명이 있을때
	else:
		#쿼리에 포함된 음식명에서 가장 긴 음식명 추출
		entity = max(entity_list, key=len)
		#쿼리에 PROPERTY 포함시 SIA 활용
		for morph in input_json['input_list']:
			for prop in property_dic.keys():
				if morph[0] == prop:
					_json['entity'] = entity
					_json['relation'] = property_dic[prop]
					sia_json = relation_query.get_sia_data(_json)
					if sia_json['hint'] == 0:
						response = food_rnn.get_response(input_json['query'])
						return_json['model'] = "EMOTOK"
						return_json['hint'] = response
					else:
						return_json['hint'] = sia_json['hint']
						return_json['data'] = sia_json['data']
						return_json['model'] = "SIA"
					return return_json

	response = food_rnn.get_response(input_json['query'])
	return_json['model'] = "EMOTOK"
	return_json['hint'] = response
	return return_json

def get_season(input_list):
	season = ['봄','여름','가을','겨울','월']
	now = datetime.datetime.now()
	nowDate = now.strftime('%m')
	nowDate = int(nowDate)

	for _season in season:
		for i in range(0,len(input_list)):
			if _season == input_list[i][0]:
				if _season == "월":
					month = int(input_list[i-1][0])
					if 1 <= month <= 12:
						nowDate = month
				else:
					return _season
					
	if 3 <= nowDate <= 5:
		season = "봄"
	elif 6<= nowDate <= 8:
		season = "여름"
	elif 9<= nowDate <=11:
		season = "가을"
	else:
		season = "겨울"

	return season
