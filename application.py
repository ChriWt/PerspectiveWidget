from customtkinter import CTk

from src.canvas3DRenderer import Canvas3DRenderer
from src.utils.vector3 import Vector3

from src.shape.cilinder import Cilinder
from src.shape.piramid import Piramid
from src.shape.sphere import Sphere
from src.shape.shape import Shape
from src.shape.cube import Cube


class Main(CTk):

    def __init__(self, *args, width: int, height: int, **kwargs):
        super().__init__(*args, **kwargs)

        self.shape_visualizer = Canvas3DRenderer(
            master=self,
            width=width,
            height=height)
        self.shape_visualizer.pack(fill="both", expand=True)

    def add_shape(self, shape: Shape) -> None:
        self.shape_visualizer.add_shape(shape)


if __name__ == "__main__":
    APP_WIDHT = 1200
    APP_HEIGHT = 850

    root = Main(width=APP_WIDHT, height=APP_HEIGHT)
    root.geometry(f"{APP_WIDHT}x{APP_HEIGHT}+{int(root.winfo_screenwidth()/2 - APP_WIDHT/2)}+{int(root.winfo_screenheight()/2 - APP_HEIGHT/2)}")
    

    root.add_shape(Sphere(Vector3(0, 0, 500), vertices_count=8, width=400))
    # root.add_shape(Cube(Vector3(0, 0, 0), width=200, height=200, depth=200))
    # root.add_shape(Piramid(Vector3(0, 0, 1200), vertices_count=6, width=200, height=200, depth=200))
    # root.add_shape(Cilinder(Vector3(0, 0, 1200), vertices_count=6, width=200, height=200, depth=200))
    root.mainloop()

    