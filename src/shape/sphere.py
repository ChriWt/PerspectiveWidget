from src.shape.shape import Shape
from src.vector3 import Vector3
from typing import List, Optional
from numpy import sin, cos
from math import pi
import numpy as np


class Sphere(Shape):

    def __init__(self, 
                 origin: Vector3, 
                 vertices_count: int,
                 width: int, 
                 height: Optional[int] = None,
                 depth: Optional[int] = None,
                 rotation_x: int = 0, 
                 rotation_y: int = 0,
                 velocity: Vector3 = Vector3(0, 0, 0)) -> None:
        super().__init__(origin, vertices_count, width, height, depth, rotation_x, rotation_y, velocity=velocity)
        self._height = self.__get_default_value_if_empty(height, width)
        self._depth = self.__get_default_value_if_empty(depth, width)

    def __get_default_value_if_empty(self, value: Optional[int], default: int) -> int:
        return default if value is None else value
    
    def get_vertices(self) -> List[Vector3]:
        vertices = []
        for phi in range(self._vertices_count):
            for theta in range(self._vertices_count):
                x = self._origin.x + self._width * sin(phi * pi / self._vertices_count) * cos(theta * 2 * pi / self._vertices_count)
                y = self._origin.y + self._height * sin(phi * pi / self._vertices_count) * sin(theta * 2 * pi / self._vertices_count)
                z = self._origin.z + self._depth * cos(phi * pi / self._vertices_count)
                vertices.append(Vector3(x, y, z))

        vertices.append(Vector3(self._origin.x, self._origin.y, self._origin.z - self._depth))
        return vertices

    def get_edges(self) -> np.ndarray:
        phi_indices = np.arange(self._vertices_count * self._vertices_count).reshape(self._vertices_count, self._vertices_count)
        
        # Horizontal edges (latitude lines), avoiding wrapping at the end of a row
        horizontal_edges = np.stack((phi_indices[:, :-1].ravel(), phi_indices[:, 1:].ravel()), axis=1)

        # Vertical edges (longitude lines), avoiding the last row
        vertical_edges = np.stack((phi_indices[:-1, :].ravel(), phi_indices[1:, :].ravel()), axis=1)

        # Connect the last vertices in each "latitude" line to the first to complete the loop
        last_to_first_edges = np.stack((phi_indices[:, -1], phi_indices[:, 0]), axis=1)

        # Connect the last row to the south pole, which is assumed to be the last vertex
        south_pole_index = self._vertices_count * self._vertices_count
        south_pole_edges = np.stack((phi_indices[-1, :], np.full(self._vertices_count, south_pole_index)), axis=1)

        return np.vstack((horizontal_edges, vertical_edges, last_to_first_edges, south_pole_edges))

    def get_vertices_count(self) -> int:
        return self._vertices_count