from abc import ABC, abstractmethod
from vector3 import Vector3
from typing import List

class Shape(ABC):

    @abstractmethod
    def get_origin(self) -> Vector3:
        pass

    @abstractmethod
    def get_edges(self, vertex: Vector3) -> list:
        pass

    @abstractmethod
    def get_vertices(self) -> List[Vector3]:
        pass