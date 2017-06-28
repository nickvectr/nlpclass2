import numpy as np
import matplotlib.pyplot as plt

from sentences import Sentences

from sklearn.feature_extraction.text import TfidfTransformer as TFIDF
from sklearn.manifold import TSNE

def tfidf_tsne():
    indx_sent, word2idx, idx2word = Sentences().limit()

    word_sent_counts = np.zeros((len(word2idx)+1,len(indx_sent)+1))
    j = 0
    for sentence in indx_sent:
        for idx in sentence:
            word_sent_counts[idx, j] += 1
        j += 1

    word_sent_tfidf = TFIDF().fit_transform(word_sent_counts).toarray()
    word_sent_tsne = TSNE().fit_transform(word_sent_tfidf)

    plt.scatter(word_sent_tsne[:,0], word_sent_tsne[:,1])
    for label in range(len(word2idx)):
        try:
            plt.annotate(s=idx2word[label].encode('utf8'), xy=(word_sent_tsne[label,0], word_sent_tsne[label,1]))
        except UnicodeError:
            pass
        except KeyError:
            pass
    plt.show()

tfidf_tsne()
