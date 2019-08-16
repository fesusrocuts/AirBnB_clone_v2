#!/usr/bin/python3
"""This is the place class
"""

from models.base_model import BaseModel, Base
from sqlalchemy import Column, Integer, String, Float, ForeignKey, MetaData, Table
from sqlalchemy.orm import relationship
import os
from models import *

place_amenity = Table(
    'place_amenity', Base.metadata, Column(
        'place_id', String(60), ForeignKey('places.id')), Column(
            'amenity_id', String(60), ForeignKey('amenities.id')))

class Place(BaseModel):

    """This is the class for Place
    Attributes:
        city_id: city id
        user_id: user id
        name: name input
        description: string of description
        number_rooms: number of room in int
        number_bathrooms: number of bathrooms in int
        max_guest: maximum guest in int
        price_by_night:: pice for a staying in int
        latitude: latitude in flaot
        longitude: longitude in float
        amenity_ids: list of Amenity ids
    """

    __tablename__ = 'places'
    city_id = Column(String(60), ForeignKey('cities.id'), nullable=False)
    user_id = Column(String(60), ForeignKey('users.id'), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, default=0, nullable=False)
    number_bathrooms = Column(Integer, default=0, nullable=False)
    max_guest = Column(Integer, default=0, nullable=False)
    price_by_night = Column(Integer, default=0, nullable=False)
    latitude = Column(Float)
    longitude = Column(Float)
    amenity_ids = []
    reviews = relationship("Review", backref="place",
                           cascade="all, delete-orphan")
    amenities = relationship("Amenity", secondary=place_amenity,
                             viewonly=False, backref='place_amenities')

    if os.getenv("HBNB_TYPE_STORAGE") != "db":
        @property
        def get_reviews(self):
            my_list = []
            reviews_dict = models.storage.all(Review)
            for key, value in reviews_dict.items():
                if self.id == reviews_dict['place_id']:
                    my_list.append(value)
            return(my_list)
        @property
        def amenities(self):
            return self.amenity_ids

        @amenities.setter
        def amenities(self, ins=None):
            if type(ins) is Amenity:
                if ins.place_amenity.place_id == self.id:
                    self.amenity_ids.append(ins.id)
