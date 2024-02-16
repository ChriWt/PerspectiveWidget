from numpy import array, radians, sin, cos
from abc import ABC, abstractmethod
from src.rendering.projectionMatrix import ProjectionMatrix
from src.shape.shape import Shape
from src.vector3 import Vector3
from tkinter import Canvas


class ShapeRendering(ABC):

    def __init__(self, canvas: Canvas, projection_matrix: ProjectionMatrix) -> None:
        self._canvas = canvas
        self._projection_matrix = projection_matrix

    @abstractmethod
    def render(self, shape: Shape) -> None:
        pass

    @staticmethod
    def _rotation_matrix_x(angle: float):
        angle = radians(angle)
        return array([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def _rotation_matrix_y(angle: float) -> array:
        angle = radians(angle)
        return array([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def _rotation_matrix_z(angle: float):
        angle = radians(angle)
        return array([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    @staticmethod
    def _translate_vertex(vertex_4d: array, translation: Vector3) -> array:
        return array([
            vertex_4d[0] + -translation.x,
            vertex_4d[1] + -translation.y,
            vertex_4d[2] + translation.z,
            1
        ])