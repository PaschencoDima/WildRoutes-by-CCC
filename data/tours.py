import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tour(SqlAlchemyBase):
    __tablename__ = 'tours'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)  # hiking, city, adventure, cultural, etc.
    duration_days = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    max_people = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    image_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    includes = sqlalchemy.Column(sqlalchemy.Text, nullable=True)  # что включено
    itinerary = sqlalchemy.Column(sqlalchemy.Text, nullable=True)  # программа маршрута

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    guide_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    guide = orm.relationship('User', back_populates='tours')

    bookings = orm.relationship('Booking', back_populates='tour', cascade='all, delete-orphan')

    def __repr__(self):
        return f'<Tour> {self.title}'