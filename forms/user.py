from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField


class RegisterForm(FlaskForm):
    ROLES = [
        ('traveler', 'Путешественник'),
        ('guide', 'Гид/Организатор')
    ]

    email = StringField('Email:', validators=[
        DataRequired('Введите email'),
        Email('Некорректный E-mail адрес')
    ])
    password = PasswordField('Пароль:', validators=[
        DataRequired('Введите пароль'),
        Length(min=3, message='Пароль слишком короткий')
    ])
    password_again = PasswordField('Повторите пароль:', validators=[
        DataRequired('Повторите пароль'),
        Length(min=3, message='Пароль слишком короткий')
    ])
    name = StringField('Имя пользователя:', validators=[
        DataRequired('Введите своё имя'),
        Length(min=2, max=50, message='Имя от 2 до 50 символов')
    ])
    about = TextAreaField('О себе:', validators=[
        Length(max=500, message='Не более 500 символов')
    ])
    role = SelectField('Роль:', choices=ROLES, validators=[
        DataRequired('Выберите роль')
    ])
    phone = StringField('Телефон:', validators=[
        Length(min=10, max=20, message='Введите корректный номер телефона')
    ])
    submit = SubmitField('Зарегистрироваться')