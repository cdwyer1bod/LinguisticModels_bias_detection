import pandas as pd
import numpy as np
from nltk.tag import StanfordPOSTagger
from nltk.tokenize import word_tokenize
from nltk import pos_tag

text = 'While in France, Christine Lagarde discussed short-term stimulus efforts in a recent interview with the Wall Street Journal.'

def getPOStag(x):
    #takes row and extracts the raw text and returns list of POS tagged tupples
    text = x[8]
    if type(text) is str:
        tokenized_text = word_tokenize(text)
        return pos_tag(tokenized_text)
    else:
        raise ValueError("getPOStag requires a string for the first input")

def getPOSdata(taggedsent, index):
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

def get_bais_index(x):
    #Ineffecient to tokenize twice, write these functions in parallel
    tokenized_text = word_tokenize(x[8])
    try:
        return int(tokenized_text.index(x[6]))
    except:
        #TODO: remove punctuatuion from column 7 so that we dont have to drop these cases
        return None

def get_bais_tag(x, n):
    if not np.isnan(x['bais_index']):
        if (x['bais_index'] + n > 0) and (x['bais_index'] + n < len(x['tagged_sent'])):
            return x['tagged_sent'][int(x['bais_index'])][1]
    else:
        return None


def get_freqs(filename):
    data = pd.read_csv(filename, ",")
    data['bais_index'] = data.apply(get_bais_index, axis = 1)
    data['tagged_sent'] = data.apply(getPOStag, axis = 1)
    pos_freq_dists = {}
    for i in range(-2, 3):
        data['bais_tag'] = data.apply(get_bais_tag, n = i, axis = 1)
        pos_freq_dist = data['bais_tag'].value_counts()/len(data)
        pos_freq_dists[i] = pos_freq_dist/pos_freq_dist[0]
    word_freq_dist = data['7'].value_counts()/len(data)
    word_freq_dist = word_freq_dist/word_freq_dist[0]
    return pos_freq_dists, word_freq_dist.to_dict()

def vectorize_word(w, POS_FREQ_DIST):
    if w in POS_FREQ_DIST.keys():
        return POS_FREQ_DIST[w]
    else:
        return 0

def vectorize_pos_n(pos, n, POS_FREQ_DIST):
    if pos in POS_FREQ_DIST[n].keys():
        return POS_FREQ_DIST[n][pos]
    else:
        return 0

#TODO: save these FREQ... somewhere to save doing the comp every time
#      potentially when running big function include option to redo freq lists
POS_FREQ_DIST, WORD_FREQ_DIST = get_freqs("5gram-edits-test-sents-clean.csv")
print(type(WORD_FREQ_DIST))

