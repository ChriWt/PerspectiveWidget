from customtkinter import CTk

from src.canvas3DRenderer import Canvas3DRenderer


class Main(CTk):

    def __init__(self, *args, width: int, height: int, **kwargs):
        super().__init__(*args, **kwargs)

        self.shape_visualizer = Canvas3DRenderer(
            master=self,
            width=width,
            height=height)
        self.shape_visualizer.pack(fill="both", expand=True)

    def display_cube(self) -> None:
        self.shape_visualizer.display_cube()

    def display_piramid(self) -> None:
        self.shape_visualizer.display_piramid()

    def display_cilinder(self) -> None:
        self.shape_visualizer.display_cilinder()

    def display_sphere(self) -> None:
        self.shape_visualizer.display_sphere()


if __name__ == "__main__":
    APP_WIDHT = 1200
    APP_HEIGHT = 850
    import time


    
    
    delta_time = []

    # import sys
    # sys.path.append(r'./release/Release')
    # from CShape3D import Vector3, Shape3D, Cilinder, Sphere

    # for i in range(999):
    #     start = time.time()
    #     shape = Sphere(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 500, 200, 200, 200)
    #     shape.get_vertices()
    #     shape.get_edges()
    #     delta_time.append(time.time() - start)
    #     print(i)

    # print(sum(delta_time)/len(delta_time))




    # from src.shape.sphere import Sphere
    # from src.utils.vector3 import Vector3
    
    # for i in range(5):
    #     start = time.time()
    #     shape = Sphere(Vector3(0, 0, 0), 500, 200, 200, 200)
    #     shape.get_vertices()
    #     shape.get_edges()
    #     delta_time.append(time.time() - start)
    #     print(i)
    
    # print(sum(delta_time)/len(delta_time))













    # vector = Vector3(1, 2, 3) 
    # print(vector)

    # shape = Shape3D()
    # shape.setVerticeCount(20)
    # print(shape.getVerticeCount())

    root = Main(width=APP_WIDHT, height=APP_HEIGHT)
    root.geometry(f"{APP_WIDHT}x{APP_HEIGHT}+{int(root.winfo_screenwidth()/2 - APP_WIDHT/2)}+{int(root.winfo_screenheight()/2 - APP_HEIGHT/2)}")
    
    root.display_sphere()
    root.mainloop()

    