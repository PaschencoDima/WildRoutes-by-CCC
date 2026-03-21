import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Booking(SqlAlchemyBase):
    __tablename__ = 'bookings'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    people_count = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    total_price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    status = sqlalchemy.Column(sqlalchemy.String, default='pending')  # pending, confirmed, cancelled, completed
    booking_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    message = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    traveler_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"))
    tour_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("tours.id"))

    traveler = orm.relationship('User', back_populates='bookings')
    tour = orm.relationship('Tour', back_populates='bookings')

    def __repr__(self):
        return f'<Booking> Tour {self.tour_id} by {self.traveler_id}'