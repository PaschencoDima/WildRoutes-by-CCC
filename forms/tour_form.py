from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, IntegerField, FloatField, DateTimeField, SelectField, BooleanField, \
    SubmitField
from wtforms.validators import DataRequired, Length, NumberRange, ValidationError, Optional
from datetime import datetime


class TourForm(FlaskForm):
    CATEGORIES = [
        ('hiking', '🏔️ Походы и трекинг'),
        ('city', '🏙️ Городские экскурсии'),
        ('adventure', '🚣 Приключения'),
        ('cultural', '🏛️ Культура и искусство'),
        ('food', '🍜 Гастрономия'),
        ('nature', '🌿 Природа'),
        ('extreme', '⚡ Экстрим')
    ]

    ORGANIZER_TYPES = [
        ('company', '🏢 Компания WildRoutes'),
        ('guide', '👤 Частный гид')
    ]

    # Основные поля
    title = StringField('Название тура', validators=[
        DataRequired('Введите название тура'),
        Length(min=5, max=100, message='Название должно быть от 5 до 100 символов')
    ])

    description = TextAreaField('Описание', validators=[
        DataRequired('Введите описание тура'),
        Length(min=50, max=2000, message='Описание должно быть от 50 до 2000 символов')
    ])

    category = SelectField('Категория', choices=CATEGORIES, validators=[
        DataRequired('Выберите категорию')
    ])

    duration_days = IntegerField('Длительность (дней)', validators=[
        DataRequired('Укажите длительность'),
        NumberRange(min=1, max=30, message='Длительность от 1 до 30 дней')
    ])

    price = FloatField('Цена (руб.)', validators=[
        DataRequired('Укажите цену'),
        NumberRange(min=0, message='Цена не может быть отрицательной')
    ])

    location = StringField('Место проведения', validators=[
        DataRequired('Укажите место проведения'),
        Length(min=3, max=100, message='Название места от 3 до 100 символов')
    ])

    max_people = IntegerField('Максимум участников', validators=[
        DataRequired('Укажите максимальное количество участников'),
        NumberRange(min=1, max=50, message='От 1 до 50 участников')
    ])

    start_date = DateTimeField('Дата начала (ГГГГ-ММ-ДД ЧЧ:ММ)', format='%Y-%m-%d %H:%M', validators=[
        DataRequired('Укажите дату начала')
    ])

    end_date = DateTimeField('Дата окончания (ГГГГ-ММ-ДД ЧЧ:ММ)', format='%Y-%m-%d %H:%M', validators=[
        DataRequired('Укажите дату окончания')
    ])

    image_url = StringField('Ссылка на изображение', validators=[
        Optional(),
        Length(max=500, message='Слишком длинная ссылка')
    ])

    images = StringField('Ссылки на дополнительные фото (через запятую)', validators=[
        Optional(),
        Length(max=2000, message='Слишком длинная строка')
    ])

    includes = TextAreaField('Что включено в стоимость', validators=[
        Optional(),
        Length(max=1000, message='Не более 1000 символов')
    ])

    itinerary = TextAreaField('Программа маршрута', validators=[
        DataRequired('Опишите программу маршрута'),
        Length(min=50, max=2000, message='Программа должна быть от 50 до 2000 символов')
    ])

    # Тип организатора
    organizer_type = SelectField('Тип организатора', choices=ORGANIZER_TYPES, validators=[
        DataRequired('Выберите тип организатора')
    ])

    # Поля для компании
    company_name = StringField('Название компании', validators=[
        Optional(),
        Length(min=2, max=100, message='Название от 2 до 100 символов')
    ])

    company_description = TextAreaField('О компании', validators=[
        Optional(),
        Length(max=500, message='Не более 500 символов')
    ])

    company_phone = StringField('Телефон компании', validators=[
        Optional(),
        Length(min=10, max=20, message='Некорректный номер')
    ])

    company_email = StringField('Email компании', validators=[
        Optional(),
        Length(max=100, message='Слишком длинный email')
    ])

    company_website = StringField('Сайт компании', validators=[
        Optional(),
        Length(max=200, message='Слишком длинная ссылка')
    ])

    is_active = BooleanField('Активен', default=True)
    submit = SubmitField('Сохранить тур')

    def validate_end_date(self, field):
        if self.start_date.data and field.data:
            if field.data <= self.start_date.data:
                raise ValidationError('Дата окончания должна быть позже даты начала')

    def validate_start_date(self, field):
        if field.data and field.data < datetime.now():
            raise ValidationError('Дата начала не может быть в прошлом')

    def get_images_list(self):
        if self.images.data:
            return [img.strip() for img in self.images.data.split(',') if img.strip()]
        return []