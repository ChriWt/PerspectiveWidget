from random import randint
from customtkinter import CTkFrame, CTkCanvas, IntVar, DoubleVar, CTkSlider, CTkLabel, CTkButton
from numpy import tan, array, radians, sin, cos
from src.rendering.shapeRenderer import ShapeRenderer
from src.rendering.rendererProperties import RendererProperties
from src.shape.shape import Shape

from src.shape.cube import Cube
from src.vector3 import Vector3

    
class Canvas3DRenderer(CTkFrame):

    HORIZONTAL = "horizontal"
    VERTICAL = "vertical"

    # Initial Field of View, Scale, and Offset Constants
    INITIAL_FOV = 90
    INITIAL_SCALE = 150

    # Projection Matrix Distance Constants
    DISTANCE_FAR_PLANE = 1000
    DISTANCE_NEAR_PLANE = 0.1

    # Initial Rotation and Translation Constants
    INITIAL_ROTATION_X = 0
    INITIAL_ROTATION_Y = 0
    INITIAL_ROTATION_Z = 0
    INITIAL_TRANSLATION_X = 200
    INITIAL_TRANSLATION_Y = 200
    INITIAL_TRANSLATION_Z = 200

    # Cube Dimension Constants
    INITIAL_CUBE_WIDTH = 1
    INITIAL_CUBE_HEIGHT = 1
    INITIAL_CUBE_DEPTH = 1

    # Slider Range Constants
    FOV_SLIDER_RANGE = (1, 179)  # degrees
    SCALE_SLIDER_RANGE = (1, 1000)
    OFFSET_X_SLIDER_RANGE = (0, 1920)
    OFFSET_Y_SLIDER_RANGE = (0, 1080)
    ASPECT_RATIO_SLIDER_RANGE = (0.1, 3)
    ROTATION_SLIDER_RANGE = (0, 360)  # degrees for X, Y, Z
    TRANSLATION_SLIDER_RANGE = (-1500, 1500)  # for X and Y, Z is (0, 1000)
    TRANSLATION_Z_SLIDER_RANGE = (0, 5000)
    CUBE_DIMENSION_SLIDER_RANGE = (1, 500)  # for width, height, depth
    SHAPE_VERTICES_SLIDER_RANGE = (4, 30)

    # Mouse Interaction Constants
    TRANSLATION_Z_INCREMENT = 10  # value for translation Z on mouse wheel event

    # UI Constants
    CANVAS_BACKGROUND_COLOR = "white"
    FOCAL_POINT_COLOR = "red"
    FOCAL_POINT_SIZE_OFFSETS = (-3, 3)  # Used for drawing the oval representing the focal point

        
    def __init__(self, 
                 *args, 
                 width: int, 
                 height: int, 
                 orientation: str = VERTICAL, 
                 show_options: bool = True, 
                 show_canvas_options: bool = True, 
                 show_rotation_options: bool = True,
                 show_translation_options: bool = True,
                 show_cube_options: bool = True,
                 **kwargs):
        super().__init__(*args, width=width, height=height, **kwargs)

        self._width = width
        self._height = height
        self._orientation = orientation
        self._show_options = show_options
        self._show_canvas_options = show_canvas_options
        self._show_rotation_options = show_rotation_options
        self._show_translation_options = show_translation_options
        self._show_cube_options = show_cube_options
        self._renderer_properties = None

        self.__init_variables()
        self.__init_renderer_properties()
        self.__init_UI()
        self.__init_variable_trace()
        self.__bind_size_change()
        self.__init_renderer()
        self.__display_focal_point()

    def __init_variables(self):
        self._cube = None
        self._fov = IntVar(value=self.INITIAL_FOV)
        self._scale = DoubleVar(value=self.INITIAL_SCALE)
        self._offset_x = IntVar(value=self._width / 2)
        self._offset_y = IntVar(value=self._height / 2)
        self._aspect_ratio = DoubleVar(value=1)
        self._distance_far_plane = self.DISTANCE_FAR_PLANE
        self._distance_near_plane = self.DISTANCE_NEAR_PLANE
        self._rotation_x = IntVar(value=self.INITIAL_ROTATION_X)
        self._rotation_y = IntVar(value=self.INITIAL_ROTATION_Y)
        self._rotation_z = IntVar(value=self.INITIAL_ROTATION_Z)
        self._translation_x = IntVar(value=self.INITIAL_TRANSLATION_X)
        self._translation_y = IntVar(value=self.INITIAL_TRANSLATION_Y)
        self._translation_z = IntVar(value=self.INITIAL_TRANSLATION_Z)
        self._cube_width = IntVar(value=self.INITIAL_CUBE_WIDTH)
        self._cube_height = IntVar(value=self.INITIAL_CUBE_HEIGHT)
        self._cube_depth = IntVar(value=self.INITIAL_CUBE_DEPTH)
        self._shape_vertices = IntVar(value=0)

    def __init_renderer_properties(self) -> None:
        self._renderer_properties = RendererProperties(
            fov=self._fov.get(), 
            aspect_ratio=self._aspect_ratio.get(),
            offset_x=self._offset_x.get(),
            offset_y=self._offset_y.get())

    def __init_UI(self):
        self._canvas = CTkCanvas(master=self, bg=self.CANVAS_BACKGROUND_COLOR)
        self.__init_canvas_bindings()
        self.__init_frames()
        self.__init_components()

    def __init_canvas_bindings(self):
        self.left_mouse_dragging_start = None
        self.right_mouse_dragging_start = None

        def on_mouse_left_down(event):
            self.left_mouse_dragging_start = (event.x, event.y)

        def on_mouse_left_move(event):
            if self.left_mouse_dragging_start is not None:
                current_position = (event.x, event.y)
                delta_x = current_position[0] - self.left_mouse_dragging_start[0]
                delta_y = current_position[1] - self.left_mouse_dragging_start[1]

                move_x = max(self._translation_x.get() + delta_x, self.TRANSLATION_SLIDER_RANGE[0])
                move_y = max(self._translation_y.get() + delta_y, self.TRANSLATION_SLIDER_RANGE[0])

                self._translation_x.set(min(move_x, self.TRANSLATION_SLIDER_RANGE[1]))
                self._translation_y.set(min(move_y, self.TRANSLATION_SLIDER_RANGE[1]))

                self.left_mouse_dragging_start = current_position
                self.__update_labels()

        def on_mouse_left_up(_):
            self.left_mouse_dragging_start = None

        def on_mouse_wheel(event):
            if event.delta > 0:
                self._translation_z.set(min(self._translation_z.get() + self.TRANSLATION_Z_INCREMENT, self.TRANSLATION_Z_SLIDER_RANGE[1]))
            else:
                self._translation_z.set(max(self._translation_z.get() - self.TRANSLATION_Z_INCREMENT, self.TRANSLATION_Z_SLIDER_RANGE[0]))
            self.__update_labels()

        def on_mouse_right_down(event):
            self.right_mouse_dragging_start = (event.x, event.y)
        
        def on_mouse_right_move(event):
            if self.right_mouse_dragging_start is not None:
                current_position = (event.x, event.y)
                delta_x = current_position[0] - self.right_mouse_dragging_start[0]
                delta_y = current_position[1] - self.right_mouse_dragging_start[1]

                self._rotation_y.set((self._rotation_y.get() + delta_y) % self.ROTATION_SLIDER_RANGE[1])
                self._rotation_x.set((self._rotation_x.get() + delta_x) % self.ROTATION_SLIDER_RANGE[1])

                self.right_mouse_dragging_start = current_position
                self.__update_labels()

        def on_mouse_right_up(_):
            self.right_mouse_dragging_start = None

        self._canvas.bind("<Button-1>", on_mouse_left_down)
        self._canvas.bind("<B1-Motion>", on_mouse_left_move)
        self._canvas.bind("<ButtonRelease-1>", on_mouse_left_up)
        self._canvas.bind("<MouseWheel>", on_mouse_wheel)

        self._canvas.bind("<Button-3>", on_mouse_right_down)
        self._canvas.bind("<B3-Motion>", on_mouse_right_move)
        self._canvas.bind("<ButtonRelease-3>", on_mouse_right_up)

    def __init_frames(self):
        self._option_frame = CTkFrame(master=self, width=1, height=1)
        self._canvas_options_frame = CTkFrame(master=self._option_frame, width=1, height=1)
        self._rotation_options_frame = CTkFrame(master=self._option_frame, width=1, height=1)
        self._translation_options_frame = CTkFrame(master=self._option_frame, width=1, height=1)
        self._cube_options_frame = CTkFrame(master=self._option_frame, width=1, height=1)

    def __init_components(self):
        frame = CTkFrame(master=self._canvas_options_frame)
        self._fov_label = CTkLabel(master=frame, text=f"Fov ({self._fov.get()})")
        self._fov_label.pack(side="top")
        CTkSlider(master=frame, variable=self._fov, from_=self.FOV_SLIDER_RANGE[0], to=self.FOV_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._canvas_options_frame)
        self._scale_label = CTkLabel(master=frame, text=f"Scale ({self._scale.get()})")
        self._scale_label.pack(side="top")
        CTkSlider(master=frame, variable=self._scale, from_=self.SCALE_SLIDER_RANGE[0], to=self.SCALE_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")
        
        frame = CTkFrame(master=self._canvas_options_frame)
        self._offset_x_label = CTkLabel(master=frame, text=f"Offset X ({self._offset_x.get()})")
        self._offset_x_label.pack(side="top")
        CTkSlider(master=frame, variable=self._offset_x, from_=self.OFFSET_X_SLIDER_RANGE[0], to=self.OFFSET_X_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._canvas_options_frame)
        self._offset_y_label = CTkLabel(master=frame, text=f"Offset Y ({self._offset_y.get()})")
        self._offset_y_label.pack(side="top")
        CTkSlider(master=frame, variable=self._offset_y, from_=self.OFFSET_Y_SLIDER_RANGE[0], to=self.OFFSET_Y_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._rotation_options_frame)
        self._rotation_x_label = CTkLabel(master=frame, text=f"Rotation X ({self._rotation_x.get()})")
        self._rotation_x_label.pack(side="top")
        CTkSlider(master=frame, variable=self._rotation_x, from_=self.ROTATION_SLIDER_RANGE[0], to=self.ROTATION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")
    
        frame = CTkFrame(master=self._rotation_options_frame)
        self._rotation_y_label = CTkLabel(master=frame, text=f"Rotation Y ({self._rotation_y.get()})")
        self._rotation_y_label.pack(side="top")
        CTkSlider(master=frame, variable=self._rotation_y, from_=self.ROTATION_SLIDER_RANGE[0], to=self.ROTATION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")
    
        frame = CTkFrame(master=self._rotation_options_frame)
        self._rotation_z_label = CTkLabel(master=frame, text=f"Rotation Z ({self._rotation_z.get()})")
        self._rotation_z_label.pack(side="top")
        CTkSlider(master=frame, variable=self._rotation_z, from_=self.ROTATION_SLIDER_RANGE[0], to=self.ROTATION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._translation_options_frame)
        self._translation_x_label = CTkLabel(master=frame, text=f"Translation X ({self._translation_x.get()})")
        self._translation_x_label.pack(side="top")
        CTkSlider(master=frame, variable=self._translation_x, from_=self.TRANSLATION_SLIDER_RANGE[0], to=self.TRANSLATION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._translation_options_frame)
        self._translation_y_label = CTkLabel(master=frame, text=f"Translation Y ({self._translation_y.get()})")
        self._translation_y_label.pack(side="top")
        CTkSlider(master=frame, variable=self._translation_y, from_=self.TRANSLATION_SLIDER_RANGE[0], to=self.TRANSLATION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._translation_options_frame)
        self._translation_z_label = CTkLabel(master=frame, text=f"Translation Z ({self._translation_z.get()})")
        self._translation_z_label.pack(side="top")
        CTkSlider(master=frame, variable=self._translation_z, from_=self.TRANSLATION_Z_SLIDER_RANGE[0], to=self.TRANSLATION_Z_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")
    
        frame = CTkFrame(master=self._cube_options_frame)
        self._cube_width_label = CTkLabel(master=frame, text=f"Cube Width ({self._cube_width.get()})")
        self._cube_width_label.pack(side="top")
        CTkSlider(master=frame, variable=self._cube_width, from_=self.CUBE_DIMENSION_SLIDER_RANGE[0], to=self.CUBE_DIMENSION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._cube_options_frame)
        self._cube_height_label = CTkLabel(master=frame, text=f"Cube Height ({self._cube_height.get()})")
        self._cube_height_label.pack(side="top")
        CTkSlider(master=frame, variable=self._cube_height, from_=self.CUBE_DIMENSION_SLIDER_RANGE[0], to=self.CUBE_DIMENSION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._cube_options_frame)
        self._cube_depth_label = CTkLabel(master=frame, text=f"Cube Depth ({self._cube_depth.get()})")
        self._cube_depth_label.pack(side="top")
        CTkSlider(master=frame, variable=self._cube_depth, from_=self.CUBE_DIMENSION_SLIDER_RANGE[0], to=self.CUBE_DIMENSION_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        frame = CTkFrame(master=self._cube_options_frame)
        self._shape_vertices_label = CTkLabel(master=frame, text=f"Cube Vertices ({self._shape_vertices.get()})")
        self._shape_vertices_label.pack(side="top")
        CTkSlider(master=frame, variable=self._shape_vertices, from_=self.SHAPE_VERTICES_SLIDER_RANGE[0], to=self.SHAPE_VERTICES_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
        frame.pack(side="left" if self._orientation == self.HORIZONTAL else "top")

        CTkButton(master=self._option_frame, text="Randomize", command=self.__randomize_shape_properties).pack(side="bottom" if self._orientation == self.VERTICAL else "right", padx=10 if self._orientation == self.HORIZONTAL else 0, pady=20 if self._orientation == self.VERTICAL else 10)

    def __randomize_shape_properties(self):
        self._rotation_x.set(randint(self.ROTATION_SLIDER_RANGE[0], self.ROTATION_SLIDER_RANGE[1]))
        self._rotation_y.set(randint(self.ROTATION_SLIDER_RANGE[0], self.ROTATION_SLIDER_RANGE[1]))
        self._rotation_z.set(randint(self.ROTATION_SLIDER_RANGE[0], self.ROTATION_SLIDER_RANGE[1]))

        self.__update_labels()
        self.__render()

    def __init_variable_trace(self):
        self._fov.trace_add("write", self.__update_fov)
        self._scale.trace_add("write", self.__update_scale)
        self._offset_x.trace_add("write", self.__update_offset_x)
        self._offset_y.trace_add("write", self.__update_offset_y)
        self._aspect_ratio.trace_add("write", self.__update_aspect_ratio)
        self._rotation_x.trace_add("write", self.__update_shape_rotation)
        self._rotation_y.trace_add("write", self.__update_shape_rotation)
        self._rotation_z.trace_add("write", self.__update_shape_rotation)
        self._translation_x.trace_add("write", self.__update_shape_position)
        self._translation_y.trace_add("write", self.__update_shape_position)
        self._translation_z.trace_add("write", self.__update_shape_position)
        self._cube_width.trace_add("write", self.__update_shape_size)
        self._cube_height.trace_add("write", self.__update_shape_size)
        self._cube_depth.trace_add("write", self.__update_shape_size)
        self._shape_vertices.trace_add("write", self.__update_shape_vertices)

    def __update_fov(self, *_) -> None:
        self._renderer_properties.update(fov=self._fov.get())
        self.__render()
            
    def __update_scale(self, *_) -> None:
        self._renderer_properties.update(scale=self._scale.get())
        self.__render()

    def __update_offset_x(self, *_) -> None:
        self._renderer_properties.update(offset_x=self._offset_x.get())
        self.__render()

    def __update_offset_y(self, *_) -> None:
        self._renderer_properties.update(offset_y=self._offset_y.get())
        self.__render()

    def __update_aspect_ratio(self, *_) -> None:
        self._renderer_properties.update(aspect_ratio=self._aspect_ratio.get())
        self.__render()
        
    def __update_shape_position(self, *_) -> None:
        self._shape._velocity = Vector3(self._translation_x.get(), self._translation_y.get(), self._translation_z.get())
        self.__render()

    def __update_shape_size(self, *_) -> None:
        self._shape._width = self._cube_width.get()
        self._shape._height = self._cube_height.get()
        self._shape._depth = self._cube_depth.get()
        self.__render()

    def __update_shape_vertices(self, *_) -> None:
        self._shape._vertices_count = self._shape_vertices.get()
        self.__render()

    def __update_shape_rotation(self, *_) -> None:
        self._shape._rotation_x = self._rotation_x.get()
        self._shape._rotation_y = self._rotation_y.get()
        self._shape._rotation_z = self._rotation_z.get()
        self.__render()
    
    def __display_focal_point(self) -> None:
        self._canvas.create_oval(
            self._offset_x.get() + self.FOCAL_POINT_SIZE_OFFSETS[0], 
            self._offset_y.get() + self.FOCAL_POINT_SIZE_OFFSETS[0],
            self._offset_x.get() + self.FOCAL_POINT_SIZE_OFFSETS[1],
            self._offset_y.get() + self.FOCAL_POINT_SIZE_OFFSETS[1],
            fill=self.FOCAL_POINT_COLOR, 
            outline=self.FOCAL_POINT_COLOR)
        
    def __display_horizontal_line(self) -> None:
        self._canvas.create_line(0, self._offset_y.get(), 1920, self._offset_y.get(), fill="black", width=1)

    def __update_labels(self, *args):
        self._fov_label.configure(text=f"Fov ({self._fov.get()})")
        self._scale_label.configure(text=f"Scale ({round(self._scale.get(), 1)})")
        self._offset_x_label.configure(text=f"Offset X ({self._offset_x.get()})")
        self._offset_y_label.configure(text=f"Offset Y ({self._offset_y.get()})")
        self._rotation_x_label.configure(text=f"Rotation X ({self._rotation_x.get()})")
        self._rotation_y_label.configure(text=f"Rotation Y ({self._rotation_y.get()})")
        self._rotation_z_label.configure(text=f"Rotation Z ({self._rotation_z.get()})")
        self._translation_x_label.configure(text=f"Translation X ({self._translation_x.get()})")
        self._translation_y_label.configure(text=f"Translation Y ({self._translation_y.get()})")
        self._translation_z_label.configure(text=f"Translation Z ({self._translation_z.get()})")
        self._cube_width_label.configure(text=f"Cube Width ({self._cube_width.get()})")
        self._cube_height_label.configure(text=f"Cube Height ({self._cube_height.get()})")
        self._cube_depth_label.configure(text=f"Cube Depth ({self._cube_depth.get()})")
        self._shape_vertices_label.configure(text=f"Cube Vertices ({self._shape_vertices.get()})")
        
    def __bind_size_change(self) -> None:        
        self.bind("<Configure>", self.__on_size_change)

    def __init_renderer(self) -> None:
        self._renderer = ShapeRenderer(self._canvas, self._renderer_properties)

    def __on_size_change(self, event) -> None:
        if event.width == self._width and event.height == self._height:
            return
        print(event.width, event.height)
        self._offset_x.set(event.width / 2)
        self._offset_y.set(event.height / 2)
        self.__update_labels()
        self.__render()
    
    def pack(self, *args, **kwargs):
        super().pack(*args, **kwargs)
        self._canvas.pack(fill="both", expand=True, side="top" if self._orientation == self.HORIZONTAL else "left")

        if not self._show_options:
            return

        common_kwargs = {
            'side': 'left' if self._orientation == self.HORIZONTAL else 'top',
            'padx': 10 if self._orientation == self.HORIZONTAL else 0,
            'pady': 20 if self._orientation == self.VERTICAL else 10
        }

        self._option_frame.pack(side="bottom" if self._orientation == self.HORIZONTAL else "right")

        if self._show_canvas_options:
            self._canvas_options_frame.pack(**common_kwargs)
        
        if self._show_rotation_options:
            self._rotation_options_frame.pack(**common_kwargs)
        
        if self._show_translation_options:
            self._translation_options_frame.pack(**common_kwargs)
        
        if self._show_cube_options:
            self._cube_options_frame.pack(**common_kwargs)
            
    def add_shape(self, shape: Shape) -> None:
        self._shape = shape

        width, height, depth = shape.get_width(), shape.get_height(), shape.get_depth()
        translation = shape.get_velocity()
        vertices_count = shape.get_vertices_count()
        rotation_x = shape.get_rotation_x()
        rotation_y = shape.get_rotation_y()
        rotation_z = shape.get_rotation_z()

        self._cube_width.set(width)
        self._cube_height.set(height)
        self._cube_depth.set(depth)
        self._translation_x.set(translation.x)
        self._translation_y.set(translation.y)
        self._translation_z.set(translation.z)
        self._shape_vertices.set(vertices_count)
        self._rotation_x.set(rotation_x)
        self._rotation_y.set(rotation_y)
        self._rotation_z.set(rotation_z)
        self.__update_labels()        
        self._renderer.render(shape)

    def __render(self) -> None:
        self._canvas.delete("all")
        self.__display_focal_point()
        self.__display_horizontal_line()
        self._renderer.render(self._shape)