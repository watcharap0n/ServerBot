import re
import numpy as np
import pandas as pd
from typing import Optional
from attacut import tokenize
from sklearn.model_selection import GridSearchCV
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.linear_model import SGDClassifier
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer


def chatbot_pipeline(X: list, y: list,
                     message: str,
                     X_test: Optional[list] = None) -> dict:
    """

    :param message:
    :param X:
    :param y:
    :param X_test:
    :return:
    """

    X = [re.sub(re.compile(r'\s+'), '', i) for i in X]
    text_clf_logis = Pipeline([('vect', CountVectorizer(tokenizer=tokenize)),
                               ('tfidf', TfidfTransformer()),
                               ('clf-svm', LogisticRegression()),
                               ])
    text_clf_logis.fit(X, y)
    if X_test:
        predicted = text_clf_logis.predict(X_test)
        pred_prob = text_clf_logis.predict_proba(X_test)
        acc = np.mean(predicted == y)
        return {'accuracy': acc, 'pred_prob': pred_prob,
                'predicted': predicted}
    message = list(message)
    predicted = text_clf_logis.predict(message)
    return {'predicted': predicted}


def chatbot_standard(X: list, y: list,
                     message: str,
                     X_test: Optional[list] = None) -> dict:
    """

    :param message:
    :param X:
    :param y:
    :param X_test:
    :return:
    """

    X = [re.sub(re.compile(r'\s+'), '', i) for i in X]
    tf_vect = CountVectorizer(tokenizer=tokenize)
    x_train_vect = tf_vect.fit_transform(X)
    clf = LogisticRegression(penalty='none')
    clf.fit(x_train_vect, y)
    message = list(message)
    x_test_vect = tf_vect.transform(message)
    if X_test:
        predicted = clf.predict(x_test_vect)
        pred_prob = clf.predict_proba(x_test_vect)[0][predicted]
        acc = np.mean(predicted == y)
        return {'accuracy': acc, 'pred_prob': pred_prob,
                'predicted': predicted}
    predicted = clf.predict(x_test_vect)
    return {'predicted': predicted}
