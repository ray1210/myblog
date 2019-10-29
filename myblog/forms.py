from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, HiddenField, PasswordField, BooleanField
from wtforms.validators import DataRequired, Email, Length


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(1, 32)])
    password = PasswordField('Password', validators=[DataRequired(), Length(1, 128)])
    remember = BooleanField('Remember me')
    submit = SubmitField('Log in')


class PostForm(FlaskForm):
    title = StringField('title', validators=[DataRequired(), Length(1, 60)])
    body = TextAreaField('body')
    submit = SubmitField('submit')


class CommentForm(FlaskForm):
    author = StringField('author', validators=[DataRequired(), Length(1, 32)])
    email = StringField('email', validators=[DataRequired(), Email(), Length(1, 255)])
    body = TextAreaField('body', validators=[DataRequired(),Length(1, 512)])
    submit = SubmitField()


class AdminCommentForm(CommentForm):
    author = HiddenField()
    email = HiddenField()


class AdminAboutForm(FlaskForm):
    title = StringField('about_title', validators=[DataRequired(), Length(1, 128)])
    body = TextAreaField('body', validators=[DataRequired()])
