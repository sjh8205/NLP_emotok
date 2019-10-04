#!/usr/bin/env python
# -*- coding: utf-8 -*-
from .solver import Solver, VariationalSolver
from .data_loader import get_loader
from .configs import Config
from .utils import Vocab, Tokenizer, PAD_TOKEN, SOS_TOKEN, EOS_TOKEN
import os
import pickle
import json
from .models import VariationalModels, HRED
from konlpy.tag import Mecab

max_sent_len = 50
max_conv_len = 100
word2vec_path = "../datasets/GoogleNews-vectors-negative300.bin"
senti_dic_path = "../datasets/SentiWord_info.json"

def load_pickle(path):
    with open(str(path), 'rb') as f:
        return pickle.load(f)

def to_pickle(obj, path):
    with open(str(path), 'wb') as f:
		    return pickle.dump(obj, f)

def kor2eng(sentence):
    translator = Translator()
    return translator.translate(sentence, dest='en').text

def eng2kor(sentence):
    translator = Translator()
    return translator.translate(sentence, dest='ko').text

def pad_sentences(conversations, max_sentence_length=30, max_conversation_length=100):
    def pad_tokens(tokens, max_sentence_length = max_sentence_length):
        n_valid_tokens = len(tokens)
        if n_valid_tokens > max_sentence_length -1:
            tokens = tokens[:max_sentence_length -1]
        n_pad = max_sentence_length - n_valid_tokens -1
        tokens = tokens + [EOS_TOKEN] + [PAD_TOKEN] * n_pad
        return tokens
        
    def pad_conversation(conversation):
        conversation = [pad_tokens(sentence) for sentence in conversation]
        return conversation
    
    all_padded_sentences = []
    all_sentence_length = []

    for conversation in conversations:
        if len(conversation) > max_conversation_length:
            conversation = conversations[:max_conversation_length]
        sentence_length = [min(len(sentence)+1, max_sentence_length) for sentence in conversation]
        all_sentence_length.append(sentence_length)

        sentences = pad_conversation(conversation)
        all_padded_sentences.append(sentences)
    sentences = all_padded_sentences
    sentence_length = all_sentence_length
    return sentences, sentence_length

def get_sentence_polarity(sentence):
    with open(senti_dic_path, encoding='utf-8', mode='r') as f:
        data = json.load(f)
    r_word = list()
    s_word = list()
    for word in sentence.split():
        result = ['None', 'None']
        for i in range(0, len(data)):
            if data[i]['word'] == word:
                result.pop()
                result.pop()
                result.append(data[i]['word_root'])
                result.append(data[i]['polarity'])
        if result[1] =='None':
            result[1] = 0
        else:
            result[1] = int(result[1])

        r_word.append(result[0])
        s_word.append(result[1])
    '''
    if sum(s_word) >0:
        return print('Positive : {}'.format(sum(s_word)))
    elif polarity_score <0:
        return print('Negative : {}'.format(sum(s_word)))
    else:
        return null
    '''
    return 0 

def checkTrait(c):
    return (int((ord(c) - 0xAC00) % 28) != 0)

def sentence_compound(generated_sen):
    word_list = list()
    for word_pos in generated_sen.split():
        if len(word_pos.split('+')) <2:
            return '다시 한번 말씀해주시겠어요?'
        word = word_pos.split('+')[0]
        pos = word_pos.split('+')[1]
        if pos.startswith('J') or pos.startswith('E') or pos.startswith('SF') or pos.startswith('XS'):
            if len(word_list) ==0:
                word_list.append(word)
                continue
            prev_word = word_list.pop()
            if checkTrait(prev_word[-1]): #받침 있는 경우
                if word == '를':
                    word = '을'
                elif word == '가':
                    word = '이'
                elif word == '는':
                    word = '은'
                elif word == '라는':
                    word = '이라는'
            else: # 받침 없는 경우
                if word == '을':
                    word = '를'
                elif word == '이':
                    word ='가'
                elif word == '은':
                    word = '는'
                elif word == '이라는':
                    word = '라는'
            
            word_list.append(prev_word+word)
        else:
            word_list.append(word)
    return ' '.join(word_list)

class eval(object):
    def __init__(self):
        #print(checkpoint)
        model = 'VHRED'
        morph = False
        pos = True
        checkpoint = '/usr/local/roja-emotok/nlp_emotok/src/health/checkpoint/dasom2/'+model+'/pos-1000-100-40-0.0001/40.pkl'
        #self.config = get_config(model=model, morph=morph, pos=pos, checkpoint=checkpoint)
        self.config = Config(model=model, pos=pos, checkpoint=checkpoint)
        self.vocab = Vocab()
        self.vocab.load(self.config.word2id_path, self.config.id2word_path)
        print('Vocabulary Size : {}'.format(self.vocab.vocab_size))
        self.config.vocab_size = self.vocab.vocab_size
        conversations = []
        conversation_length = []
        sentence = []
        use_cuda = True
        if self.config.model in VariationalModels:
            self.solver = VariationalSolver(self.config, None, None, vocab=self.vocab, is_train=False)
            self.solver.build(use_cuda)
        else:
            self.solver = Solver(self.config, None, None, vocab=self.vocab,is_train=False)
            self.solver.build(use_cuda)


    def chat_generate(self, dialogue):
        sentence = []
        conversations =[]
        conversation_length =[]

        #get_sentence_polarity(current_converse)
        for dialog in dialogue:
            if self.config.morph:
                mecab = Mecab()
                #print(mecab.morphs(dialog))
                sentence.append(mecab.morphs(dialog))
            elif self.config.pos:
                mecab = Mecab()
                pos = list()
                for instance in mecab.pos(dialog):
                    word = '+'.join(instance)
                    pos.append(word)
                #print(pos)
                sentence.append(pos)
            else:
                sentence.append(dialog.split())
        sentence.append('대화 생성 결과'.split())    

        conversations.append(sentence)
        conversation_length.append(len(conversations[0]))
        sentences, sentence_length = pad_sentences(conversations, max_sentence_length=max_sent_len, max_conversation_length=max_conv_len)
        
        # After padding, call get_loader with batch_size =1 ? 
        data_loader = get_loader(
            sentences = sentences,
            conversation_length = conversation_length,
            sentence_length = sentence_length,
            vocab=self.vocab,
            batch_size = 80)
        sentence.pop()
        generated_sen = self.solver.nlg(data_loader)
        # generated sentence는 morph, pos에 따라 Decoded Sentence가 다름

        if self.config.morph:
            sentence.append(generated_sen.split())
            return generated_sen
        elif self.config.pos:
            #complete_sen = ' '.join(list(word.split('+')[0] for word in generated_sen.split()))
            complete_sen = sentence_compound(generated_sen)
            sentence.append(complete_sen)
            return complete_sen
        else:
            sentence.append(generated_sen.split())
            return generated_sen
   
'''
if __name__ == '__main__':
    # 2019.01.11 1st Prototype
    config = get_config(mode = 'test')
    print('Loading Vocabulary ... ')
    vocab = Vocab()
    vocab.load(config.word2id_path, config.id2word_path)
    print('Vocabulary Size : {}'.format(vocab.vocab_size))
    config.vocab_size = vocab.vocab_size
    conversations = []
    conversation_length = []
    sentence = []
    on_cpu = True
    use_cuda = True
    if config.model in VariationalModels:
        solver = VariationalSolver(config, None, None, vocab=vocab, is_train=False)
        solver.build()
    else:
        solver = Solver(config, None, None, vocab=vocab, is_train=False)
        solver.build(use_cuda)



    while True:
        conversations = []
        conversation_length = []
        current_converse = input('[User] : ')

        #get_sentence_polarity(current_converse)

        if current_converse in ['exit', 'exit']:
            break
        if config.morph:
            mecab = Mecab()
            sentence.append(mecab.morphs(current_converse))
            sentence.append(mecab.morphs('대화 생성 결과'))
        else:
            sentence.append(current_converse.split())
            sentence.append('대화 생성 결과'.split())

        conversations.append(sentence)
        conversation_length.append(len(conversations[0]))
        sentences, sentence_length = pad_sentences(conversations, max_sentence_length=max_sent_len, max_conversation_length=max_conv_len)
        # print(sentences)
        
        # After padding, call get_loader with batch_size =1 ? 
        data_loader = get_loader(
            sentences = sentences,
            conversation_length = conversation_length,
            sentence_length = sentence_length,
            vocab=vocab,
            batch_size = 100)
        sentence.pop()
        generated_sen = solver.nlg(data_loader)

        if config.morph:
            mecab = Mecab()
            sentence.append(mecab.morphs(generated_sen))
        else:
            sentence.append(generated_sen.split())

        print('[Chatbot] : {}'.format(generated_sen))
        #get_sentence_polarity(generated_sen)

    '''

