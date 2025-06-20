#!/usr/bin/python3
from abc import ABC, abstractmethod
'''

'''


class Repository(ABC):
    '''
    This class defines the base in memory repositories
    to test the API before database implementation
    '''
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[str(obj.id)] = obj

    def get(self, obj_id):
        return self._storage.get(str(obj_id))

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            updated_obj = obj.copy(update=data)
            self._storage[str(obj_id)] = updated_obj
            return updated_obj
        return None

    def delete(self, obj_id):
        key = str(obj_id)
        if key in self._storage:
            del self._storage[key]

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values()
                     if getattr(obj, attr_name) == attr_value), None)
