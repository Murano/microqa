# -*- coding: utf-8 -*-

from flask_wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import DataRequired

class QuestionForm(Form):
    username = StringField(u"Имя", validators=[DataRequired()])
    title = StringField(u"Заголово вопроса", validators=[DataRequired()])
    body = TextAreaField(u"Тело вопроса", validators=[DataRequired()])
    tags = StringField(u"Тэги (через запятую)", validators=[DataRequired()])

class CommentForm(Form):
    username = StringField(u"Имя", validators=[DataRequired()])
    body = TextAreaField(u"Ответ", validators=[DataRequired()])