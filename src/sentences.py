from nltk.corpus import brown
import operator
import numpy as np

SENTENCES_KEEP_WORDS=['king',
                      'man',
                      'queen',
                      'woman',
                      'italy',
                      'rome',
                      'france',
                      'paris',
                      'london',
                      'britain',
                      'england'
                     ]

class Sentences(object):
    def __init__(self, n_sentences=None, keep_words=SENTENCES_KEEP_WORDS):
        sentences = brown.sents()
        if n_sentences is None:
            self.sentences = sentences
        if n_sentences > len(sentences):
            self.sentences = sentences
        else:
            self.sentences = sentences[:n_sentences]
        self.keep_words = set(keep_words)
        self.indx_sent, self.word2idx, self.idx2word = self._build_idx()

    def _build_idx(self):
        indx_sents = []
        idx2word = ['START', 'END']
        word2idx = {'START' : 0,
                    'END' : 1
                   }
        idx = len(word2idx.keys())
        for sentence in self.sentences:
            indx_sent = []
            for token in sentence:
                token = token.lower()
                if token not in word2idx:
                    word2idx[token] = idx
                    idx2word.append(token)
                    idx += 1
                indx_sent.append(word2idx[token])
            indx_sents.append(indx_sent)
        assert len(set(idx2word)) == len(idx2word)
        return indx_sents, word2idx, idx2word

    def limit_vocab(self, n_limit=500):
        word2count = {word : 0 for word in self.word2idx.keys()}
        for sentence in self.indx_sent:
            for indx in sentence:
                word2count[self.idx2word[indx]] += 1
        word2count = sorted(word2count.items(),
                            key=operator.itemgetter(1),
                            reverse=True)
        word2idx_limit = {'START' : 0,
                          'END' : 1
                         }
        idx = len(word2idx_limit.keys())
        for word in self.keep_words:
            word2idx_limit[word] = idx
            idx += 1
        base_len = len(word2idx_limit.keys())
        for word_tuple in word2count[:n_limit-base_len]:
            word2idx_limit[word_tuple[0]] = idx
            idx += 1
        word2idx_limit['UNKNOWN'] = idx
        idx2word_limit = {val : key for key, val in word2idx_limit.items()}
        indx_sent_limit = []
        for sentence in self.indx_sent:
            if len(sentence) > 1:
                new_indx_sent = [word2idx_limit[self.idx2word[idx]]
                                 if self.idx2word[idx] in word2idx_limit.keys()
                                 else n_limit-1
                                 for idx in sentence]
                indx_sent_limit.append(new_indx_sent)
        return indx_sent_limit, word2idx_limit, idx2word_limit

    def train_test_split_bigram(self, train_percentage=0.8, n_limit=500):
        indx_sent, word2idx, idx2word = self.limit_vocab(n_limit=n_limit)
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

        return X_train, y_train, X_test, y_test

#sentences = Sentences()
#print(sentences.limit())
