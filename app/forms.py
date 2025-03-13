# Import necessary modules from Flask-WTF and WTForms
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

# Define a form class for the trivia game
class TriviaForm(FlaskForm):
    # Field for the trivia question with a data required validator
    question = StringField('Question', validators=[DataRequired()])
    # Field for the trivia answer with a data required validator
    answer = StringField('Answer', validators=[DataRequired()])
    # Submit button for the form
    submit = SubmitField('Submit')