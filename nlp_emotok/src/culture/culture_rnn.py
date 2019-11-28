import os, random
from .model.eval import eval
from konlpy.tag import Mecab
from fuzzywuzzy import fuzz

chat_response = eval()
answer_path = os.path.dirname(os.getcwd())+'/nlp_emotok/src/culture/answer/culture_answer.csv'
answer_file = open(answer_path,'r', encoding='utf-8')
answer_list = answer_file.readlines()

def get_response(query):

	conversations = []
	conversations.append(query)
	response = chat_response.chat_generate(conversations)

	response = text_refine(response)

	return response


def text_refine(_response):
    max_ratio = 0
    response = dict()

    for answer in answer_list:
        answer = answer.split(',')
        ratio = fuzz.ratio(answer[0], _response)
        if max_ratio < ratio:
            max_ratio = ratio
            result = answer

    return result
