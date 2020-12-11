from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from flask_login import current_user
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms import ValidationError, TextAreaField
from wtforms.validators import DataRequired, Email, Length, EqualTo
from .models import User


class RegisterForm(FlaskForm):
    username = StringField('Логин', validators=[
        DataRequired(),
        Length(min=4, max=30,
               message='Логин может содержать от 4 до 30 символов')])
    email = StringField('Email', validators=[
        DataRequired(), Email('Некорректный Email')])
    password = PasswordField('Пароль', validators=[
        DataRequired(),
        Length(min=8, max=100,
               message='Пароль может содержать от 8 до 100 символов')])
    password_repeat = PasswordField('Повторите пароль', validators=[
        DataRequired(), EqualTo('password', message='Пароли не совпадают')])
    submit = SubmitField('Зарегистрироваться')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Такой email уже существует')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Такой логин уже сущестует')


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[
        DataRequired(), Email('Некорректный Email')])
    password = PasswordField('Пароль', validators=[DataRequired()])
    remember = BooleanField('Запомнить', default=False)
    submit = SubmitField('Войти')

    def validate_email(self, field):
        if not User.query.filter_by(email=field.data).first():
            raise ValidationError('Такой email не зарегистрирован')


class UpdateAccountForm(FlaskForm):
    picture = FileField('Обновить фотографию',
                        validators=[FileAllowed(['jpg', 'png', 'jpeg'])])
    username = StringField('Логин', validators=[
        DataRequired(),
        Length(min=4, max=30,
               message='Логин может содержать от 4 до 30 символов')])
    firstname = StringField('Имя', validators=[
        DataRequired()])
    lastname = StringField('Фамилия', validators=[
        DataRequired()])
    submit = SubmitField('Сохранить')

    def validate_username(self, field):
        if self.username.data != current_user.username:
            if User.query.filter_by(username=field.data).first():
                raise ValidationError('Так логин уже сущестует')


class AritcleForm(FlaskForm):
    title = StringField('Название', validators=[
        DataRequired(),
        Length(min=4, max=50,
               message='Название статьи может содержать от 4 до 50 символов')])
    text = TextAreaField('Текст статьи', validators=[
        DataRequired(),
        Length(max=500,
               message='Статья может содержать до 500 символов')],
        render_kw={'rows': 10})
    submit = SubmitField('Добавить')


class UpdateArticleForm(FlaskForm):
    title = StringField('Название', validators=[
        DataRequired(),
        Length(min=4, max=50,
               message='Название статьи может содержать от 4 до 50 символов')])
    text = TextAreaField('Текст статьи', validators=[
        DataRequired(),
        Length(max=500,
               message='Статья может содержать до 500 символов')],
        render_kw={'rows': 10})
    submit = SubmitField('Обновить')
