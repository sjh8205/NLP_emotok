import os, random
from .model.eval import eval
from konlpy.tag import Mecab

chat_response = eval()

def get_json(query):

	response = get_response(query)
	
	return_json = {
	"result": 0,
	"msg": "success",
	"data":{
		"status": {
				"errorType": "success",
				"code" : 0
		},
		"result": {
			"hint": response,
			"formatType": "text",
			"data":[
				{
					"serviceName": "Chitchat",
					"actionName": "Chitchat_speech"
				}
			]
		},
		"query":query,
		"semantic":{
			"outputContext": {
				"service": "",
				"context": ""
			},
			"service": "Chitchat",
			"params": None,
			"action": "Chitchat_speech"
		}

		}

	}
	
	return return_json

def get_response(query):

	conversations = []
	conversations.append(query)
	response = chat_response.chat_generate(conversations)
	return response

