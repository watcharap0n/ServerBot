""":param

x_test = ['สวัสดีครับเป็นอย่างไรบ้าง', 'ชื่ออะไรหรออยากสอบถาม', 'สอบถามหน่อยครับพอดีสนใจตัวโปรแกรม', 'ทำอะไรได้บ้างมีแผนว่าจะทำอะไรหะ',
          'โปรแกรมทำอะไรได้บ้าแล้วมีประโยชน์ในการทำอะไร', 'โปรแกรมเหมาะธุรกิจอะรฟ', 'คิดราคาอย่าไร', 'บริการหลังจากลูกค้าซื้อไปแล้ว']
x = [
     'สวัสดีครับ ทักทายหน่อย สวัสดีเป็นอย่างไรบ้าง กล่าวทักทายหน่อย สวัสดีสอบถามหน่อย สวัสดี',
     'ชื่ออะไร เธอมีชื่อว่าอะไรครับ แนะนำตัวหน่อย แนะนำตัว บอกชื่อเธอมา มีชื่อว่าอะไร',
     'อยากสอบถาม สอบถามเกี่ยวกับโปรแกรมหน่อย สอบถามปัญหาต่างๆ สอบถามหน่อยได้ไหม สอบถามหน่อย สอบถาม',
     'ทำอะไรอยู่ ทำไรครับ ทำอะไรเป็นอย่างไรบ้าง ทำอะไรเอ่ย ทำไร',
     'โปรแกรมทำอะไรได้บ้าง อยากรู้เรื่องโปรแกรม มีความสนใจตัวโปรแกรม สนใจตัวโปรแกรมครับผม แนะนำตัวโปรแกรมหน่อย ช่วยแนะนำตัวโปรแกรมหน่อย มีความอยากรู้เรื่องโปรแกรม',
     'โปรแกรมเหมาะกับธุรกิจอะไร โปรแกรมเหมาะกับธรุกิจประเภทไหน',
     'โปรแกรมคิดค่าบริการอย่างไร คิดค่าบริการอย่าง โปรแกรมราคาเท่าไหร่ ราคาของโปรแกรม ราคาที่สนใจ ราคาเป็นอย่างไรบ้าง',
     'บริการหลังการขาย หลังการขายของลูกค้า หลังการขาย หลังการขายเป็นอย่างไรบ้าง',

     ]
y = [['สวัสดีครับ :)', 'สวัสดีครับ'],
     ['ชื่อบอทแมงโก้', 'ชื่อบอทจ้าาา'],
     ['ยินดีให้บริการครับ สอบถามได้เลย', 'สอบถามมาได้เลย'],
     ['กำลังให้บริการสอบถามปัญหาครับ']

"""

import re
import numpy as np
from pydantic import BaseModel
from typing import Optional, Any, List
from attacut import tokenize
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import TfidfVectorizer, CountVectorizer, TfidfTransformer


class Engine(BaseModel):
    predicted: Optional[Any] = None
    confidence: Optional[Any] = None
    answers: Optional[list]
    name: Optional[str] = None
    card: Optional[str] = None
    ready: Optional[bool]
    id: Optional[str]
    status_flex: Optional[bool]
    require: Optional[str] = None


async def chatbot_pipeline(
        X: list,
        y: list,
        db: list,
        message: str,
        answers: list,
        X_test: Optional[list] = None) -> object:
    """

    :param message:
    :param answers:
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
    intent = db[predicted[0]]
    return Engine(
        predicted=predicted,
        answers=answers,
        name=intent.get('name'),
        card=intent.get('card'),
        ready=intent.get('ready'),
        id=intent.get('_id'),
        status_flex=intent.get('status_flex')
    )


async def chatbot_standard(
        X: list,
        y: list,
        db: list,
        answers: list,
        message: str,
        X_test: Optional[list] = None) -> object:
    """
    :param db:
    :param answers
    :param message:
    :param X:
    :param y:
    :param X_test:
    :return:
    """

    if len(X) == 1 and len(answers) == 1:
        return Engine(require='ต้องสร้าง Intent อย่างน้อย 2 Intent ก่อนถึงจะสามารถใช้งานบอทได้ครับ')
    X = [re.sub(re.compile(r'\s+'), '', i) for i in X]
    tf_vect = CountVectorizer(tokenizer=tokenize)
    x_train_vect = tf_vect.fit_transform(X)
    clf = LogisticRegression(penalty='none')
    clf.fit(x_train_vect, y)
    x_test_vect = tf_vect.transform([message])
    if X_test:
        predicted = clf.predict(x_test_vect)
        pred_proba = clf.predict_proba(x_test_vect)[0][predicted]
        acc = np.mean(predicted == y)
        return {'accuracy': acc, 'pred_prob': pred_proba,
                'predicted': predicted}
    predicted = clf.predict(x_test_vect)
    pred_proba = clf.predict_proba(x_test_vect)[0][predicted]
    intent = db[predicted[0]]
    return Engine(
        predicted=predicted,
        confidence=pred_proba,
        answers=answers,
        name=intent.get('name'),
        card=intent.get('card'),
        ready=intent.get('ready'),
        id=intent.get('_id'),
        status_flex=intent.get('status_flex')
    )


async def intent_model(
        X: list,
        y: list,
        db: list,
        answers: list,
        message: str,
) -> object:
    """
        :param
    """

    if len(X) == 1 and len(answers) == 1:
        return Engine(require='ต้องสร้าง Intent อย่างน้อย 2 Intent ก่อนถึงจะสามารถใช้งานบอทได้ครับ')
    sum_text = [re.sub(re.compile(r'\s+'), '', i) for i in X]
    tf_vect = TfidfVectorizer(tokenizer=tokenize)
    x_train_vect = tf_vect.fit_transform(sum_text)
    my_classifire = LogisticRegression(penalty='none')
    my_classifire.fit(x_train_vect, y)
    x_test_vect = tf_vect.transform([message])
    predicted = my_classifire.predict(x_test_vect)
    pred_proba = my_classifire.predict_proba(x_test_vect)[0][predicted]
    intent = db[predicted[0]]
    return Engine(
        predicted=predicted,
        confidence=pred_proba,
        answers=answers,
        name=intent.get('name'),
        card=intent.get('card'),
        ready=intent.get('ready'),
        id=intent.get('_id'),
        status_flex=intent.get('status_flex')
    )
