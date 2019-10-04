#! /usr/bin/env python
# -*- coding: utf-8 -*-
import json
#import sys
import tensorflow as tf
import numpy as np
import os
#import data_helpers
#from sdd.multi_class_data_loader import MultiClassDataLoader
#from sdd.word_data_processor import WordDataProcessor
from . import data_helpers
from .multi_class_data_loader import MultiClassDataLoader
from .word_data_processor import WordDataProcessor
import csv
import time

os.environ['TF_CPP_MIN_LOG_LEVEL']='2'

# Parameters
# ==================================================

# Eval Parameters
#tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
#tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
#tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")

# Misc Parameters
#tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")
#tf.flags.DEFINE_boolean("log_device_placement", False, "Log placement of ops on devices")

#data_loader = MultiClassDataLoader(tf.flags, WordDataProcessor())
#data_loader.define_flags()

#FLAGS = tf.flags.FLAGS
#FLAGS(sys.argv)

#tf.flags.DEFINE_integer("batch_size", 64, "Batch Size (default: 64)")
#tf.flags.DEFINE_string("checkpoint_dir", "", "Checkpoint directory from training run")
#tf.flags.DEFINE_boolean("eval_train", False, "Evaluate on all training data")	
#tf.flags.DEFINE_boolean("allow_soft_placement", True, "Allow device soft device placement")

data_loader = MultiClassDataLoader(tf.flags, WordDataProcessor())
#data_loader.define_flags()

#FLAGS = tf.flags.FLAGS
#FLAGS(sys.argv)

def get_label(preprocessing_text):

	#data_loader = MultiClassDataLoader(tf.flags, WordDataProcessor())
	#data_loader.define_flags()

	#FLAGS = tf.flags.FLAGS
	#FLAGS(sys.argv)


	x_raw = [preprocessing_text]
	#가장 최근 학습데이터
	latest_subdir = './emotok_label/runs/0729_emotok_label'
	#FLAGS.checkpoint_dir = latest_subdir + "/checkpoints/"
	
	# Map data into vocabulary
	#vocab_path = os.path.join(FLAGS.checkpoint_dir, "..", "vocab")
	vocab_path = '/usr/local/roja-emotok/src/emotok_label/runs/0729_emotok_label/vocab'
	vocab_processor = data_loader.restore_vocab_processor(vocab_path)
	x_test = np.array(list(vocab_processor.transform(x_raw)))


	# Evaluation
	# ==================================================
	#checkpoint_file = tf.train.latest_checkpoint(FLAGS.checkpoint_dir)
	checkpoint_file = '/usr/local/roja-emotok/src/emotok_label/runs/0729_emotok_label/checkpoints/model-290000'
	
	graph = tf.Graph()
	with graph.as_default():
		session_conf = tf.ConfigProto(
			allow_soft_placement=True)
			#allow_soft_placement=FLAGS.allow_soft_placement)
			#log_device_placement=FLAGS.log_device_placement)
		sess = tf.Session(config=session_conf)
		with sess.as_default():
			# Load the saved meta graph and restore variables
			saver = tf.train.import_meta_graph("{}.meta".format(checkpoint_file))
			saver.restore(sess, checkpoint_file)
			
			# Get the placeholders from the graph by name
			input_x = graph.get_operation_by_name("input_x").outputs[0]
			#input_y = graph.get_operation_by_name("input_y").outputs[0]
			dropout_keep_prob = graph.get_operation_by_name("dropout_keep_prob").outputs[0]

			#accuracy = graph.get_operation_by_name("accuracy/accuracy").outputs[0]

			# Tensors we want to evaluate
			scores = graph.get_operation_by_name("output/scores").outputs[0]
			predictions = graph.get_operation_by_name("output/predictions").outputs[0]

			# Generate batches for one epoch
			#batches = data_helpers.batch_iter(list(x_test), FLAGS.batch_size, 1, shuffle=False)
			batches = data_helpers.batch_iter(list(x_test), 64, 1, shuffle=False)

			# Collect the predictions here
			all_predictions = []

        
			for x_test_batch in batches:
				batch_predictions = sess.run(predictions, {input_x: x_test_batch, dropout_keep_prob: 1.0})
				#all_predictions = np.concatenate([all_predictions, batch_predictions])
				#batch_scores = sess.run(scores, {input_x: x_test_batch, dropout_keep_prob: 1.0})
				#batch_score = sess.run(tf.nn.softmax(batch_scores))
        
			#batch_score = batch_score.round(3)
			#print(batch_score)

			#print(all_predictions)
			#print(batch_predictions)
	
	return batch_predictions
