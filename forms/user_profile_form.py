from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Optional


class UserProfileForm(FlaskForm):
    ROLES = [
        ('traveler', 'Путешественник'),
        ('guide', 'Гид/Организатор')
    ]

    name = StringField('Имя', validators=[
        DataRequired('Введите ваше имя'),
        Length(min=2, max=50, message='Имя от 2 до 50 символов')
    ])

    email = StringField('Email', validators=[
        DataRequired('Введите email'),
        Email('Некорректный email')
    ])

    about = TextAreaField('О себе', validators=[
        Length(max=500, message='Не более 500 символов')
    ])

    phone = StringField('Телефон', validators=[
        Optional(),
        Length(min=10, max=20, message='Некорректный номер телефона')
    ])

    role = SelectField('Роль', choices=ROLES, validators=[
        DataRequired('Выберите роль')
    ])

    avatar_url = StringField('Ссылка на аватар', validators=[
        Optional(),
        Length(max=500, message='Слишком длинная ссылка')
    ])

    submit = SubmitField('Сохранить изменения')