# -*- coding: utf-8 -*-

from flask import render_template, redirect, url_for, request, flash

from app import app
from helpers import flash_errors
from forms import QuestionForm, CommentForm, LoginForm, RegistrationForm
from model import Question, Comment, Tag, User
from flask.ext.login import login_user, logout_user, current_user, login_required

@app.route('/')
def index():
    questions = Question.objects.order_by("-timestamp")
    return render_template("index.html", questions=questions)

@app.route("/question/add/", methods=["GET", "POST"])
@login_required
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        title = form.title.data
        body = form.body.data
        tags = form.tags.data
        if tags != "":
            tags = set(map(lambda x: x.strip(), tags.split(",")))
            tag_obj = Tag.objects.get_or_create()[0]
            for tag in tags:
                tag_obj.update(add_to_set__tags=tag)
            tag_obj.save()
        else:
            tags = []
        question = Question(username=current_user.username, title=title, body=body, tags=tags)
        question.save()
        return redirect(url_for("index"))
    return render_template("add_question.html", form=form)

@app.route("/question/<question_id>", methods=["GET", "POST"])
def question(question_id):
    question = Question.objects.get(id=question_id)
    form = CommentForm()
    if current_user.is_authenticated():
        if form.validate_on_submit():
            body = form.body.data
            comment = Comment(username=current_user.username, body=body)
            question.update(add_to_set__comments=comment)
            question.save()
            return redirect("/question/%s" % question_id)
    return render_template('question.html', question=question, form=form)

@app.route('/register', methods=('GET', 'POST'))
def register():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        user = User()
        form.populate_obj(user)
        user.save()
        login_user(user)
        return redirect(url_for('index'))
    else:
        flash_errors(form)
    return render_template('register.html', form=form)


@app.route('/tag/<tag>')
def tag(tag):
    questions = Question.objects(tags=tag).order_by("-timestamp")
    return render_template('tag.html', questions=questions, tag=tag)


@app.route('/tags')
def tags():
    tags = Tag.objects.get_or_create()[0]
    return render_template('tags.html', tags=tags.tags)


@app.route("/login", methods=["GET", "POST"])
def login():
    if current_user.is_authenticated():
        return redirect(url_for('index'))

    form = LoginForm()
    if form.validate_on_submit():
        user=form.get_user()
        if user:
            login_user(user)
            flash(u'Привет %s' % user.username, 'success')
            return redirect(url_for("index"))
    else:
        flash_errors(form)
    return render_template("login.html", form=form)

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("index"))