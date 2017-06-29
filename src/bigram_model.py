'''
Optional Bigram model experiment
Section 2, Lecture 9
'''
import numpy as np

from sentences import Sentences

from sklearn.linear_model import LogisticRegression

def bigram_model():
    indx_sent, word2idx, idx2word = Sentences(n_sentences=1000).limit_vocab()
    train_percentage = 0.8

    n_vocab = len(word2idx.keys())+1

    n_sentence = len(indx_sent)
    n_train_sentence = round(n_sentence*train_percentage)
    n_test_sentence = n_sentence - n_train_sentence

    # TRAIN
    train_sentence = indx_sent[:n_train_sentence]
    n_train_word = sum(len(sentence)-1 for sentence in train_sentence)
    X_train = np.zeros((n_vocab, n_train_word))
    y_train = np.zeros(n_train_word)
    j = 0
    for sentence in train_sentence:
        for idx in range(len(sentence)-1):
            X_train[sentence[idx], j] = 1
            y_train[j] = sentence[idx+1]
            j += 1

    model = LogisticRegression()
    model.fit(X_train.transpose(), y_train)

    # TEST
    test_sentence = indx_sent[n_train_sentence:]
    n_test_word = sum(len(sentence)-1 for sentence in test_sentence)
    X_test = np.zeros((n_vocab, n_test_word))
    y_test = np.zeros(n_test_word)
    j = 0
    for sentence in test_sentence:
        for idx in range(len(sentence)-1):
            X_test[sentence[idx], j] = 1
            y_test[j] = sentence[idx+1]
            j += 1

    print("Bigram model test accuracy: %f" % model.score(X_test.transpose(), y_test))

bigram_model()
