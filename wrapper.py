import pandas as pd
from vectorize import get_pos_tag, vectorize_word, vectorize_pos_n, get_freqs
from Logistic_Model_Tester import isInList

def data_stripper(arr):
    new_data = arr[:]
    new_data.columns = ['Bias Inducing Word','De-Biased Word','Sentence Pre-Edit','Sentence Post-Edit']
    return new_data[['Bias Inducing Word','Sentence Pre-Edit']]

def vectorize_df(df, POS_FREQ_DIST, WORD_FREQ_DIST):
    df['tagged_sent'] = df.apply(get_pos_tag, axis = 1) 
    attiribute_matrix = []
    result_vector = []
    for row in df.index:
        # TODO: this definition of word may not match definition in 'Bias Inducing Word'
        for pair in df['tagged_sent'].iloc[row]:
            current_vector = []
            current_vector.append(vectorize_word(pair[0], WORD_FREQ_DIST))
            for n in range(-1,2):
                current_vector.append(vectorize_pos_n(pair[1], n, POS_FREQ_DIST))
            print(current_vector, "\n") 
    return


POS_FREQ_DIST, WORD_FREQ_DIST = get_freqs("./final_datasets/train-sents-final1.csv")

train_alldata = pd.read_csv("./final_datasets/train-sents-final1.csv")
train_data = data_stripper(train_alldata.head())
print(train_data)
vectorize_df(train_data, POS_FREQ_DIST, WORD_FREQ_DIST)
