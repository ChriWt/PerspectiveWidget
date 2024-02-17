import math
from typing import List, Optional, Tuple
from src.shape.shape import Shape
from src.vector3 import Vector3


class Piramid(Shape):

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
        super().__init__(origin, max(vertices_count, 3), width, height, depth, rotation_x, rotation_y, rotation_z, velocity)

    def get_vertices(self) -> List[Vector3]:
        vertices = []
        vertices.append(Vector3(self._origin.x, self._origin.y + self._height, self._origin.z))

        alpha = 2 * math.pi / self._vertices_count

        for i in range(self._vertices_count):
            x = self._origin.x + self._width * math.cos(i * alpha)
            y = self._origin.y
            z = self._origin.z + self._depth * math.sin(i * alpha)
            vertices.append(Vector3(x, y, z))
        
        return vertices
        

    def get_edges(self) -> List[Tuple[int, int]]:
        edges = []
        for i in range(1, self._vertices_count):
            edges.append((0, i))
            edges.append((i, i + 1))
        edges.append((0, self._vertices_count))
        edges.append((1, self._vertices_count))
        return edges