from flask import render_template, redirect, url_for, request

from app import app
from forms import QuestionForm, CommentForm
from model import Question, Comment

@app.route('/')
def index():
    print dir(request)
    questions = Question.objects.order_by("-timestamp")
    return render_template("index.html", questions=questions)

@app.route("/question/add/", methods=["GET", "POST"])
def new_question():
    form = QuestionForm()
    if form.validate_on_submit():
        username = form.username.data
        title = form.title.data
        body = form.body.data
        tags = form.tags.data
        if tags != "":
            tags = tags.split(",")
        else:
            tags = []
        question = Question(username=username, title=title, body=body, tags=tags)
        question.save()
        return redirect(url_for("index"))
    return render_template("add_question.html", form=form)

@app.route("/question/<question_id>", methods=["GET", "POST"])
def question(question_id):
    question = Question.objects.get(id=question_id)
    form = CommentForm()
    if form.validate_on_submit():
        username = form.username.data
        body = form.body.data
        comment = Comment(username=username, body=body)
        question.update(add_to_set__comments=comment)
        question.save()
        return redirect("/question/%s" % question_id)
    return render_template('question.html', question=question, form=form)