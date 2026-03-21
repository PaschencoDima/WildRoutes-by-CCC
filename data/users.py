import datetime
import sqlalchemy
from flask_login import UserMixin, AnonymousUserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class User(SqlAlchemyBase, UserMixin):
    __tablename__ = 'users'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    about = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    email = sqlalchemy.Column(sqlalchemy.String, index=True, unique=True, nullable=False)
    hashed_password = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)

    # Дополнительные поля для платформы путешествий
    role = sqlalchemy.Column(sqlalchemy.String, default='traveler')  # traveler, guide
    phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    avatar_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # Связи
    tours = orm.relationship('Tour', back_populates='guide', cascade='all, delete-orphan')
    bookings = orm.relationship('Booking', back_populates='traveler', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User> {self.name} ({self.email})'

    def set_password(self, password):
        self.hashed_password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.hashed_password, password)

    def is_guide(self):
        return self.role == 'guide'

    def is_traveler(self):
        return self.role == 'traveler'

    def get_avatar(self):
        if self.avatar_url:
            return self.avatar_url
        return 'https://via.placeholder.com/150/4CAF50/ffffff?text=' + self.name[0].upper()


class AnonymousUser(AnonymousUserMixin):
    def is_guide(self):
        return False

    def is_traveler(self):
        return False

    def get_avatar(self):
        return None