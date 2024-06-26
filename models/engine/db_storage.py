#!/usr/bin/python3
"""This module defines a class to manage database storage for hbnb clone"""

from models.base_model import BaseModel, Base
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, scoped_session
import os


classes = {'State': State, 'City': City, 'User': User, 'Place': Place}

class DBStorage:
    """This class manages database storage of hbnb models"""
    __engine = None
    __session =None

    def __init__(self):
        db_creds = [
            os.getenv('HBNB_MYSQL_USER'),
            os.getenv('HBNB_MYSQL_PWD'),
            os.getenv('HBNB_MYSQL_HOST'),
            os.getenv('HBNB_MYSQL_DB')
        ]

        conn_string = 'mysql+mysqldb://{}:{}@{}/{}'.format(db_creds[0], db_creds[1], db_creds[2], db_creds[3])
        self.__engine = create_engine(conn_string, pool_pre_ping=True)

        if os.getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)


    def get_key_by_value(dictionary, value):
        for key, val in dictionary.items():
            if val == value:
                return key
            return None


    def all(self, cls=None):
        """Returns a dictionary of models currently in storage"""
        objects = []
        cls_indices = []
        
        if cls:
            rows = self.__session.query(cls)
            for i, row in enumerate(rows):
                objects.append(row)

                for key, value in classes.items():
                    if value == cls:
                        cls_indices.append(key)
                        break
                    
        else:
            for key, _cls in classes.items():
                rows = self.__session.query(_cls)
                for row in rows:
                    objects.append(row)
                    cls_indices.append(key)


        output = {}

        for i, obj in enumerate(objects):
            key = '{}.{}'.format(cls_indices[i], obj.id)
            output[key] = obj

        return output


    def new(self, obj):
        """Adds new object to stoage"""
        self.__session.add(obj)

    def save(self):
        """Commit all changes to databse"""
        self.__session.commit()


    def delete(self, obj=None):
        """Deletes obj from __objects if it exists"""
        if not obj:
            return
        for _cls in classes:
            self.__session.query(_cls).filter(_cls.id == obj.id).delete(synchronize_session='fetch')

    def reload(self):
        """Loads storage dictionary from file"""
        Base.metadata.create_all(self.__engine)
        Session = sessionmaker(bind=self.__engine, expire_on_commit=True)
        self.__session = scoped_session(Session)
