import csv,os,random
from fuzzywuzzy import fuzz

#룰 베이스에 맞는 발화멘트(인사...)
def get_hint(input_json, threshold):
	filename_path = os.path.dirname(os.getcwd())+'/nlp-beanq-service/src/dasom2/rb_m/dictionary/greeting.csv'
	#유사도 결과
	max_ratio = 0
	#발화 멘트
	hint_dic = {}
	
	query = input_json['query']
	
	#csv파일 -> Dic 형태로
	with open(filename_path, 'r', encoding='utf-8') as f:
		csv_reader = csv.reader(f)
		for row in csv_reader:
			hint_dic[row[0]] = row[1]

	#가장 높은 유사도 판별
	for text in hint_dic.keys():
		ratio = fuzz.ratio(query, text)
		if max_ratio < ratio:
			max_ratio = ratio
			result = text
	
	if max_ratio >= threshold:
		hint = get_ment(hint_dic[result])
		return_json = {'appId':'dasom2',
						'clientId':input_json['clientId'],
						'domain': 'asr',
						'hint' : hint,
						'data' : {
							"serviceName": "emotok",
							"actionName": "emotok"
						}
					}
		return return_json
	else:
		return 0

#다양한 발화를 가져옴
def get_ment(key):
	filename_path = os.path.dirname(os.getcwd())+'/nlp-beanq-service/src/dasom2/rb_m/ment/greeting.csv'
	ment_list = []
	
	with open(filename_path, 'r', encoding='utf-8') as f:
		csv_reader = csv.reader(f)
		for row in csv_reader:
			if row[0] == key:
				ment_list.append(row[1])

	return random.choice(ment_list)
