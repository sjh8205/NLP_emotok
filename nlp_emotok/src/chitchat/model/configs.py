import os
import argparse
from datetime import datetime
from collections import defaultdict
from pathlib import Path
import pprint
from torch import optim
import torch.nn as nn
from .layers.rnncells import StackedLSTMCell, StackedGRUCell

project_dir = Path(__file__).resolve().parent.parent
data_dir = project_dir.joinpath('datasets')


data_dict = {'cornell': data_dir.joinpath('cornell'), 
            'ubuntu': data_dir.joinpath('ubuntu'), 
            'kor': data_dir.joinpath('korean-dialogs-pkl'),
            'servicelog':data_dir.joinpath('servicelog-pkl'),
            'service+chatbot': data_dir.joinpath('service-chat-pkl'),
            'all':data_dir.joinpath('all-data-pkl'),
            'dasom2':data_dir.joinpath('dasom2-pkl'),
			'emotok':data_dir.joinpath('emotok-pkl'),
			'chitchat':data_dir.joinpath('emotok_0405_chitchat_pos_pkl')}

optimizer_dict = {'RMSprop': optim.RMSprop, 'Adam': optim.Adam}
rnn_dict = {'lstm': nn.LSTM, 'gru': nn.GRU}
rnncell_dict = {'lstm': StackedLSTMCell, 'gru': StackedGRUCell}
username = Path.home().name
save_dir = project_dir.joinpath('checkpoint/')
#save_dir = Path('/data1/{}/conversation/'.format(username))


def str2bool(v):
    """string to boolean"""
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')




'''
class Config(object):
    def __init__(self, **kwargs):
        """Configuration Class: set kwargs as class attributes with setattr"""
        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'optimizer':
                    value = optimizer_dict[value]
                if key == 'rnn':
                    value = rnn_dict[value]
                if key == 'rnncell':
                    value = rnncell_dict[value]
                setattr(self, key, value)

        # Dataset directory: ex) ./datasets/cornell/
        if self.morph:
            if self.data.lower() =='kor':
                self.dataset_dir = data_dir.joinpath('korean-dialogs-morph-pkl')
            elif self.data.lower() =='servicelog':
                self.dataset_dir = data_dir.joinpath('servicelog-morph-pkl')
            elif self.data.lower() =='service+chatbot':
                self.dataset_dir = data_dir.joinpath('service-chat-morph-pkl')
            elif self.data.lower() =='all':
                self.dataset_dir = data_dir.joinpath('all-data-morph-pkl')
            elif self.data.lower() =='dasom2':
                self.dataset_dir = data_dir.joinpath('dasom2-morph-pkl')
        elif self.pos:
            self.dataset_dir = data_dir.joinpath('emotok-pos-pkl')
        else:
            self.dataset_dir = data_dict[self.data.lower()]

        # Data Split ex) 'train', 'valid', 'test'
#        self.data_dir = self.dataset_dir.joinpath(self.mode)
        # Pickled Vocabulary
        self.word2id_path = self.dataset_dir.joinpath('word2id.pkl')
        self.id2word_path = self.dataset_dir.joinpath('id2word.pkl')

        # Pickled Dataframes
        self.sentences_path = self.dataset_dir.joinpath('sentences.pkl')
        self.sentence_length_path = self.dataset_dir.joinpath('sentence_length.pkl')
        self.conversation_length_path = self.dataset_dir.joinpath('conversation_length.pkl')
#        print(self.sentences_path)
        # Save path
        if self.mode == 'train' and self.checkpoint is None:
            #time_now = datetime.now().strftime('%Y-%m-%d_%H:%M:%S')
            para_list = []
            if self.morph:
                para_list.append('morph')
            elif self.pos:
                para_list.append('pos')
            para_list.append(self.batch_size)
            para_list.append(self.n_epoch)
            para_list.append(self.learning_rate)
            self.save_path = save_dir.joinpath(self.data, self.model).joinpath('-'.join(map(lambda x : str(x),para_list)))
            self.logdir = self.save_path
            os.makedirs(str(self.save_path), exist_ok=True)
        elif self.checkpoint is not None:
            assert os.path.exists(self.checkpoint)
            self.save_path = os.path.dirname(self.checkpoint)
            self.logdir = self.save_path

    def __str__(self):
        """Pretty-print configurations in alphabetical order"""
        config_str = 'Configurations\n'
        config_str += pprint.pformat(self.__dict__)
        return config_str
'''

class Config(object):
    def __init__(self, model, pos, checkpoint):
		
        setattr(self, 'optimizer', optim.Adam)
        setattr(self, 'rnn', nn.GRU)
        setattr(self, 'rnncell', StackedGRUCell)
        '''
        for key, value in kwargs.items():
                if key == 'optimizer':
                    value = optimizer_dict[value]
                if key == 'rnn':
                    value = rnn_dict[value]
                if key == 'rnncell':
                    value = rnncell_dict[value]
                setattr(self, key, value)
        '''
        self.morph = False
        setattr(self,'morph', False)
        self.model = 'VHRED'
        setattr(self,'model', 'VHRED')
        self.pos = pos
        setattr(self, 'pos', pos)
        self.checkpoint = checkpoint
        setattr(self, 'checkpoint', checkpoint)
        # Dataset directory: ex) ./datasets/cornell/
        if self.morph:
            if self.data.lower() =='kor':
                self.dataset_dir = data_dir.joinpath('korean-dialogs-morph-pkl')
            elif self.data.lower() =='servicelog':
                self.dataset_dir = data_dir.joinpath('servicelog-morph-pkl')
            elif self.data.lower() =='service+chatbot':
                self.dataset_dir = data_dir.joinpath('service-chat-morph-pkl')
            elif self.data.lower() =='all':
                self.dataset_dir = data_dir.joinpath('all-data-morph-pkl')
            elif self.data.lower() =='dasom2':
                self.dataset_dir = data_dir.joinpath('dasom2-morph-pkl')
        elif self.pos:
            self.dataset_dir = data_dir.joinpath('emotok_0723_chitchat_pos_pkl')
        else:
            self.dataset_dir = data_dict[self.data.lower()]

        self.word2id_path = self.dataset_dir.joinpath('word2id.pkl')
        self.id2word_path = self.dataset_dir.joinpath('id2word.pkl')
        self.sentences_path = self.dataset_dir.joinpath('sentences.pkl')
        self.sentence_length_path = self.dataset_dir.joinpath('sentence_length.pkl')
        self.conversation_length_path = self.dataset_dir.joinpath('conversation_length.pkl')

        self.mode = 'service'
        setattr(self, 'mode', 'service')
        self.batch_size=40
        setattr(self, 'batch_size', 40)
        self.eval_batch_size=80
        setattr(self, 'eval_batch_size', 80)
        #self.n_epoch = 80
        #setattr(self, 'n_epoch', 80)	
        self.n_epoch = 40
        setattr(self, 'n_epoch', 40)
        self.learning_rate = 0.0001
        setattr(self, 'learning_rate', 0.0001)
        self.optimizer = optim.Adam
        self.clip = 1.0
        setattr(self, 'clip', 1.0)
        self.data = 'emotok'
        setattr(self, 'data', 'emotok')
        self.max_unroll = 30
        setattr(self, 'max_unroll', 30)
        self.sample = False
        setattr(self, 'sample', False)
        self.temperature = 1.0
        setattr(self, 'temperature', 1.0)
        self.beam_size = 1
        setattr(self, 'beam_size', 1)
        self.rnn = nn.GRU
        self.rnncell = StackedGRUCell
        self.num_layers = 1
        setattr(self, 'num_layer', 1)
        self.tie_embedding = True
        setattr(self, 'tie_embedding', True)
        self.embedding_size = 1000
        setattr(self, 'embedding_size', 1000)
        self.encoder_hidden_size = 1000
        setattr(self, 'encoder_hidden_size', 1000)
        self.bidirectional = True
        setattr(self, 'bidirectional', True)
        self.decoder_hidden_size = 1000
        setattr(self, 'decoder_hidden_size', 1000)
        self.dropout=0.2
        setattr(self, 'dropout', 0.2)
        self.context_size = 1000
        setattr(self, 'context_size', 1000)
        self.feedforward = 'FeedForward'
        setattr(self, 'feedforward', 'FeedForward')
        self.activation = 'Tanh'
        setattr(self, 'activation', 'Tanh')
        self.z_sent_size = 100
        setattr(self, 'z_sent_size', 100)
        self.z_conv_size = 100
        setattr(self, 'z_conv_size', 100)
        self.word_drop = 0.25
        setattr(self, 'word_drop', 0.25)
        self.kl_threshold = 0.0
        setattr(self, 'kl_threshold', 0.0)
        self.kl_annealing_iter = 25000
        setattr(self, 'kl_annealing_iter', 25000)
        self.importance_sample = 100
        setattr(self, 'importance_sample', 100)
        self.sentence_drop = 0.25
        setattr(self, 'sentence_drop', 0.25)
        self.n_context = 1
        setattr(self, 'n_context', 1)
        self.n_sample_step = 1
        setattr(self, 'n_sample_step', 1)
        self.bow = False
        setattr(self, 'bow', False)
        self.print_every = 100
        setattr(self, 'print_every', 100)
        self.plot_every_epoch = 1
        setattr(self, 'plot_every_epoch', 1)
        self.save_every_epoch = 10
        setattr(self, 'save_every_epoch', 10)
    

'''
def get_config(parse=True, **optional_kwargs):
    parser = argparse.ArgumentParser()

    # Mode
    parser.add_argument('--mode', type=str, default='service')
 
    # Added for Korean Morpheme
    parser.add_argument('--morph', type=bool, default=False)
    parser.add_argument('--pos', type=bool, default=False)

    # Data
    parser.add_argument('--data', type=str, default='dasom2')

	# Model
    parser.add_argument('--model', type=str, default='HRED',
                        help='one of {HRED, VHRED, VHCR}')

    # Train
    parser.add_argument('--batch_size', type=int, default=40)
    parser.add_argument('--eval_batch_size', type=int, default=80)
    parser.add_argument('--n_epoch', type=int, default=30)
    parser.add_argument('--learning_rate', type=float, default=1e-4)
    parser.add_argument('--optimizer', type=str, default='Adam')
    parser.add_argument('--clip', type=float, default=1.0)
    parser.add_argument('--checkpoint', type=str, default=None)

    # Generation
    parser.add_argument('--max_unroll', type=int, default=30)
    parser.add_argument('--sample', type=str2bool, default=False,
                        help='if false, use beam search for decoding')
    parser.add_argument('--temperature', type=float, default=1.0)
    parser.add_argument('--beam_size', type=int, default=1)

    # Currently does not support lstm
    parser.add_argument('--rnn', type=str, default='gru')
    parser.add_argument('--rnncell', type=str, default='gru')
    parser.add_argument('--num_layers', type=int, default=1)
    parser.add_argument('--embedding_size', type=int, default=1000)
    parser.add_argument('--tie_embedding', type=str2bool, default=True)
    parser.add_argument('--encoder_hidden_size', type=int, default=1000)
    parser.add_argument('--bidirectional', type=str2bool, default=True)
    parser.add_argument('--decoder_hidden_size', type=int, default=1000)
    parser.add_argument('--dropout', type=float, default=0.2)
    parser.add_argument('--context_size', type=int, default=1000)
    parser.add_argument('--feedforward', type=str, default='FeedForward')
    parser.add_argument('--activation', type=str, default='Tanh')

    # VAE model
    parser.add_argument('--z_sent_size', type=int, default=100)
    parser.add_argument('--z_conv_size', type=int, default=100)
    parser.add_argument('--word_drop', type=float, default=0.25,
                        help='only applied to variational models')
    parser.add_argument('--kl_threshold', type=float, default=0.0)
    parser.add_argument('--kl_annealing_iter', type=int, default=250000)
    parser.add_argument('--importance_sample', type=int, default=100)
    parser.add_argument('--sentence_drop', type=float, default=0.25)

    # Generation
    parser.add_argument('--n_context', type=int, default=1)
    parser.add_argument('--n_sample_step', type=int, default=1)

    # BOW
    parser.add_argument('--bow', type=str2bool, default=False)

    # Utility
    parser.add_argument('--print_every', type=int, default=100)
    parser.add_argument('--plot_every_epoch', type=int, default=1)
    parser.add_argument('--save_every_epoch', type=int, default=10)

       # Parse arguments
    if parse:
        kwargs = parser.parse_args()
    else:
        kwargs = parser.parse_known_args()[0]

    # Namespace => Dictionary
    kwargs = vars(kwargs)
    kwargs.update(optional_kwargs)

    return Config(**kwargs)
'''
