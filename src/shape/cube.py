from typing import List, Tuple
from src.shape.shape import Shape
from src.vector3 import Vector3


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

        self._near_left_up = self.__calculate_near_left_up()
        self._far_right_bottom = self.__calculate_far_right_bottom()

    def __calculate_near_left_up(self) -> Vector3:
        return Vector3(self._origin.x - self._width / 2, self._origin.y + self._height / 2, self._origin.z - self._depth / 2)
    
    def __calculate_far_right_bottom(self) -> Vector3:
        return Vector3(self._origin.x + self._width / 2, self._origin.y - self._height / 2, self._origin.z + self._depth / 2)
    
    def get_vertices(self) -> List[Vector3]:
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




    # EDGES = [
    #         (0, 1), (1, 2), (2, 3), (3, 0),  # Spigoli superiore
    #         (4, 5), (5, 7), (7, 6), (6, 4),  # Spigoli inferiore
    #         (0, 4), (1, 5), (2, 7), (3, 6)   # Spigoli verticali
    #     ]

    # def __init__(self, near_front_left: Vector3, far_back_right: Vector3, color: str = "black", stroke_width: int = 2) -> None:
    #     self.__check_coordinates_validity(near_front_left, far_back_right)

    #     self.near_front_left: Vector3 = near_front_left
    #     self.far_back_right: Vector3 = far_back_right
    #     self.color: str = color
    #     self.stroke_width: int = stroke_width

    #     difference = self.far_back_right - self.near_front_left
    #     self.width =  abs(difference.x)
    #     self.height = abs(difference.y)
    #     self.depth = abs(difference.z)

    #     self.vertices: list = self.__calculate_vertices()

    # def __check_coordinates_validity(self, near_front_left: Vector3, far_back_right: Vector3) -> None:
    #     if near_front_left.x >= far_back_right.x or near_front_left.y <= far_back_right.y or near_front_left.z >= far_back_right.z:
    #         raise ValueError("Invalid coordinates: near_front_left must be less than far_back_right")

    # def __calculate_vertices(self) -> list:
    #     return [
    #         self.near_front_left,
    #         Vector3(self.far_back_right.x, self.near_front_left.y, self.near_front_left.z),
    #         Vector3(self.far_back_right.x, self.far_back_right.y, self.near_front_left.z),
    #         Vector3(self.near_front_left.x, self.far_back_right.y, self.near_front_left.z),
    #         Vector3(self.near_front_left.x, self.near_front_left.y, self.far_back_right.z),
    #         Vector3(self.far_back_right.x, self.near_front_left.y, self.far_back_right.z),
    #         Vector3(self.near_front_left.x, self.far_back_right.y, self.far_back_right.z),
    #         self.far_back_right,
    #     ]
    
    # def get_edges(self, vertex: Vector3) -> list:
    #     return [(vertex[start], vertex[end]) for start, end in Cube.EDGES]
    
    # def get_origin(self) -> Vector3:
    #     return Vector3(
    #         (self.near_front_left.x + self.far_back_right.x) / 2, 
    #         (self.near_front_left.y + self.far_back_right.y) / 2, 
    #         (self.near_front_left.z + self.far_back_right.z) / 2)
    
    # def get_vertices(self) -> list:
    #     return self.vertices

    # def update_near_front_left(self, vector: Vector3) -> None:
    #     self.near_front_left = vector
    #     self.width = self.far_back_right.x - self.near_front_left.x
    #     self.height = self.near_front_left.y - self.far_back_right.y
    #     self.depth = self.far_back_right.z - self.near_front_left.z
    #     self.vertices = self.__calculate_vertices()

    # def update_far_back_right(self, vector: Vector3) -> None:
    #     self.far_back_right = vector
    #     self.width = self.far_back_right.x - self.near_front_left.x
    #     self.height = self.near_front_left.y - self.far_back_right.y
    #     self.depth = self.far_back_right.z - self.near_front_left.z
    #     self.vertices = self.__calculate_vertices()