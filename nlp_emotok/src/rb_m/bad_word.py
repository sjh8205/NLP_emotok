import random,os
f_bad_word = open(os.path.dirname(os.getcwd())+'/nlp-beanq-service/src/dasom2/rb_m/dictionary/bad_word.txt','r',encoding='utf-8')
bad_word_list = f_bad_word.readlines()

def replace_badword(response):

	ment_list = ['잘 모르겠어요',
				 '잘 알아 듣지 못했어요',
				 '아직 공부가 더 필요해요']
	
	if response == 0:
		ment = random.choice(ment_list)
		return ment

	_response = response.replace(" ","")

	for bad_word in bad_word_list:
		bad_word = bad_word.replace("\n","")
		if bad_word in _response:
			ment = random.choice(ment_list)
			return ment

	return response
	
