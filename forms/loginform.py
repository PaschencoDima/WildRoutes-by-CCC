from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, BooleanField, SubmitField


class LoginForm(FlaskForm):
    email = StringField('Email:', validators=[
        DataRequired('Введите email'),
        Email('Некорректный E-mail адрес')
    ])
    password = PasswordField('Пароль:', validators=[
        DataRequired('Введите пароль'),
        Length(min=3, message='Пароль слишком короткий')
    ])
    remember_me = BooleanField('Запомнить меня')
    submit = SubmitField('Войти')