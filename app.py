from flask import Flask, render_template, request, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

# ********************************************
# GLOBAL VARIABLES
# responses -> initialize responses; this is the variable that will store survey answers
#     e.g. responses = ['Yes', 'No', 'Less than $10,000', 'Yes']
responses = []
# *********************************************


@app.route('/')
def home_page():
    """Shows survey start page"""
    return render_template('home.html', survey=survey)


@app.route('/questions/<int:idx>')
def show_question(idx):
    """Shows question from the survey"""

    if len(responses) >= len(survey.questions):
        return redirect('/thank-you')

    if idx == len(responses):
        question = survey.questions[idx].question
        choices = survey.questions[idx].choices
        return render_template('question.html', survey=survey, question=question, choices=choices, idx=idx)
    else:
        flash("You are trying to access an invalid question.", "error")
        return redirect(f'/questions/{len(responses)}')


@app.route('/answer', methods=['POST'])
def add_answer():
    """Adds the answer to the pretend database and redirects the user"""
    answer = request.form['answer']
    # Add to pretend database
    responses.append(answer)

    # Redirect user to either the next question or
    # thank you page if there are no more questions.
    if len(responses) < len(survey.questions):
        return redirect(f'/questions/{len(responses)}')
    else:
        return redirect('/thank-you')


@app.route('/thank-you')
def thank_you():
    """Show the thank you page"""
    return render_template('thank-you.html')
