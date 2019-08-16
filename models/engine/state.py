#!/usr/bin/python3
"""This is the state class"""
from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String, Integer, ForeignKey


class State(BaseModel, Base):
    """This is the class for State
    Attributes:
    name: input name
    """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    cities = relationship('City', cascade='all, delete-orphan', backref='state')

    @property
    def cities(self):
        """
        Getter fuction for FileStorage mode
        """
        list_cities = []
        for item in models.storage.all(City).values():
            if item.state_id == self.id:
                list_cities.append(item)
        return list_cities
