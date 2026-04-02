import datetime
import sqlalchemy
from sqlalchemy import orm
from .db_session import SqlAlchemyBase


class Tour(SqlAlchemyBase):
    __tablename__ = 'tours'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    title = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    description = sqlalchemy.Column(sqlalchemy.Text, nullable=False)
    category = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    duration_days = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    price = sqlalchemy.Column(sqlalchemy.Float, nullable=False)
    location = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    max_people = sqlalchemy.Column(sqlalchemy.Integer, nullable=False)
    start_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    end_date = sqlalchemy.Column(sqlalchemy.DateTime, nullable=False)
    image_url = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    images = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    includes = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    itinerary = sqlalchemy.Column(sqlalchemy.Text, nullable=True)

    # Тип организатора: 'company' или 'guide'
    organizer_type = sqlalchemy.Column(sqlalchemy.String, default='company')

    # Если organizer_type = 'company'
    company_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    company_description = sqlalchemy.Column(sqlalchemy.Text, nullable=True)
    company_phone = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    company_email = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    company_website = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    # Если organizer_type = 'guide'
    guide_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("users.id"), nullable=True)
    guide = orm.relationship('User', back_populates='tours')

    created_date = sqlalchemy.Column(sqlalchemy.DateTime, default=datetime.datetime.now)
    is_active = sqlalchemy.Column(sqlalchemy.Boolean, default=True)

    bookings = orm.relationship('Booking', back_populates='tour', cascade='all, delete-orphan')

    def get_images_list(self):
        if self.images:
            import json
            try:
                return json.loads(self.images)
            except:
                return []
        return []

    def set_images_list(self, images_list):
        import json
        self.images = json.dumps(images_list)

    def get_organizer_name(self):
        if self.organizer_type == 'company':
            return self.company_name or "WildRoutes"
        else:
            return self.guide.name if self.guide else "Гид"

    def get_organizer_info(self):
        if self.organizer_type == 'company':
            return {
                'name': self.company_name or "WildRoutes",
                'description': self.company_description,
                'phone': self.company_phone,
                'email': self.company_email,
                'website': self.company_website,
                'type': 'company'
            }
        else:
            return {
                'name': self.guide.name if self.guide else "Гид",
                'description': self.guide.about if self.guide else None,
                'phone': self.guide.phone if self.guide else None,
                'avatar': self.guide.avatar_url if self.guide else None,
                'type': 'guide'
            }

    def __repr__(self):
        return f'<Tour> {self.title}'