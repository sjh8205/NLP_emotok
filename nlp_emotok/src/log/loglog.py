# -*- coding: utf-8 -*-
from datetime import datetime
import logging
import logging.handlers

def access_log(message):
	access_logger = logging.getLogger("access")
	access_logger.setLevel(logging.INFO)

	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	#stream_hander = logging.StreamHandler()
	#stream_hander.setFormatter(formatter)
	#access_logger.addHandler(stream_hander)

	log_max_size = 10 * 1024 * 1024
	log_file_count = 5
	#file_handler = logging.FileHandler('/usr/local/log/dasom2/access/access.log')
	
	file_Handler = logging.handlers.RotatingFileHandler(
		filename='/usr/local/log/emotok/access/access.log',
		maxBytes=log_max_size,
		encoding = "utf-8",
		backupCount=log_file_count
	)
	
	file_Handler.setFormatter(formatter)
	access_logger.addHandler(file_Handler)

	access_logger.info(message)

def error_log(message):
	error_logger = logging.getLogger("error")
	error_logger.setLevel(logging.INFO)
	
	formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

	#stream_hander = logging.StreamHandler()
	#stream_hander.setFormatter(formatter)
	#error_logger.addHandler(stream_hander)

	log_max_size = 10 * 1024 * 1024
	log_file_count = 5

	file_Handler = logging.handlers.RotatingFileHandler(
		filename='/usr/local/log/emotok/error/error.log',
		maxBytes=log_max_size,
		encoding = "utf-8",
		backupCount=log_file_count
	)

	file_Handler.setFormatter(formatter)
	error_logger.addHandler(file_Handler)
	
	error_logger.error(message)
