import pandas as pd
import numpy as np
from collections import defaultdict
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag

text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'
columns = ["Bias Inducing Word", "De-Biased Word", "Sentence Pre-Edit", "Sentence Post-Edit"]

def get_pos_tag(x):
    #takes row and extracts the raw text and returns list of POS tagged tupples
    text = x['Sentence Pre-Edit']
    if type(text) is str:
        tokenized_text = word_tokenize(text)
        return pos_tag(tokenized_text)
    else:
        raise ValueError("get_pos_tag requires a string for the first input")

def get_POS_data(taggedsent, index):
    # Takes a tagged sent and the index of the word to be vectorized
    # If POS +/- N is out of range returns None
    POSdata = []
    Ns = range(-2,3)
    for N in Ns:
        if (index + N > 0) and (index + N < len(taggedsent)):
            POSdata.append(taggedsent[index+N][1])
        else:
            POSdata.append(None)
    return POSdata

def get_bias_index(x):
    #Ineffecient to tokenize twice, write these functions in parallel
    tokenized_text = word_tokenize(x['Sentence Pre-Edit'])
    try:
        return int(tokenized_text.index(x['Bias Inducing Word']))
    except:
        #TODO: remove punctuatuion from column 7 so that we dont have to drop these cases
        return None

def get_bias_tag(x, n):
    if not np.isnan(x['bias_index']):
        if (x['bias_index'] + n > 0) and (x['bias_index'] + n < len(x['tagged_sent'])):
            return x['tagged_sent'][int(x['bias_index'])][1]
    else:
        return None

def get_corpus_freqs(df):
    # Gets the number of times each word and tag appears in the corpus and
    # returns then in two dicts
    tags_freq = defaultdict(float)
    words_freq = defaultdict(float)
    for row in df['tagged_sent'].values:
        for pair in row:
            tags_freq[pair[1]]+=1.0
    for row in df['Sentence Pre-Edit'].values:
        for word in row.split(' '):
            words_freq[word]+=1.0
    return tags_freq, words_freq

def get_freqs(filename):
    # Returns two dictionaries, giving the freq dist of each known bais word
    # and POS + n
    # Freq is defined as # bias cases of word/tag / # cases in corpus of word/tag
    data = pd.read_csv(filename, ",")
    data.columns = columns
    data['bias_index'] = data.apply(get_bias_index, axis = 1)
    data['tagged_sent'] = data.apply(get_pos_tag, axis = 1)
    tags_freq, words_freq = get_corpus_freqs(data)
    pos_freq_dists = {}
    for i in range(-2, 3):
        data['bias_tag'] = data.apply(get_bias_tag, n = i, axis = 1)
        pos_freq_dist = data['bias_tag'].value_counts().astype(float)
        for index in pos_freq_dist.index:
            pos_freq_dist[index] = pos_freq_dist[index]/tags_freq[index]
        pos_freq_dists[i] = pos_freq_dist/max(pos_freq_dist)
    word_freq_dist = data['Bias Inducing Word'].value_counts().astype(float)
    for index in word_freq_dist.index:
        try:
            word_freq_dist[index] = float(float(word_freq_dist[index])/float(words_freq[index]))
        except:
            del word_freq_dist[index]
    word_freq_dist = word_freq_dist/max(word_freq_dist)
    return pos_freq_dists, word_freq_dist.to_dict()

def vectorize_word(w, WORD_FREQ_DIST):
    if w in WORD_FREQ_DIST.keys():
        return WORD_FREQ_DIST[w]
    else:
        return 0

def vectorize_pos_n(pos, n, POS_FREQ_DIST):
    if pos in POS_FREQ_DIST[n].keys():
        return POS_FREQ_DIST[n][pos]
    else:
        return 0

#TODO: save these FREQ... somewhere to save doing the comp every time
#      potentially when running big function include option to redo freq lists


POS_FREQ_DIST, WORD_FREQ_DIST = get_freqs("./final_datasets/train-sents-final1.csv")
#print(WORD_FREQ_DIST)
#print(POS_FREQ_DIST)
