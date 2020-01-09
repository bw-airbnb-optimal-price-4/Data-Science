from sqlalchemy import Table, Column, Integer, String
from sqlalchemy.orm import mapper
from app.database import metadata, db_session


class Neighborhood(object):
    query = db_session.query_property()

    def __init__(self, id=None, neighborhood=None):
        self.id = id
        self.neighborhood = neighborhood

    def __repr__(self):
        return '<Property Type %r>' % self.neighborhood


neighborhoods = Table('neighborhoods', metadata,
                      Column('id', Integer, primary_key=True),
                      Column('neighborhood', String(255)),
                      )
mapper(Neighborhood, neighborhoods)
