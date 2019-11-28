from konlpy.tag import Mecab
from .emotok_label import emotok_label
from .chitchat import chitchat
from .food import food
from .health import health
from .culture import culture

mecab = Mecab()
def get_json(input_json):
	input_json = get_pair(input_json)
	#도메인이 없을 때 (다솜 서비스 이외)
	if input_json['domain'] == None:
		#2motok 레이블 판단
		_label = emotok_label.get_label(input_json['preprocessing_text'])
		if _label[0] == 0:
			domain = "chitchat"
		elif _label[0] == 1:
			domain = "food"
		elif _label[0] == 2:
			domain = "health"
		elif _label[0] == 3:
			domain = "culture"
		input_json['domain'] = domain
	
	#도메인이 있을 때 (다솜 서비스)
	if input_json['domain'] == "chitchat":
		_json = chitchat.get_data(input_json)
	elif input_json['domain'] == "food":
		_json = food.get_data(input_json)
	elif input_json['domain'] == "health":
		_json = health.get_data(input_json)
	elif input_json['domain'] == "culture":
		_json = culture.get_data(input_json)

	#_json['sia'] = str(sia)

	return _json	

#2motok 레이블 판단을 위한 전처리
def get_pair(input_json):
	input_json['input_list'] = mecab.pos(input_json['query'])
	input_json['preprocessing_text'] = get_cnn_pair(input_json['input_list'])
	input_json['nouns'] = mecab.nouns(input_json['query'])

	return input_json

#CNN 학습 모델 사용 형태소 분석
def get_cnn_pair(input_list):
    text = ""

    for ip in input_list:
        text += ip[0]+ip[1]+" "

    text = text.strip().lower()

    return text	
