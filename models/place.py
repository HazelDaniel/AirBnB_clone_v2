#!/usr/bin/python3
""" Place Module for HBNB project """
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship

storage_type = getenv("HBNB_TYPE_STORAGE")


class Place(BaseModel, Base):
    """ a class implementation of the places table """
    __tablename__ = "places"

    if storage_type == "db":
        reviews = relationship("Reviews", backref="place")

    city_id = Column(String(60), ForeignKey("cities.id"), nullable=False)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=False)
    name = Column(String(128), nullable=False)
    description = Column(String(1024))
    number_rooms = Column(Integer, nullable=False, default=0)
    number_bathrooms = Column(Integer, nullable=False, default=0)
    max_guest = Column(Integer, nullable=False, default=0)
    price_by_night = Column(Integer, nullable=False, default=0)
    latitude = Column(Float, default=0)
    longitude = Column(Float, default=0)
    amenity_ids = []

    @property
    def reviews(self):
        """returns the list of Review instances
            with place_id equals to the current Place.id"""
        from models import storage
        if (storage_type == "file"):
            return map(lambda x: x.place_id == self.id,
                       storage.all("Review").values())
        return None
