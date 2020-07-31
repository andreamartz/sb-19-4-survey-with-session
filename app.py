from flask import Flask, render_template, request, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

debug = DebugToolbarExtension(app)


@app.route('/')
def show_survey_start():
    """Shows survey start page"""
    return render_template('survey_start.html', survey=survey)


@app.route('/begin', methods=["POST"])
def allow_survey_start():
    """Initialize list of responses to be an empty list.  
    Clears session of any existing responses."""

    session["responses"] = []
    return redirect('/questions/0')


@app.route('/questions/<int:qid>')
def show_question(qid):
    """Shows question from the survey"""
    
    if session["responses"] == None:
        # User must start the survey from the start page
        return redirect('/')

    if len(session['responses']) >= len(survey.questions):
        # User has answered all questions; thank them.
        return redirect('/thank-you')

    if qid != len(session["responses"]):
        # User trying to access questions out of order
        flash("You are trying to access an invalid question.", "error")
        return redirect(f'/questions/{len(session["responses"])}')

    # User is where they should be in survey
    question = survey.questions[qid].question
    choices = survey.questions[qid].choices
    return render_template('question.html', question=question, choices=choices, qid=qid, survey=survey)


@app.route('/answer', methods=['POST'])
def add_answer():
    """Add the answer to pretend database.
    Redirect the user."""

    # Get response to question
    answer = request.form['answer']

    # Add response to pretend database
    responses = session["responses"]
    responses.append(answer)
    session["responses"] = responses

    # Redirect user to either the next question or
    # thank you page if there are no more questions.
    if len(session["responses"]) == len(survey.questions):
        return redirect('/thank-you')
    else:
        return redirect(f"/questions/{len(session['responses'])}")


@app.route('/thank-you')
def thank_you():
    """Show the thank you page after survey completion."""
    return render_template('thank-you.html')
