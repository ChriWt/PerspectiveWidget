import time
from src.rendering.projectionMatrix import ProjectionMatrix
from src.rendering.shapeRendering import ShapeRendering
from src.shape.cube import Cube
from src.shape.shape import Shape
from src.vector3 import Vector3
from tkinter import Canvas
from numpy import array


class CubeRendering(ShapeRendering):

    def __init__(self, canvas: Canvas, projection_matrix: ProjectionMatrix) -> None:
        super().__init__(canvas, projection_matrix)

    def render(self, shape: Shape) -> None:
        if shape is None: 
            return
        
        start = time.time()
        
        self._cube = shape

        vertices = shape.get_vertices()
        vertices = [self.__apply_projection(vertex) for vertex in vertices]

        edges = shape.get_edges()

        for edge in edges:
            self._canvas.create_line(vertices[edge[0]].x, vertices[edge[0]].y, vertices[edge[1]].x, vertices[edge[1]].y, fill="black", width=1)

        print(f"Rendering time: {time.time() - start:.4f} seconds")


    def __apply_projection(self, vertex: Vector3) -> None:
        origin = self._cube.get_origin()
        centered_vertex = vertex - origin
        vertex_4d = array([centered_vertex.x, centered_vertex.y, centered_vertex.z, 1])

        rotated_vertex_4d = self.__apply_rotation(vertex_4d)

        translated_vertex_4d = self._translate_vertex(rotated_vertex_4d, self._cube._velocity)

        projected_vertex = self._projection_matrix.get_matrix() @ translated_vertex_4d

        projected_vertex = self.__normalize_projected_vertex(projected_vertex)

        # TODO deve essere dinamico
        scale = 300
        offset_x = 400
        offset_y = 400

        return Vector3(projected_vertex.x * scale + offset_x, projected_vertex.y * scale + offset_y, projected_vertex.z)


    def __apply_rotation(self, vertex_4d: array) -> array:
        rotated_vertex_4d = self._rotation_matrix_y(self._cube._rotation_y) @ \
                            self._rotation_matrix_x(self._cube._rotation_x) @ \
                            self._rotation_matrix_z(self._cube._rotation_z) @ \
                            vertex_4d
    
        origin = self._cube.get_origin()
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
    
    # def do_something(self):
    #     print("do something - CUBE RENDERING")