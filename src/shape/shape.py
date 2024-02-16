

from abc import ABC, abstractmethod
from typing import List, Tuple
from src.vector3 import Vector3


class Shape(ABC):

    def __init__(self, 
                 origin: Vector3, 
                 vertices_count: int,
                 width: int = 0, 
                 height: int = 0, 
                 depth: int = 1, 
                 rotation_x: int = 0, 
                 rotation_y: int = 0, 
                 rotation_z: int = 0,
                 velocity: Vector3 = Vector3(0, 0, 0)) -> None:
        self._origin = origin
        self._vertices_count = vertices_count
        self._width = width
        self._height = height
        self._depth = depth
        self._rotation_x = rotation_x
        self._rotation_y = rotation_y
        self._rotation_z = rotation_z
        self._velocity = velocity

    @abstractmethod
    def get_vertices(self) -> List[Vector3]:
        pass

    def get_origin(self) -> Vector3:
        return self._origin

    @abstractmethod
    def get_edges(self) -> List[Tuple[int, int]]:
        pass