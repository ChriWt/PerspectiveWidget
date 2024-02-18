from src.rendering.rendererProperties import RendererProperties
from src.shape.shape import Shape
from src.utils.vector3 import Vector3

from numpy import array, radians, sin, cos
from tkinter import Canvas
import time


class ShapeRenderer: 

    EDGES_COLOR = "white"

    def __init__(self, canvas: Canvas, renderer_properties: RendererProperties) -> None:
        self._canvas = canvas
        self._renderer_properties = renderer_properties

    def render(self, shape: Shape) -> None:
        if shape is None: 
            return
        
        # start = time.time()
        
        self._rendering_shape = shape
        
        vertices = shape.get_vertices()
        vertices = [self.__apply_projection(vertex) for vertex in vertices]
        
        edges = shape.get_edges()

        for edge in edges:
            self._canvas.create_line(vertices[edge[0]].x, vertices[edge[0]].y, vertices[edge[1]].x, vertices[edge[1]].y, fill=self.EDGES_COLOR, width=1)

        # print(f"Rendering time: {time.time() - start:.4f}s")

    def __apply_projection(self, vertex: Vector3) -> None:
        origin = self._rendering_shape.get_origin()
        centered_vertex = vertex - origin

        vertex_4d = array([centered_vertex.x, centered_vertex.y, centered_vertex.z, 1])

        rotated_vertex_4d = self.__apply_rotation(vertex_4d)

        translated_vertex_4d = self.__translate_vertex(rotated_vertex_4d, self._rendering_shape._velocity)

        projected_vertex = self._renderer_properties.get_projection_matrix() @ translated_vertex_4d

        projected_vertex = self.__normalize_projected_vertex(projected_vertex)

        scale = self._renderer_properties.get_scale()
        offset_x = self._renderer_properties.get_offset_x()
        offset_y = self._renderer_properties.get_offset_y()

        return Vector3(projected_vertex.x * scale + offset_x, projected_vertex.y * scale + offset_y, projected_vertex.z)

    def __apply_rotation(self, vertex_4d: array) -> array:
        rotated_vertex_4d = self.__rotation_matrix_y(self._rendering_shape._rotation_y) @ \
                            self.__rotation_matrix_x(self._rendering_shape._rotation_x) @ \
                            self.__rotation_matrix_z(self._rendering_shape._rotation_z) @ \
                            vertex_4d

        origin = self._rendering_shape.get_origin()

        return array([
                rotated_vertex_4d[0] + origin.x,
                rotated_vertex_4d[1] + origin.y,
                rotated_vertex_4d[2] + origin.z,
                1
            ])
    
    def __normalize_projected_vertex(self, projected_vertex: array) -> Vector3:
        if projected_vertex[3] != 0:  # Avoid division by zero
            normalized_vertex = projected_vertex / projected_vertex[3]  # Perspective divide
        else:
            normalized_vertex = projected_vertex  # This case should ideally not occur
        return Vector3(normalized_vertex[0], normalized_vertex[1], normalized_vertex[2])

    @staticmethod
    def __rotation_matrix_x(angle: float) -> array:
        angle = radians(angle)
        return array([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def __rotation_matrix_y(angle: float) -> array:
        angle = radians(angle)
        return array([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def __rotation_matrix_z(angle: float) -> array:
        angle = radians(angle)
        return array([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def __translate_vertex(vertex_4d: array, translation: Vector3) -> array:
        return array([
            vertex_4d[0] + -translation.x,
            vertex_4d[1] + -translation.y,
            vertex_4d[2] + translation.z,
            1
        ])