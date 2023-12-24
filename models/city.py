#!/usr/bin/python3
""" City Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String, ForeignKey
import os

storage_type = os.getenv('HBNB_TYPE_STORAGE')


if storage_type == "db":
    class City(BaseModel, Base):
        """ The city class, contains state ID and name """
        __tablename__ = "cities"
        name = Column(String(128), nullable=False)
        state_id = Column(String(60), ForeignKey("states.id"), nullable=False)
else:
    class City(BaseModel):
        """ The city class, contains state ID and name """
        __tablename__ = "cities"
