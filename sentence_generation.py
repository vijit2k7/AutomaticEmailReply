from __future__ import print_function
from keras.models import Sequential, Model
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, Input, Flatten, Bidirectional
from keras.layers.normalization import BatchNormalization
from keras.optimizers import Adam
from keras.callbacks import EarlyStopping, ModelCheckpoint
from keras.metrics import categorical_accuracy
import numpy as np
import random
import sys
import os
import time
import codecs
import collections
from six.moves import cPickle

#import spacy, and french model
import spacy
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
nlp = spacy.load('fr_core_news_sm')

data_dir = 'data/Artistes_et_Phalanges-David_Campion'# data directory containing input.txt
save_dir = 'save' # directory to store models
seq_length = 30 # sequence length
sequences_step = 1 #step to create sequences

file_list = ["101","102","103","104","105","106","107","108","109","110","111","112","201","202","203","204","205","206","207","208","209","210","211","212","213","214","301","302","303","304","305","306","307","308","309","310","311","312","313","314","401","402","403","404","405","406","407","408","409","410","411","412"]
vocab_file = os.path.join(save_dir, "words_vocab.pkl")

def create_wordlist(doc):
    wl = []
    for word in doc:
        if word.text not in ("\n","\n\n",'\u2009','\xa0'):
            wl.append(word.text.lower())
    return wl

wordlist = []
for file_name in file_list:
    input_file = os.path.join(data_dir, file_name + ".txt")
    #read data
    with codecs.open(input_file, "r",'cp850') as f:
        data = f.read()
    #create sentences
    doc = nlp(data)
    wl = create_wordlist(doc)
    wordlist = wordlist + wl


# count the number of words
word_counts = collections.Counter(wordlist)

# Mapping from index to word : that's the vocabulary
vocabulary_inv = [x[0] for x in word_counts.most_common()]
vocabulary_inv = list(sorted(vocabulary_inv))

# Mapping from word to index
vocab = {x: i for i, x in enumerate(vocabulary_inv)}
words = [x[0] for x in word_counts.most_common()]

#size of the vocabulary
vocab_size = len(words)
print("vocab size: ", vocab_size)

#save the words and vocabulary
with open(os.path.join(vocab_file), 'wb') as f:
    print("file is",f)
    cPickle.dump((words, vocab, vocabulary_inv), f)


#create sequences
sequences = []
next_words = []
# for i in range(0, len(wordlist) - seq_length, sequences_step):
#     sequences.append(wordlist[i: i + seq_length])
#     next_words.append(wordlist[i + seq_length])
#
# print('nb sequences:', len(sequences),seq_length,vocab_size)
#
#
# def split_list(alist, wanted_parts=1):
#     length = len(alist)
#     return [alist[i*length // wanted_parts: (i+1)*length // wanted_parts]
#              for i in range(wanted_parts)]
#
#
# list_sequences = list(split_list(sequences,10))
# print("len of B,C is",len(list_sequences[0]),len(list_sequences[1]))
# X = np.zeros((len(list_sequences[0]), seq_length, vocab_size), dtype=np.bool)
# y = np.zeros((len(list_sequences[0]), vocab_size), dtype=np.bool)
# for i, sentence in enumerate(list_sequences[0]):
#     for t, word in enumerate(sentence):
#         X[i, t, vocab[word]] = 1
#     y[i, vocab[next_words[i]]] = 1


#building the model using LSTM
def bidirectional_lstm_model(seq_length, vocab_size):
    print('Build LSTM model.')
    model = Sequential()
    model.add(Bidirectional(LSTM(rnn_size, activation="relu"), input_shape=(seq_length, vocab_size)))
    model.add(Dropout(0.6))
    model.add(Dense(vocab_size))
    model.add(Activation('softmax'))

    optimizer = Adam(lr=learning_rate)
    callbacks = [EarlyStopping(patience=2, monitor='val_loss')]
    model.compile(loss='categorical_crossentropy', optimizer=optimizer, metrics=[categorical_accuracy])
    return model

# rnn_size = 64 # size of RNN
# batch_size = 64 # minibatch size
# seq_length = 30 # sequence length
# num_epochs = 6 # number of epochs
# learning_rate = 0.001 #learning rate
# sequences_step = 1 #step to create sequences
# md = bidirectional_lstm_model(seq_length, vocab_size)
# md.summary()

# #fit the model
# callbacks=[EarlyStopping(patience=4, monitor='val_loss'),
#            ModelCheckpoint(filepath=save_dir + "/" + 'my_model_gen_sentences_lstm.{epoch:02d}-{val_loss:.2f}.hdf5',
#                            monitor='val_loss', verbose=0, mode='auto', period=2)]
# history = md.fit(X, y,
#                  batch_size=batch_size,
#                  shuffle=True,
#                  epochs=num_epochs,
#                  callbacks=callbacks,
#                  validation_split=0.01)
#
# #save the model
# md.save(save_dir + "/" + 'my_model_gen_sentences_lstm.final.hdf5')

#load vocabulary
print("loading vocabulary...")
vocab_file = os.path.join(save_dir, "words_vocab.pkl")

with open(os.path.join(save_dir, 'words_vocab.pkl'), 'rb') as f:
        words, vocab, vocabulary_inv = cPickle.load(f)

vocab_size = len(words)

from keras.models import load_model
# load the model
print("loading model...")
model = load_model(save_dir + "/" + 'my_model_gen_sentences_lstm.final.hdf5')

#sampling and using temperature to smooth its value

def sample(preds, temperature=1.0):
    # helper function to sample an index from a probability array
    preds = np.asarray(preds).astype('float64')
    preds = np.log(preds) / temperature
    exp_preds = np.exp(preds)
    preds = exp_preds / np.sum(exp_preds)
    probas = np.random.multinomial(1, preds, 1)
    return np.argmax(probas)


#initiate sentences
seed_sentences = "nolan avance sur le chemin de pierre et grimpe les marches ."
generated = ''
sentence = []
for i in range (seq_length):
    sentence.append("a")

seed = seed_sentences.split()

for i in range(len(seed)):
    sentence[seq_length-i-1]=seed[len(seed)-i-1]

generated += ' '.join(sentence)
print('Generating text with the following seed: "' + ' '.join(sentence) + '"')

words_number = 100
#generate the text
for i in range(words_number):
    #create the vector
    x = np.zeros((1, seq_length, vocab_size))
    for t, word in enumerate(sentence):
        x[0, t, vocab[word]] = 1.
    #print(x.shape)

    #calculate next word
    preds = model.predict(x, verbose=0)[0]
    next_index = sample(preds, 0.34)
    next_word = vocabulary_inv[next_index]

    #add the next word to the text
    generated += " " + next_word
    # shift the sentence by one, and and the next word at its end
    sentence = sentence[1:] + [next_word]

print(generated)