from flask_wtf import FlaskForm
from wtforms.validators import DataRequired, Email, Length
from wtforms import StringField, PasswordField, TextAreaField, SelectField, SubmitField


class RegisterForm(FlaskForm):
    ROLES = [
        ('traveler', 'Путешественник'),
        ('guide', 'Гид/Организатор')
    ]

    name = StringField('Имя пользователя', validators=[
        DataRequired('Введите имя'),
        Length(min=2, max=50)
    ])

    email = StringField('Email', validators=[
        DataRequired('Введите email'),
        Email('Некорректный email')
    ])

    password = PasswordField('Пароль', validators=[
        DataRequired('Введите пароль'),
        Length(min=3, message='Пароль минимум 3 символа')
    ])

    password_again = PasswordField('Повторите пароль', validators=[
        DataRequired('Повторите пароль')
    ])

    about = TextAreaField('О себе')

    role = SelectField('Роль', choices=ROLES)

    phone = StringField('Телефон')

    submit = SubmitField('Зарегистрироваться')