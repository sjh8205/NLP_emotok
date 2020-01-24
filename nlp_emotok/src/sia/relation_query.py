#git Test
import requests,json

oper_1 = "http://0.0.0.0:5001/roja/answer"
oper_2 = "http://0.0.0.0:5007/roja/answer"
devel = "http://0.0.0.0:5005/roja/answer"

def get_sia_data(triple_dict):
	_data = {
			'entity':triple_dict['entity'],
			'relation':triple_dict['relation']
			}

	if triple_dict['server'] == "oper_1":
		r_json = requests.post(oper_1,
				headers={'Content-Type': 'application/json; charset=utf-8'},
				data=json.dumps(_data, ensure_ascii=False).encode('utf-8'))

	elif triple_dict['server'] == "oper_2":
		r_json = requests.post(oper_2,
				headers={'Content-Type': 'application/json; charset=utf-8'},
				data=json.dumps(_data, ensure_ascii=False).encode('utf-8'))
	
	elif triple_dict['server'] == "devel":
		r_json = requests.post(devel,
				headers={'Content-Type': 'application/json; charset=utf-8'},
				data=json.dumps(_data, ensure_ascii=False).encode('utf-8'))

	r_json = r_json.json()
	return_json = dict()

	if r_json['status_code'] == 1:
		return_json['hint'] = 0
		return return_json

	else:
		return_json['hint'] = r_json['data']['answer']
		return_json['data'] = r_json['data']
		return return_json

