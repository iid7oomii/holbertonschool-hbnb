from abc import ABC, abstractmethod


class Repository(ABC):
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
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]

    def get_by_attribute(self, attr_name, attr_value):
        return next(
            (
                obj
                for obj in self._storage.values()
                if getattr(obj, attr_name) == attr_value
            ),
            None,
        )


class SQLAlchemyRepository(Repository):
    """SQLAlchemy-based repository for database persistence"""
    
    def __init__(self, model):
        """
        Initialize repository with a SQLAlchemy model.
        
        Args:
            model: SQLAlchemy model class (e.g., User, Place, Review)
        """
        self.model = model
    
    def add(self, obj):
        """
        Add an object to the database.
        
        Args:
            obj: Object instance to add
        """
        from hbnb.app import db
        db.session.add(obj)
        db.session.commit()
    
    def get(self, obj_id):
        """
        Retrieve an object by its ID.
        
        Args:
            obj_id: The unique identifier of the object
            
        Returns:
            Object instance or None if not found
        """
        return self.model.query.get(obj_id)
    
    def get_all(self):
        """
        Retrieve all objects of this model type.
        
        Returns:
            List of all objects
        """
        return self.model.query.all()
    
    def update(self, obj_id, data):
        """
        Update an object with new data.
        
        Args:
            obj_id: The unique identifier of the object
            data: Dictionary of attributes to update
        """
        from hbnb.app import db
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
    
    def delete(self, obj_id):
        """
        Delete an object from the database.
        
        Args:
            obj_id: The unique identifier of the object
        """
        from hbnb.app import db
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
    
    def get_by_attribute(self, attr_name, attr_value):
        """
        Retrieve an object by a specific attribute value.
        
        Args:
            attr_name: Name of the attribute to filter by
            attr_value: Value to match
            
        Returns:
            First matching object or None
        """
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
