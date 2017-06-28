from nltk.corpus import brown
import operator

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
    def __init__(self, keep_words=SENTENCES_KEEP_WORDS):
        self.sentences = brown.sents()
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

    def limit(self, n_limit=500):
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

#sentences = Sentences()
#print(sentences.limit())
