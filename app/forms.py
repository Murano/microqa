# -*- coding: utf-8 -*-

from flask import flash
from flask_wtf import Form
from wtforms import StringField, TextAreaField, PasswordField, TextField
from model import User
from wtforms.validators import DataRequired, ValidationError

class QuestionForm(Form):
    title = StringField(u"Заголовок вопроса", validators=[DataRequired()])
    body = TextAreaField(u"Тело вопроса", validators=[DataRequired()])
    tags = StringField(u"Тэги (через запятую)", validators=[DataRequired()])

class CommentForm(Form):
    body = TextAreaField(u"Ответ", validators=[DataRequired()])

class LoginForm(Form):
    username = StringField(u"Логин", validators=[DataRequired()])
    password = PasswordField(u"Пароль", validators=[DataRequired()])

    def validate_username(self, field):
        user = self.get_user()

        if user is None:
            raise ValidationError(u'Неверное имя пользователя')

        if user.password != self.password.data:
            raise ValidationError(u'Неверный пароль')

    def get_user(self):
        return User.objects(username=self.username.data).first()

class RegistrationForm(Form):
    username = TextField(u"Логин", validators=[DataRequired()])
    email = TextField(u"E-mail", validators=[DataRequired()] ) # TODO: validate
    password = PasswordField(u"Пароль", validators=[DataRequired()])

    def validate_username(self, field):
        if User.objects(username=self.username.data):
            raise ValidationError(u'Такой логин уже занят')

    def validate_email(self, field):
        if User.objects(email=self.email.data):
            raise ValidationError(u'Такой email адрес уже существует')