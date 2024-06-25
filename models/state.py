#!/usr/bin/python3

""" State Module for HBNB project """

import os
from models.base_model import BaseModel, Base
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """ State class """

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = 'states'
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state')

    else:
        name = ""

        @property
        def cities(self):
            from models import storage
            city_instances = storage.all(City)
            cities_of_this_state = [val for key, val in city_instances.items() if val.state_id == self.id]
            return cities_of_this_state
