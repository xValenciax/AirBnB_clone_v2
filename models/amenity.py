#!/usr/bin/python3

""" State Module for HBNB project """

import os
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship


class Amenity(BaseModel, Base):
    """This Model represents features wished in a place"""

    if os.getenv('HBNB_TYPE_STORAGE') == 'db':
        __tablename__ = "amenities"
        name = Column(String(128), nullable=False)
        place_amenities = relationship('Place', secondary='place_amenity', viewonly=False)

    else:
        name = ""
