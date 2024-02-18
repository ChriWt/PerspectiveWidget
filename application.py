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

    root = Main(width=APP_WIDHT, height=APP_HEIGHT)
    root.geometry(f"{APP_WIDHT}x{APP_HEIGHT}+{int(root.winfo_screenwidth()/2 - APP_WIDHT/2)}+{int(root.winfo_screenheight()/2 - APP_HEIGHT/2)}")
    
    root.display_cilinder()
    root.mainloop()

    