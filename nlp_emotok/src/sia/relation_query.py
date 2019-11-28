import requests,json

def get_sia_data(triple_dict):
    _data = {
            'entity':triple_dict['entity'],
            'relation':triple_dict['relation']
            }

    r_json = requests.post("http://0.0.0.0:5005/roja/answer",
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
