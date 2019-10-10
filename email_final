import pyLDAvis
import pyLDAvis.gensim
import matplotlib.pyplot as plt
import pandas as pd
#emails = pd.read_csv('data/mail-body-CSV.csv',skiprows=2)
#print("emails at start",emails.loc[[0]])
from google.cloud import bigquery
import json

client = bigquery.Client()
query_job = client.query("""
        SELECT Corps
        FROM `paris-ilab.paris-pune-hackathon.mails`
        LIMIT 1000""")

emails = query_job.result()  # Waits for job to complete.
for row in emails:
    print(row.DeNom)
    print(row.ANom)


def parse_raw_message(raw_message):
    print("each msg is",raw_message)
    lines = raw_message.split('\n')
    print("lines is",lines)
    email = {}
    message = ''
    for line in lines:
            message += line.strip()
            email['body'] = message
    return email


def parse_into_emails(emails):
    emails_new=[]
    for index,row in emails.iterrows():
        print("each row",index,row)
        # emails_new.append(parse_raw_message(emails[[index]]))
    print("emails are",emails_new)
    return {
        'body': emails
    }

email_df = pd.DataFrame(parse_into_emails(emails))
print("HEAD OF EMAIL",email_df,email_df.head())

import re
import numpy as np
import gensim
import gensim.corpora as corpora
from gensim.utils import simple_preprocess
from gensim.models import CoherenceModel
# spacy for lemmatization
import spacy
# for plotting
# import pyLDAvis
# import pyLDAvis.gensim
import matplotlib.pyplot as plt
#  >>> import nltk
#  >>> nltk.download('stopwords')
# prep NLTK Stop words
from nltk.corpus import stopwords
stop_words = stopwords.words('french')
stop_words.extend(['from', 'subject', 're', 'edu', 'use'])




# Convert email body to list
print("email_df",email_df.body)
data = email_df.body.values.tolist()
print("data is",data)
# tokenize - break down each sentence into a list of words
def sent_to_words(sentences):
    for sentence in sentences:
        yield(gensim.utils.simple_preprocess(str(sentence), deacc=True))  # deacc=True removes punctuations
data_words = list(sent_to_words(data))
print(data_words[0])

from gensim.models.phrases import Phrases, Phraser
# Build the bigram and trigram models
bigram = Phrases(data_words, min_count=5, threshold=100) # higher threshold fewer phrases.
trigram = Phrases(bigram[data_words], threshold=100)


# Faster way to get a sentence clubbed as a trigram/bigram
bigram_mod = Phraser(bigram)
trigram_mod = Phraser(trigram)
# See trigram example
# print(trigram_mod[bigram_mod[data_words[200]]])


# remove stop_words, make bigrams and lemmatize
def remove_stopwords(texts):
    return [[word for word in simple_preprocess(str(doc)) if word not in stop_words] for doc in texts]

def make_bigrams(texts):
    return [bigram_mod[doc] for doc in texts]

def make_trigrams(texts):
    return [trigram_mod[bigram_mod[doc]] for doc in texts]

def lemmatization(texts, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV']):
    """https://spacy.io/api/annotation"""
    texts_out = []
    for sent in texts:
        doc = nlp(" ".join(sent))
        texts_out.append([token.lemma_ for token in doc if token.pos_ in allowed_postags])
    return texts_out


# Remove Stop Words
data_words_nostops = remove_stopwords(data_words)
# Form Bigrams
data_words_bigrams = make_bigrams(data_words_nostops)
#python -m spacy download en
# Initialize spacy 'en' model, keeping only tagger component (for efficiency)
nlp = spacy.load('fr_core_news_sm', disable=['parser', 'ner'])
# Do lemmatization keeping only noun, adj, vb, adv
data_lemmatized = lemmatization(data_words_bigrams, allowed_postags=['NOUN', 'ADJ', 'VERB', 'ADV'])
print("data lemmatized is",data_lemmatized)


# create dictionary and corpus both are needed for (LDA) topic modeling

# Create Dictionary
id2word = corpora.Dictionary(data_lemmatized)

# Create Corpus
texts = data_lemmatized

# Term Document Frequency
corpus = [id2word.doc2bow(text) for text in texts]


# Build LDA model
lda_model = gensim.models.ldamodel.LdaModel(corpus=corpus,
                                           id2word=id2word,
                                           num_topics=20,
                                           random_state=100,
                                           update_every=1,
                                           chunksize=100,
                                           passes=10,
                                           alpha='auto',
                                           per_word_topics=True)

from sklearn.externals import joblib

# Save the model as a pickle in a file
joblib.dump(lda_model, 'lda_model.pkl')

# Load the model from the file
lda_model = joblib.load('lda_model.pkl')
print(lda_model.print_topics())# The weights reflect how important a keyword is to that topic.

doc_lda = lda_model[corpus]
# Model perplexity and topic coherence provide a convenient
# measure to judge how good a given topic model is.
# Compute Perplexity
print('\nPerplexity: ', lda_model.log_perplexity(corpus))  # a measure of how good the model is. lower the better.

# Compute Coherence Score
coherence_model_lda = CoherenceModel(model=lda_model, texts=data_lemmatized, dictionary=id2word, coherence='c_v')
coherence_lda = coherence_model_lda.get_coherence()
print('\nCoherence Score: ', coherence_lda)

# Visualize the topics
pyLDAvis.enable_notebook(sort=True)
vis = pyLDAvis.gensim.prepare(lda_model, corpus, id2word)
pyLDAvis.display(vis)
