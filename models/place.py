#!/usr/bin/python3

""" Place Module for HBNB project """

import os
from models.base_model import BaseModel, Base
from models.review import Review
from models.amenity import Amenity
from sqlalchemy import Column, String, Integer, Float, ForeignKey, Table
from sqlalchemy.orm import relationship


if os.getenv('HBNB_TYPE_STORAGE') == 'db':
    place_amenity = Table('place_amenity', Base.metadata,
                          Column('place_id', String(60), ForeignKey('places.id'), nullable=False, primary_key=True),
                          Column('amenity_id', String(60), ForeignKey('amenities.id'), nullable=False, primary_key=True)
    )

class Place(BaseModel, Base):
    """ A place to stay """

    if os.getenv("HBNB_TYPE_STORAGE") == 'db':
        __tablename__ = 'places'
        city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
        user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
        name = Column(String(128), nullable=False)
        description = Column(String(1024), nullable=True)
        number_rooms = Column(Integer, default=0, nullable=False)
        number_bathrooms = Column(Integer, default=0, nullable=False)
        max_guest = Column(Integer, default=0, nullable=False)
        price_by_night = Column(Integer, default=0, nullable=False)
        latitude = Column(Float, nullable=True)
        longitude = Column(Float, nullable=True)
        reviews = relationship('Review', backref='place')
        amenities = relationship('Amenity', secondary='place_amenity', viewonly=False)

    else:
        city_id = ""
        user_id = ""
        name = ""
        description = ""
        number_rooms = 0
        number_bathrooms = 0
        max_guest = 0
        price_by_night = 0
        latitude = 0.0
        longitude = 0.0
        amenity_ids = []

        @property
        def reviews(self):
            """Get all reviews of this place"""
            from models import storage
            review_instances = storage.all(Review)
            reviews_of_this_place = [val for key, val in review_instances.items() if val.place_id == self.id]
            return reviews_of_this_place

        @property
        def amenities(self):
            """Get all amenities of this place"""
            from models import storage
            amenity_instances = storage.all(Amenity)
            amenities_of_this_place = [val for key, val in review_instances.items() if val.id in self.amenity_ids]
            return amenities_of_this_place


        @amenities.setter
        def amenities(self, obj):
            """Set an amenity to this place's amenity list"""
            if isinstance(obj, Amenity):
                self.amenity_ids.append(obj.id)            
