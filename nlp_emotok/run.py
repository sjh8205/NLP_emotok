# -*- coding: utf-8 -*-
"""
Copyright (C) 원더풀플랫폼

@brief Flask App of ROJA_2MOTOK Server
@author Dongsu Shin
"""
#import re, random, os, csv, sys, time, json, traceback
from flask import Flask, request
from flask import make_response
from flask import redirect, url_for
from logging.config import dictConfig
#from flask import Flask, jsonify, request, render_template, url_for, redirect, session, make_response, current_app
#from functools import update_wrapper
from flask_cors import CORS, cross_origin
from src import emotok
from src.sia import relation_query
from src.log import loglog
from src.db import set_DB_info
from src.sia import question
import traceback, json
import pymysql
import random
import traceback

dictConfig({
        'version': 1,
        'formatters': {
                'simple': {
                        'format': '%(asctime)s %(name)s %(levelname)s %(message)s'
                }
        },
        'handlers': {
                'file': {
                        'class': 'logging.FileHandler',
                        'level': 'DEBUG',
                        'formatter': 'simple',
                        'filename': '/var/log/flask/flask.log',
                        'encoding': 'utf-8'
                }
        },
        'loggers': {
                'file': {
                        'level': 'DEBUG',
                        'handlers': ['file']
                }
        },
        'root': {
                'level': 'DEBUG',
                'handlers': ['file']
        }
})

app = Flask(__name__)
CORS(app)
cors = CORS(app, resources={r"/*": {"origins": "*"}})

# 서버 정상 구동 확인 함수
@app.route('/', methods=['GET', 'POST'])
def main():
        #return redirect(url_for('successive_question'), code=307)
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

	"""
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
	"""
        
@app.route('/roja/random_question', methods=['POST'])
def random_question():
    data = question.random()
    data = NoneToStr(data)

    response = dict()
    response['data'] = data
    response['status_code'] = 0

    app.logger.debug("{}: {}".format(random_question.__name__, json.dumps(response, ensure_ascii=False)))

    return make_response(json.dumps(response, ensure_ascii=False))
	
@app.route('/roja/successive_question', methods=['POST'])
def successive_question():
    req = request.get_json()
    req = StrToNone(req)

    response = dict()
    try:
        data = question.succesive(req)
        data = NoneToStr(data)
        response['data'] = data
        response['status_code'] = 0
    except ValueError as ve:
        response['data'] = dict()
        response['status_code'] = 1
        app.logger.debug("{}: {}".format(successive_question.__name__, traceback.format_exc()))
    except Exception:
        response['data'] = dict()
        response['status_code'] = 1
        app.logger.debug("{}: {}".format(successive_question.__name__, traceback.format_exc()))

    app.logger.debug("{}: {}".format(successive_question.__name__, json.dumps(req, ensure_ascii=False)))
    app.logger.debug("{}: {}".format(successive_question.__name__, json.dumps(response, ensure_ascii=False)))
    
    return make_response(json.dumps(response, ensure_ascii=False))

@app.route('/roja/answer', methods=['POST'])
def answer_question():
        req = request.get_json()
        req = StrToNone(req)
        response = dict()
        try:
                data = question.answer(req['entity'], req['relation'])
                data = NoneToStr(data)
                response['data'] = data
                response['status_code'] = 0
        except Exception as e:
                response['data'] = dict()
                response['status_code'] = 1
                app.logger.debug("{}: {}".format(answer_question.__name__, traceback.format_exc()))

        app.logger.debug("{}: {}".format(answer_question.__name__, json.dumps(req, ensure_ascii=False)))
        app.logger.debug("{}: {}".format(answer_question.__name__, json.dumps(response, ensure_ascii=False)))
        
        return make_response(json.dumps(response, ensure_ascii=False))

def error_send():
	conn = set_DB_info.get_sms_db()
	sql_query = "INSERT INTO SMS_MSG (REQDATE, STATUS, TYPE, PHONE, CALLBACK, MSG )		VALUES ( now(), '1', '0', '01034412229', '0222979383', '2MOTOK ERROR' );" 
	conn.cursor().execute(sql_query)
	conn.commit()

def StrToNone(json):
    for key in json:
        if isinstance(json[key], dict):
            json[key] = StrToNone(json[key])
        else:
             if json[key] == "None":
                json[key] = None

    return json

def NoneToStr(json):
    for key in json:
        if isinstance(json[key], dict):
            json[key] = NoneToStr(json[key])
        else:
            if json[key] == None:
                json[key] = "None"
    return json
	
if __name__ == "__main__":
	app.run(host='0.0.0.0', port=5001)
