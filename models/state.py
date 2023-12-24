#!/usr/bin/python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from . import storage

storage_type = getenv("HBNB_TYPE_STORAGE")


if storage_type == "db":
    class State(BaseModel, Base):
        """ the class implementation of states table """
        __tablename__ = "states"
        if storage_type == "db":
            name = Column(String(128), nullable=False)
            cities = relationship("City", backref="state")

else:
    class State(BaseModel):
        """ the class implementation of the states storage"""
        @property
        def cities(self):
            """returns the list of City instances
                with state_id equals to the current State.id"""
            return map(lambda x: x.state_id == self.id,
                       storage.all("City").values())
