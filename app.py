from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from random import randint, choice, sample
from surveys import Survey, satisfaction_survey
app=Flask(__name__)
app.config['SECRET_KEY'] = "chickens123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug= DebugToolbarExtension(app)

# responses = [] #won't be using as a single list, will turn into a session

@app.route('/')
def home_page():
    title=satisfaction_survey.title
    instructions=satisfaction_survey.instructions
    return render_template("home.html", title=title, instructions=instructions)

@app.route('/make-session', methods=["POST"])
def make_session():
    session["responses"]=[]
    return redirect('/questions/0')

@app.route('/questions/<int:question_num>')
def questions_page(question_num):
    question_length=len(satisfaction_survey.questions)
    responses=session["responses"]
    response_length=len(responses)

    if question_num >= question_length or question_num > response_length: #try relating the question_num to length of responses to see if the user is trying to skip questions through the url
        flash("You have been redirected. You must answer the survey questions in order")
        return redirect(f'/questions/{response_length}')
    if question_num < response_length: #prevents going back
        flash("You have already submitted the response for the previous page, please continue")
        return redirect(f'/questions/{question_num +1}')
    if question_length == response_length:
        return redirect('/thank_you')
    my_question=satisfaction_survey.questions[question_num].question #question num is the index so this will get the corresponding question
    choices= satisfaction_survey.questions[question_num].choices
    return render_template(f"questions.html", my_question =my_question, choices=choices, question_num=question_num, question_length=question_length, response_length=response_length) 

@app.route('/answer', methods=["POST"])
def collected_answers():
    #can we make a flash conditional is not there...redirect back to the same page?
    answer=request.form["choice"] #the radio buttons have a name of choice so here will be the answer

    responses=session["responses"] #initially empty list, length of 0
    responses.append(answer) #add the new answer into the list
    session["responses"]=responses #modify the session to add in the answer to the list

    question_length=len(satisfaction_survey.questions) #how many questions are in the survey...once we post last one, want to go to thank-you page
    question_num=len(responses) #starts at 0 (index of 0)

    if question_length  == question_num: #if number of responses = number of questions, then everything was answered and survey is done.
        return redirect('/thank_you')

    return redirect(f'/questions/{question_num}') #because /0 corresponds with first question (offset by 1), 

@app.route('/thank_you')
def thank_you():
    #something
    return render_template('thank_you.html')
