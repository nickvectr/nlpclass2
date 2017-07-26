'''
Optional Bigram model experiment
Section 2, Lecture 9
'''
import numpy as np

from sentences import Sentences

from sklearn.linear_model import LogisticRegression

def bigram_model():
    X_train, y_train, X_test, y_test = Sentences(n_sentences=1000).train_test_split_bigram()
    model = LogisticRegression()
    model.fit(X_train.transpose(), y_train)
    print("Bigram model test accuracy: %f" % model.score(X_test.transpose(), y_test))

if __name__ == "__main__":
    bigram_model()
