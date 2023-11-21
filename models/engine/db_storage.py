#!/usr/bin/env python3
from models.base_model import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


dialect, driver = "mysql", "mysqldb"
user, password = getenv("HBNB_MYSQL_USER"), getenv("HBNB_MYSQL_PWD")
host, db_name = getenv("HBNB_MYSQL_HOST"), getenv("HBNB_MYSQL_DB")
hbnb_env = getenv("HBNB_ENV")

metadata = None


class DBStorage:
    """a class implementation of the database storage"""
    __engine = None
    __session = None

    def __init__(self):
        """a constructor function for the DBStorage class"""
        connection_url = f"mysql+mysqldb://{user}:{password}@{host}/{db_name}"
        DBStorage.__engine = create_engine(connection_url, pool_pre_ping=True)
        global metadata
        metadata = Base.metadata
        if (hbnb_env == "test"):
            metadata.drop_all()

    def all(self, cls=None):
        """ this querys the db session and returns
            a dict of all objects in the query """
        if not DBStorage.__session:
            return {}
        from models import User, City, Place, State, Review, Amenity
        name_to_class_mapper = {"User": User, "City": City, "Place": Place,
                                "State": State, "Review": Review, "Amenity": Amenity}
        if not cls:
            users = DBStorage.__session.query(User).all()
            cities = DBStorage.__session.query(City).all()
            states = DBStorage.__session.query(State).all()
            reviews = DBStorage.__session.query(Review).all()
            amenities = DBStorage.__session.query(Amenity).all()
            res = [*amenities, *cities, *reviews, *states, *users]
            res_dict = {f"{entry.__dict__['__class__']}.{entry.id}": entry
                        for entry in res}
            return res_dict
        else:
            if cls not in name_to_class_mapper:
                return []
            res = DBStorage.__session.query(name_to_class_mapper[cls]).all()
            res_dict = {f"{entry.__dict__['__class__']}.{entry.id}": entry
                        for entry in res}
            return res_dict

    def new(self, obj):
        """adds the object to the current database session"""
        if (self.__session):
            self.__session.add(obj)

    def save(self):
        """commits all changes of the current database session"""
        if (self.__session):
            self.__session.commit()

    def delete(self, obj):
        """delete from the current database session obj if not None"""
        if not obj:
            return
        if (self.__session):
            self.__session.delete(obj)

    def reload(self):
        """creates all tables in the database"""
        if metadata:
            metadata.create_all(bind=self.__engine)
        self.__session = scoped_session(sessionmaker(bind=self.__engine,
                                                     expire_on_commit=False))()
