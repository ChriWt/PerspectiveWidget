from typing import List, Tuple
from src.shape.shape import Shape
from src.utils.vector3 import Vector3


class Cube(Shape):

    VERTICES_COUNT = 8

    def __init__(self, 
                 origin: Vector3, 
                 width: int = 0, 
                 height: int = 0, 
                 depth: int = 1,
                 rotation_x: int = 0, 
                 rotation_y: int = 0, 
                 rotation_z: int = 0) -> None:
        super().__init__(origin, self.VERTICES_COUNT, width, height, depth, rotation_x, rotation_y, rotation_z)

    def __calculate_near_left_up(self) -> Vector3:
        return Vector3(self._origin.x - self._width / 2, self._origin.y + self._height / 2, self._origin.z - self._depth / 2)
    
    def __calculate_far_right_bottom(self) -> Vector3:
        return Vector3(self._origin.x + self._width / 2, self._origin.y - self._height / 2, self._origin.z + self._depth / 2)
    
    def get_vertices(self) -> List[Vector3]:
        self._near_left_up = self.__calculate_near_left_up()
        self._far_right_bottom = self.__calculate_far_right_bottom()

        return [
            self._near_left_up,                                                                   # LEFT, TOP, NEAR
            Vector3(self._near_left_up.x, self._far_right_bottom.y, self._near_left_up.z),        # LEFT, BOT, NEAR
            Vector3(self._far_right_bottom.x, self._near_left_up.y, self._near_left_up.z),        # RIGHT, TOP, NEAR
            Vector3(self._far_right_bottom.x, self._far_right_bottom.y, self._near_left_up.z),    # RIGHT, BOT, NEAR
            self._far_right_bottom,                                                               # RIGHT, BOT, FAR
            Vector3(self._near_left_up.x, self._far_right_bottom.y, self._far_right_bottom.z),    # LEFT, BOT, FAR
            Vector3(self._near_left_up.x, self._near_left_up.y, self._far_right_bottom.z),        # LEFT, TOP, FAR
            Vector3(self._far_right_bottom.x, self._near_left_up.y, self._far_right_bottom.z)     # RIGHT, TOP, FAR
        ]


    def get_edges(self) -> List[Tuple[int, int]]:
        return [
            (0, 1), (1, 3), (3, 2), (2, 0),  # Edges of the near face
            (4, 5), (5, 6), (6, 7), (7, 4),  # Edges of the far face
            (0, 6), (1, 5), (2, 7), (3, 4)   # Side edges connecting near and far faces
        ]