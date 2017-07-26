'''
Optional Skipgram model experiment
Section 2, Lecture 10

The machinery is correct, but the code would take a very long time to run.
You will see greater error AFTER training because it uses one-at-a-time
stochastic gradient descent.
'''
import numpy as np
from math import floor, isnan
from sentences import Sentences

def sigmoid(v,d=False):
    if d:
        return v*(1.0-v)
    return 1.0/(1.0+np.exp(-v))

def tanh(v,d=False):
    if d:
        return 1-v*v
    return 2*sigmoid(2*v)-1

def relu(v, d=False):
    if d:
        return 1.0 * (v > 0)
    return v * (v > 0)
    return np.maximum(v, 0, v)

def skipgram_model():
    np.random.seed(0)
    act = tanh
    context = 3
    vocab_limit = 500
    indx_sent, word2idx, idx2word = Sentences(n_sentences=5000).limit_vocab(n_limit=vocab_limit)
    skipgrams = [[] for i in range(vocab_limit)]
    for sentence in indx_sent:
        len_sent = len(sentence)
        for tidx, token in enumerate(sentence):
            bigram = []
            for step in range(1, context+1):
                if tidx + step < len_sent:
                    bigram.append(sentence[tidx+step])
                if tidx - step >= 0:
                    bigram.append(sentence[tidx-step])
            skipgrams[token].append(bigram)

    train_percentage = 0.8

    train_grams = [[] for i in range(vocab_limit)]
    n_train = 0
    test_grams = [[] for i in range(vocab_limit)]
    n_test = 0
    for sidx, skipgram in enumerate(skipgrams):
        skip_len = len(skipgram)
        if skip_len < 3:
            ValueError('Insufficient data for training and testing!')
        train_len = floor(train_percentage*skip_len)
        n_train += train_len
        n_test += skip_len - train_len
        train_grams[sidx].extend(skipgram[:train_len])
        test_grams[sidx].extend(skipgram[train_len:])

    # number based on:
    # https://stats.stackexchange.com/questions/181/how-to-choose-the-number-of-hidden-layers-and-nodes-in-a-feedforward-neural-netw
    n_hidden = round(n_train/(5*(vocab_limit + vocab_limit)))

    input_to_hidden = 2*np.random.random((vocab_limit, n_hidden)) - 1.0
    hidden_to_output = 2*np.random.random((n_hidden, vocab_limit)) - 1.0

    base_error = 0.0
    for tidx, token_skipgrams in enumerate(test_grams):
        guess = np.dot(input_to_hidden[tidx, :], hidden_to_output)
        for skipgram in token_skipgrams:
            iter_error = -guess
            iter_error[skipgram] += 1.0
            base_error += np.linalg.norm(tanh(iter_error))

    print('Base L2 error: %s' % str(base_error))

    n_epoch = 10
    alpha = 1.0
    # this implements one-at-a-time stochastic gradient descent
    for epoch in range(n_epoch):
        for tidx, token_skipgrams in enumerate(train_grams):
            for skipgram in token_skipgrams:
                # input is one-hot, so returns one column of input_to_hidden
                l1 = act(input_to_hidden[tidx, :])
                l2 = act(np.dot(l1, hidden_to_output))
                err_output_to_hidden = -l2
                # skipgram is a list
                err_output_to_hidden[skipgram] += 1.0
                d1 = err_output_to_hidden*act(l2,d=True)
                err_hidden_to_input = np.dot(d1, hidden_to_output.T)
                d0 = err_hidden_to_input*act(l1, d=True)
                hidden_to_output += alpha*np.outer(l1, d1)
                input_to_hidden[tidx, :] += alpha*d0
                ih_norm = np.linalg.norm(input_to_hidden[tidx, :])
                if(isnan(ih_norm)):
                    raise ValueError()

    test_error = 0.0
    for tidx, token_skipgrams in enumerate(test_grams):
        guess = np.dot(input_to_hidden[tidx, :], hidden_to_output)
        for skipgram in token_skipgrams:
            iter_error = -guess
            iter_error[skipgram] += 1.0
            test_error += np.linalg.norm(tanh(iter_error))

    print('Test L2 error: %s' % str(test_error))

if __name__ == "__main__":
    skipgram_model()
