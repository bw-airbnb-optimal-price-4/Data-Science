from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from app.database import metadata, db_session


class PropertyType(object):
    query = db_session.query_property()

    def __init__(self, id=None, property_type=None):
        self.id = id
        self.property_type = property_type

    def __repr__(self):
        return '<Property Type %r>' % self.property_type


property_types = Table('property_types', metadata,
                       Column('id', Integer, primary_key=True),
                       Column('property_type', String(255)),
                       )
mapper(PropertyType, property_types)
