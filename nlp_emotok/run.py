# -*- coding: utf-8 -*-
"""
Copyright (C) 원더풀플랫폼

@brief Flask App of ROJA_2MOTOK Server
@author Dongsu Shin
"""
#import re, random, os, csv, sys, time, json, traceback
from flask import Flask, request
from flask import make_response
#from flask import Flask, jsonify, request, render_template, url_for, redirect, session, make_response, current_app
#from functools import update_wrapper
from flask_cors import CORS, cross_origin
from src import emotok
from src.sia import relation_query
from src.sia import additional_question
from src.log import loglog
from src.db import set_DB_info
import traceback, json
import pymysql
import random

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# 서버 정상 구동 확인 함수
@app.route('/')
def main():
	return "ROJA 2MOTOK"

#Json return 함수
def response_json(return_json):
	return json.dumps(return_json, ensure_ascii=False)

#QA 결과
@app.route('/roja/2motok', methods=['POST'])
def ROJA_2MOTOK():
	input_json = request.get_json()
	
	try:
		return_json = emotok.get_json(input_json)
		loglog.access_log("sucess")
		return json.dumps(return_json, ensure_ascii=False)
	except Exception:
		error_msg   = traceback.format_exc()
		error_msg = error_msg + str(input_json)
		error_json = {
            "status": "fail",
            "messager": error_msg
        }
		loglog.error_log(error_msg)
		error_send()
		return json.dumps(error_json, ensure_ascii=False)

	'''
	try:
		return_json = dasom2_dialog_services.get_json(input_json)
		loglog.access_log("sucess")
		#output_json = jms.hide_variable(return_json)
		return return_json
	except Exception:
		error_msg   = traceback.format_exc()
		error_msg = error_msg + str(input_json)
		error_json = {
			"status": "fail",
			"messager": error_msg
		}
		loglog.error_log(error_msg)
		#error_send()
		return error_json
	'''
@app.route('/roja/random_question', methods=['POST'])
def random_add_question():
        _json = additional_question.random()
        """
	_json = dict()
	entity, relation = relation_query.get_random_entity_relation()
	_json['entity'] = entity
	_json['relation'] = relation
	_json['history'] = {}
	_json['yon'] = 0
	_json['add_q'] = entity + "에 대해 알려드릴까요?"
        """
	return make_response(json.dumps(_json, ensure_ascii=False))
	
@app.route('/roja/successive_question', methods=['POST'])
def successive_question():
        req = request.get_json()
        _json = additional_question.successive(req)
        return make_response(json.dumps(_json, ensure_ascii=False))

def error_send():
	conn = set_DB_info.get_sms_db()
	sql_query = "INSERT INTO SMS_MSG (REQDATE, STATUS, TYPE, PHONE, CALLBACK, MSG )		VALUES ( now(), '1', '0', '01034412229', '0222979383', '2MOTOK ERROR' );" 
	conn.cursor().execute(sql_query)
	conn.commit()
	

	
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5005)
