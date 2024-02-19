import time
from tkinter import Canvas

from CShape3D import RenderingProperties, Shape3D, Renderer


class ShapeRenderer: 

    EDGES_COLOR = "white"

    def __init__(self, canvas: Canvas, renderer_properties: RenderingProperties) -> None:
        self._canvas = canvas
        self._renderer = Renderer(renderer_properties)

    def render(self, shape: Shape3D) -> None:
        if shape is None: 
            return
        
        edges = self._renderer.render(shape)

        for edge in edges:
            self._canvas.create_line(edge.start.x, edge.start.y, edge.end.x, edge.end.y, fill=self.EDGES_COLOR, width=1)

    def set_rendering_properties(self, rendering_properties: RenderingProperties) -> None:
        self._renderer.set_rendering_properties(rendering_properties)