#!/usr/bin/python3
"""New engine"""
import sqlalchemy
from sqlalchemy import create_engine
from os import getenv
from models.base_model import BaseModel, Base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import scoped_session
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
import models


class DBStorage:
    '''
    Serializes instances to JSON file and deserializes to JSON file.
    '''

    __engine = None
    __session = None

    def __init__(self):
        '''
        create new instance of DBStorage
        '''
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')
        my_sql = "mysql+mysqldb://{}:{}@{}/{}".format(user,
                                                      password,
                                                      host,
                                                      database)
        self.__engine = create_engine('{}'.format(my_sql),
                                      pool_pre_ping=True)
        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(bind=self.__engine)

    def all(self, cls=None):
        '''
            Queries database for specified classes

        '''
        to_query = []
        new_dict = {}
        if cls:
            results = self.__session.query(cls).all()
            for row in results:
                key = row.__class__.__name__
                t_id = str(row.id)
                new_key = key + '.' + row.id
                new_dict[new_key] = row
        else:
            for k, v in models.classes.items():
                if k != "BaseModel":
                    for obj in self.__session.query(v).all():
                        key = "{}.{}".format(obj.__class__.__name__, obj.id)
                        new_dict[key] = obj
        return new_dict

    def new(self, obj):
        '''
            Saves an object to the current session object
        '''
        if obj:
            self.__session.add(obj)

    def save(self):
        """add to session"""
        self.__session.commit()

    def delete(self, obj=None):
        """remove obj from session"""
        if obj:
            self.__session.delete(obj)

    def reload(self):
        '''
            Restarts the database engine session
        '''
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine)
        Session = scoped_session(session_factory)
        self.__session = Session()
