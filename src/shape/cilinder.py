from typing import List, Optional, Tuple
import math

from src.utils.vector3 import Vector3
from src.shape.shape import Shape


class Cilinder(Shape):

    def __init__(self, 
                 origin: Vector3, 
                 vertices_count: int,
                 width: int, 
                 height: Optional[int] = None,
                 depth: Optional[int] = None,
                 rotation_x: int = 0,
                 rotation_y: int = 0,
                 rotation_z: int = 0,
                 velocity: Vector3 = Vector3(0, 0, 0)) -> None:
        super().__init__(origin, vertices_count, width, height, depth, rotation_x, rotation_y, rotation_z, velocity=velocity)
    
    def get_vertices(self) -> List[Vector3]:
        alpha = 2 * math.pi / self._vertices_count
        top_vertices = []
        bot_vertices = []
        for i in range(self._vertices_count):
            x = self._origin.x + self._width * math.cos(i * alpha)
            y = self._origin.y
            z = self._origin.z + self._depth * math.sin(i * alpha)
            top_vertices.append(Vector3(x, y - self._height, z))
            bot_vertices.append(Vector3(x, y + self._height, z))

        return top_vertices + bot_vertices


    def get_edges(self) -> List[Tuple[int, int]]:
        edges = []
        for i in range(self._vertices_count):
            edges.append((i, (i + 1) % self._vertices_count))
            edges.append((i + self._vertices_count, (i + 1) % self._vertices_count + self._vertices_count))
            edges.append((i, i + self._vertices_count))
        return edges