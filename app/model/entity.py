from abc import ABC, abstractmethod

from pypika import Table

class Entity(ABC):

    @classmethod
    @abstractmethod
    def entity_name(cls) -> str:
        pass

    @classmethod
    @abstractmethod
    def table_name(cls) -> str:
        pass

    @classmethod
    def table(cls) -> Table:
        return Table(cls.table_name())
    
