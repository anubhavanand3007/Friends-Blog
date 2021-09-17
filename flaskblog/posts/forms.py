from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flaskblog import conn

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Submit')

class UpdateForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()],default= "")
    content = TextAreaField('Content', validators=[DataRequired()],default= "")
    submit = SubmitField('Submit')

    