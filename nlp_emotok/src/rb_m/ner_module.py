import pymysql, os
from .. import pyjosa

filename_path = os.path.dirname(os.getcwd())+'/roja-emotok/src/rb_m/dictionary/ner_list.csv'
filename_path_1 = os.path.dirname(os.getcwd())+'/roja-emotok/src/rb_m/dictionary/ner_list_1.csv'
f = open(filename_path,'r',encoding='utf-8')
f1 = open(filename_path_1,'r',encoding='utf-8')
ner_list = f.readlines()
ner_1_list = f1.readlines()

def get_ner_hint(input_json):
	ner_tag = get_ner_tag(input_json)

	if ner_tag == 0:
		return 0
	else:
		hint = get_template(ner_tag)
		return hint

def get_ner_tag(input_json):
	query = input_json['query']
	query = query.replace(" ","")

	for _ner in ner_list:
		_ner = _ner.split(',')
		if _ner[0] in input_json['query']:
			_ner[1] = _ner[1].replace("\n","")
			return _ner

	for _nouns in input_json['nouns']:
		for _ner_1 in ner_1_list:
			_ner_1 = _ner_1.split(',')
			if _ner_1[0] in _nouns:
				_ner_1[1] = _ner_1[1].replace("\n","")
				return _ner_1

	return 0
	
def get_template(ner_tag):
    conn = pymysql.connect(
        host='35.229.155.246',
        user='root',
        password='rojaroja',
        db='wp_data',
        charset='utf8',
        cursorclass=pymysql.cursors.DictCursor
    )
    
    tag = ner_tag[1]

    with conn.cursor() as cursor:
        question_sql = "SELECT template FROM wp_data.dasom_ner_hint_single where tag=%s order by rand() limit 1;"
        cursor.execute(question_sql, (tag))
        row = cursor.fetchall()
		
        if row == ():
            return 0
        
        for a in row:
            template = a['template']
            if "%s" in template:
                template = template.replace("%s", ner_tag[0])
                template = pyjosa.replace_josa(template)

        return template



			
