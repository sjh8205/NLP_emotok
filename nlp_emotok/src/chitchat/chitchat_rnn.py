import os, random
from .model.eval import eval
from konlpy.tag import Mecab

chat_response = eval()

def get_json(query):
	non_response_list = ['한 번만 더 말씀해 주시겠어요','바보얌','잘 알아듣지 못했어요']

	response = get_response(query)
	
	for non_response in non_response_list:
		if non_response == response:
			serviceName = "human_intelligence"
			actionName = "human_intelligence"
		else:
			serviceName = "Chitchat"
			actionName = "Chitchat_speech"

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
					"serviceName": serviceName,
					"actionName": actionName
				}
			]
		},
		"query":query,
		"semantic":{
			"outputContext": {
				"service": "",
				"context": ""
			},
			"service": serviceName,
			"params": None,
			"action": actionName
		}

		}

	}
	
	return return_json

def get_response(query):

	conversations = []
	conversations.append(query)
	response = chat_response.chat_generate(conversations)
	return response


