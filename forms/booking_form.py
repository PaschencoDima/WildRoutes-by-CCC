from flask_wtf import FlaskForm
from wtforms import IntegerField, TextAreaField, SubmitField
from wtforms.validators import DataRequired, NumberRange, Optional, Length

class BookingForm(FlaskForm):
    people_count = IntegerField('Количество участников', validators=[
        DataRequired('Укажите количество участников'),
        NumberRange(min=1, max=20, message='От 1 до 20 участников')
    ])

    message = TextAreaField('Сообщение гиду (опционально)', validators=[
        Optional(),
        Length(max=500, message='Не более 500 символов')
    ])

    submit = SubmitField('Забронировать')