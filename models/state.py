#!/usr/bin/env python3
""" State Module for HBNB project """
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from . import storage

storage_type = getenv("HBNB_TYPE_STORAGE")


class State(BaseModel, Base):
    """ State class """
    __tablename__ = "states"
    name = Column(String(128), nullable=False)
    if storage_type == "db":
        cities = relationship("City", backref="state")

    @property
    def cities(self):
        if (storage_type == "file"):
            state_id_mapper = lambda x: x.state_id == self.id
            return map(state_id_mapper, storage.all().values())
        return None
