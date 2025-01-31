#!/usr/bin/python3
"""This module defines a class to manage file storage for hbnb clone"""
import json


class FileStorage:
    """This class manages storage of hbnb models in JSON format"""
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        if not cls:
            return FileStorage.__objects
        else:
            if (type(cls) == str):
                return {key: value for key, value in
                        FileStorage.__objects.items() if key.startswith(cls)}
            return {key: value for key, value in
                    FileStorage.__objects.items()
                    if key.startswith(cls.__name__)}

    def new(self, obj):
        """Adds new object to storage dictionary"""
        if not obj:
            return
        self.all().update({obj.to_dict()['__class__'] + '.' + obj.id: obj})

    def save(self):
        """Saves storage dictionary to file"""
        with open(FileStorage.__file_path, 'w') as f:
            temp = {}
            temp.update(FileStorage.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def delete(self, obj=None):
        """this delete an instance 'obj' from the '__objects' dict"""
        if not obj:
            return
        if (not obj.id):
            return
        key = f"{obj.to_dict()['__class__']}.{obj.id}"
        try:
            self.__objects.pop(key)
        except KeyError:
            return

    def reload(self):
        """Loads storage dictionary from file"""
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(FileStorage.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def search(self, cls=None, **kwargs):
        """this returns an instance of the classes with
            the provided id"""
        objs = self.all(cls)
        for key, obj in objs:
            flag = 0
            for attr, value in kwargs:
                if obj.get(attr) != value:
                    flag = 1
                    break
            if flag == 0:
                return obj
        return None

    def close(self):
        """This makes call to the reload method in order to
        deserialize json file to objects"""
        self.reload()
