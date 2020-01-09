from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import mapper
from app.database import metadata, db_session
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship
from sqlalchemy.orm import backref
from .property_type import PropertyType
from .neighborhood import Neighborhood


class Listing(object):
    query = db_session.query_property()

    def __init__(self, id=None, user_id=None, property_type_id=None,
                 neighborhood_id=None, room_type=None,
                 accommodates=None, bedrooms=None, bathrooms=None, beds=None,
                 listing_url=None,
                 title=None, picture_url=None, city=None, state=None, zip=None,
                 price=None, country=None, latitude=None, longitude=None):
        self.id = id
        self.user_id = user_id
        self.property_type_id = property_type_id
        self.neighborhood_id = neighborhood_id
        self.room_type = room_type
        self.accommodates = accommodates
        self.bedrooms = bedrooms
        self.bathrooms = bathrooms
        self.beds = beds
        self.listing_url = listing_url
        self.title = title
        self.picture_url = picture_url
        self.city = city
        self.state = state
        self.zip = zip
        self.price = price
        self.country = country
        self.latitude = latitude
        self.longitude = longitude

    def __repr__(self):
        return '<Listing %r>' % self.title


room_types_enum = ENUM('Entire Home/Apt', 'Private Room', 'Shared Room',
                       'Hotel Room', name='room_types', metadata=metadata)
listings = Table('listings', metadata,
                 Column('id', Integer, primary_key=True),
                 Column('user_id', Integer, ForeignKey("users.id"),
                        nullable=False),
                 Column('property_type_id', Integer,
                        ForeignKey("property_types.id"), nullable=False),
                 Column('neighborhood_id', Integer,
                        ForeignKey("neighborhoods.id"), nullable=False),
                 Column('room_type', room_types_enum, nullable=False),
                 Column('accommodates', Integer, nullable=False),
                 Column('bedrooms', Integer, nullable=False),
                 Column('bathrooms', Integer, nullable=False),
                 Column('beds', Integer, nullable=False),
                 Column('listing_url', String(355), nullable=False),
                 Column('title', String(255), nullable=False),
                 Column('picture_url', String(355)),
                 Column('city', String(255), nullable=False),
                 Column('state', String(2), nullable=False),
                 Column('zip', Integer, nullable=False),
                 Column('price', Integer, nullable=False),
                 Column('country', String(255), nullable=False),
                 Column('latitude', Float, nullable=False),
                 Column('longitude', Float, nullable=False)
                 )
mapper(Listing, listings, properties={
    "property_type": relationship(PropertyType,
                                  backref=backref("property_type_id",
                                                  lazy='dynamic')),
    "neighborhood":  relationship(Neighborhood,
                                  backref=backref("neighborhood_id",
                                                  lazy='dynamic'))
})
