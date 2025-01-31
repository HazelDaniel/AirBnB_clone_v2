#!/usr/bin/python3
"""a module that holds the implementation of a dbstorage engine"""
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
            metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """ this querys the db session and returns
            a dict of all objects in the query """
        if not self.__session:
            return {}
        from models.user import User
        from models.city import City
        from models.place import Place
        from models.state import State
        from models.review import Review
        from models.amenity import Amenity
        name_to_class_mapper = {"User": User, "City": City, "Place": Place,
                                "State": State, "Review": Review,
                                "Amenity": Amenity}
        if not cls:
            cls_list = name_to_class_mapper.values()
            res_list = []
            res_dict = {}
            for entry in cls_list:
                res = self.__session.query(entry).all()
                res_list.extend(res)
            for entry in res_list:
                x = entry
                res_dict[f"{entry.to_dict()['__class__']}"
                         f".{entry.id}"] = x.__str__()
            return res_dict
        else:
            if not (type(cls) == str):
                if cls.__name__ not in name_to_class_mapper:
                    return {}
                res = self.__session.query(name_to_class_mapper
                                           [cls.__name__]).all()
                res_dict = {}
                for entry in res:
                    res_dict[f"{cls}.{entry.id}"] = entry
            else:
                if cls not in name_to_class_mapper:
                    return {}
                res = self.__session.query(name_to_class_mapper
                                           [cls]).all()
                res_dict = {}
                for entry in res:
                    res_dict[f"{cls}.{entry.id}"] = entry
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
            """this is to avoid circular imports that
                would be triggered if we were to import from models
                package directly"""
            from models.user import User
            from models.city import City
            from models.place import Place
            from models.state import State
            from models.review import Review
            from models.amenity import Amenity
            metadata.create_all(bind=self.__engine)
            self.__session =\
                scoped_session(sessionmaker(bind=self.__engine,
                                            expire_on_commit=False))

    def search(self, cls=None, **kwargs):
        """this searches for the objects that
            correspond to this value in the object storage"""
        objs = self.all(cls)
        for key, obj in objs.items():
            flag = 0
            for attr, value in kwargs.items():
                if getattr(obj, attr) != value:
                    flag = 1
                    break
            if flag == 0:
                return obj
        return None

    def close(self):
        """makes a call to the reload method in order to close
            the current db session"""
        if self.__session:
            self.__session.close()
