from cube import Cube
from cubeVisualizer import CubeVisualizer
from vector3 import Vector3

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


if __name__ == "__main__":
    APP_WIDHT = 1200
    APP_HEIGHT = 800

    root = Main(width=APP_WIDHT, height=APP_HEIGHT)
    root.geometry(f"{APP_WIDHT}x{APP_HEIGHT}+{int(root.winfo_screenwidth()/2 - APP_WIDHT/2)}+{int(root.winfo_screenheight()/2 - APP_HEIGHT/2)}")
    root.add_cube(Cube(Vector3(50, 200, 50), Vector3(200, 50, 200)))
    root.mainloop()

    