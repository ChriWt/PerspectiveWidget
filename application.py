from src.shape.shape import Shape
from src.shape.sphere import Sphere
from src.shape.cube import Cube
from src.perspectiveWidget import CubeVisualizer
from src.vector3 import Vector3

from customtkinter import CTk


class Main(CTk):

    def __init__(self, *args, width: int, height: int, **kwargs):
        super().__init__(*args, **kwargs)

        self.cube_visualizer = CubeVisualizer(
            master=self, 
            width=width,
            height=height)
        self.cube_visualizer.pack(fill="both", expand=True)

    def add_cube(self, cube: Cube) -> None:
        self.cube_visualizer.add_cube(cube)

    def add_shape(self, shape: Shape) -> None:
        self.cube_visualizer.add_shape(shape)


if __name__ == "__main__":
    APP_WIDHT = 1200
    APP_HEIGHT = 800

    root = Main(width=APP_WIDHT, height=APP_HEIGHT)
    root.geometry(f"{APP_WIDHT}x{APP_HEIGHT}+{int(root.winfo_screenwidth()/2 - APP_WIDHT/2)}+{int(root.winfo_screenheight()/2 - APP_HEIGHT/2)}")
    
    # root.add_shape(Sphere(Vector3(0, 0, 1024), vertices_count=15, width=400))
    root.add_shape(Cube(Vector3(0, 0, 240), width=200, height=200, depth=200))
    root.mainloop()

    