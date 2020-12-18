from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from surveys import Survey, satisfaction_survey
app=Flask(__name__)
app.config['SECRET_KEY'] = "chickens123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug= DebugToolbarExtension(app)

responses = []

@app.route('/')
def home_page():
    title=satisfaction_survey.title
    instructions=satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

@app.route('/questions/<int:question_num>')
def questions_page(question_num):
    question_length=len(satisfaction_survey.questions)
    response_length=len(responses)
    if question_num >= question_length or question_num > response_length: #try relating the question_num to length of responses to see if the user is trying to skip questions through the url
        flash("You have been redirected. You must answer the survey questions in order")
        return redirect(f'/questions/{response_length}')
    if question_length == response_length:
        return redirect('/thank_you')
    my_question=satisfaction_survey.questions[question_num].question #question num is the index so this will get the corresponding question
    choices= satisfaction_survey.questions[question_num].choices
    return render_template(f"questions.html", my_question =my_question, choices=choices, question_num=question_num, question_length=question_length, response_length=response_length) 

@app.route('/answer', methods=["POST"])
def collected_answers():
    question_length=len(satisfaction_survey.questions) #how many questions are in the survey...once we post last one, want to go to thank-you page
    question_num=len(responses) #starts at 0 (index of 0)
    answer=request.form["choice"]
    responses.append(answer)
    if question_length -1 == question_num:
        return redirect('/thank_you')
    return redirect(f'/questions/{question_num+1}')

@app.route('/thank_you')
def thank_you():
    #something
    return render_template('thank_you.html')
