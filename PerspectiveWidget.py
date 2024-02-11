from random import randint
from customtkinter import CTkFrame, CTkCanvas, IntVar, DoubleVar, CTkSlider, CTkLabel, CTkButton
from numpy import tan, array, radians, sin, cos

from cube import Cube
from vector3 import Vector3

    
class CubeVisualizer(CTkFrame):

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
    INITIAL_TRANSLATION_X = 120
    INITIAL_TRANSLATION_Y = 130
    INITIAL_TRANSLATION_Z = 70

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
    TRANSLATION_SLIDER_RANGE = (-1000, 1000)  # for X and Y, Z is (0, 1000)
    TRANSLATION_Z_SLIDER_RANGE = (0, 1000)
    CUBE_DIMENSION_SLIDER_RANGE = (1, 500)  # for width, height, depth

    # Mouse Interaction Constants
    TRANSLATION_Z_INCREMENT = 10  # value for translation Z on mouse wheel event

    # UI Constants
    CANVAS_BACKGROUND_COLOR = "white"
    FOCAL_POINT_COLOR = "grey"
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

        self.__init_variables()
        self.__init_UI()
        self.__init_variable_trace()
        self.__bind_size_change()

    def __init_variables(self):
        self._cube = None
        self._fov = IntVar(value=self.INITIAL_FOV)
        self._scale = DoubleVar(value=self.INITIAL_SCALE)
        self._offset_x = IntVar(value=self._width / 2)
        self._offset_y = IntVar(value=self._height / 2)
        self._aspect_ratio = DoubleVar(value=self._width / self._height)
        self._distance_far_plane = self.DISTANCE_FAR_PLANE
        self._distance_near_plane = self.DISTANCE_NEAR_PLANE
        self._projection_matrix = self.__create_projection_matrix()
        self._rotation_x = IntVar(value=self.INITIAL_ROTATION_X)
        self._rotation_y = IntVar(value=self.INITIAL_ROTATION_Y)
        self._rotation_z = IntVar(value=self.INITIAL_ROTATION_Z)
        self._translation_x = IntVar(value=self.INITIAL_TRANSLATION_X)
        self._translation_y = IntVar(value=self.INITIAL_TRANSLATION_Y)
        self._translation_z = IntVar(value=self.INITIAL_TRANSLATION_Z)
        self._cube_width = IntVar(value=self.INITIAL_CUBE_WIDTH)
        self._cube_height = IntVar(value=self.INITIAL_CUBE_HEIGHT)
        self._cube_depth = IntVar(value=self.INITIAL_CUBE_DEPTH)

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

        frame = CTkFrame(master=self._canvas_options_frame)
        self._aspect_ratio_label = CTkLabel(master=frame, text=f"Aspect Ratio ({round(self._aspect_ratio.get())})")
        self._aspect_ratio_label.pack(side="top")
        CTkSlider(master=frame, variable=self._aspect_ratio, from_=self.ASPECT_RATIO_SLIDER_RANGE[0], to=self.ASPECT_RATIO_SLIDER_RANGE[1], orientation=self.HORIZONTAL, command=self.__update_labels).pack(side="top")
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

        CTkButton(master=self._option_frame, text="Random Cube", command=self.__randomize_cube_properties).pack(side="bottom" if self._orientation == self.VERTICAL else "right", padx=10 if self._orientation == self.HORIZONTAL else 0, pady=20 if self._orientation == self.VERTICAL else 10)

    def __randomize_cube_properties(self):
        self._rotation_x.set(randint(self.ROTATION_SLIDER_RANGE[0], self.ROTATION_SLIDER_RANGE[1]))
        self._rotation_y.set(randint(self.ROTATION_SLIDER_RANGE[0], self.ROTATION_SLIDER_RANGE[1]))
        self._rotation_z.set(randint(self.ROTATION_SLIDER_RANGE[0], self.ROTATION_SLIDER_RANGE[1]))

        self.__update_labels()
        self.__draw_cube()

    def __init_variable_trace(self):
        self._fov.trace_add("write", self.__update_projection_matrix)
        self._scale.trace_add("write", self.__update_projection_matrix)
        self._offset_x.trace_add("write", self.__update_projection_matrix)
        self._offset_y.trace_add("write", self.__update_projection_matrix)
        self._aspect_ratio.trace_add("write", self.__update_projection_matrix)
        self._rotation_x.trace_add("write", lambda *args: self.__draw_cube())
        self._rotation_y.trace_add("write", lambda *args: self.__draw_cube())
        self._rotation_z.trace_add("write", lambda *args: self.__draw_cube())
        self._translation_x.trace_add("write", lambda *args: self.__draw_cube())
        self._translation_y.trace_add("write", lambda *args: self.__draw_cube())
        self._translation_z.trace_add("write", lambda *args: self.__draw_cube())
        self._cube_width.trace_add("write", lambda *args: self.__update_cube_size())
        self._cube_height.trace_add("write", lambda *args: self.__update_cube_size())
        self._cube_depth.trace_add("write", lambda *args: self.__update_cube_size())
    
    def __create_projection_matrix(self):
        scale_x = (1 / tan(radians(self._fov.get() / 2))) / self._aspect_ratio.get()
        scale_y = 1 / tan(radians(self._fov.get() / 2))
        scale_z = ((self._distance_far_plane + self._distance_near_plane) * -1) / (self._distance_far_plane - self._distance_near_plane)
        translate_z = (-2 * self._distance_far_plane * self._distance_near_plane) / (self._distance_far_plane - self._distance_near_plane)
    
        return [
            [scale_x, 0, 0, 0],
            [0, scale_y, 0, 0],
            [0, 0, scale_z, translate_z],
            [0, 0, -1, 0]
        ]

    def __update_projection_matrix(self, *args):
        self._projection_matrix = self.__create_projection_matrix()
        self.__draw_cube()

    def __draw_cube(self) -> None:
        if self._cube is None: 
            return
        
        self._canvas.delete("all")
        
        new_vertices = self.__calculate_vertices()

        for start, end in self._cube.get_edges(new_vertices):
            self._canvas.create_line(start.x, start.y, end.x, end.y, fill=self._cube.color, width=self._cube.stroke_width)

        self.__display_focal_point()
        
    def __calculate_vertices(self) -> list:
        new_vertices = []
        for vertex in self._cube.get_vertices():
            new_vertices.append(self.__apply_projection(vertex))
        return new_vertices

    def __apply_projection(self, vertex: Vector3) -> None:
        centered_vertex = vertex - self._cube.get_origin()

        vertex_4d = array([centered_vertex.x, centered_vertex.y, centered_vertex.z, 1])

        rotated_vertex_4d = self.__apply_rotation(vertex_4d)

        translated_vertex_4d = self.__translate_vertex(rotated_vertex_4d)

        projected_vertex = self._projection_matrix @ translated_vertex_4d
    
        projected_vertex = self.__normalize_projected_vertex(projected_vertex)

        x = projected_vertex[0] * self._scale.get() + self._offset_x.get()
        y = projected_vertex[1] * self._scale.get() + self._offset_y.get()

        return Vector3(x, y, projected_vertex[2])

    def __apply_rotation(self, vertex_4d: array) -> array:
        rotated_vertex_4d = self.__rotation_matrix_y(self._rotation_y.get()) @ \
                            self.__rotation_matrix_x(self._rotation_x.get()) @ \
                            self.__rotation_matrix_z(self._rotation_z.get()) @ \
                            vertex_4d
    
        origin = self._cube.get_origin()
        return array([
                rotated_vertex_4d[0] + origin.x,
                rotated_vertex_4d[1] + origin.y,
                rotated_vertex_4d[2] + origin.z,
                1
            ])

    def __rotation_matrix_x(self, angle: float):
        angle = radians(angle)
        return array([
            [cos(angle), 0, sin(angle), 0],
            [0, 1, 0, 0],
            [-sin(angle), 0, cos(angle), 0],
            [0, 0, 0, 1]
        ])

    def __rotation_matrix_y(self, angle: float) -> array:
        angle = radians(angle)
        return array([
            [1, 0, 0, 0],
            [0, cos(angle), -sin(angle), 0],
            [0, sin(angle), cos(angle), 0],
            [0, 0, 0, 1]
        ])

    def __rotation_matrix_z(self, angle: float):
        angle = radians(angle)
        return array([
            [cos(angle), -sin(angle), 0, 0],
            [sin(angle), cos(angle), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def __translate_vertex(self, vertex_4d: array) -> array:
        return array([
            vertex_4d[0] + -self._translation_x.get(),
            vertex_4d[1] + -self._translation_y.get(),
            vertex_4d[2] + self._translation_z.get(),
            1
        ])

    def __update_cube_size(self):
        half_width = self._cube_width.get() / 2
        half_height = self._cube_height.get() / 2
        half_depth = self._cube_depth.get() / 2
        origin = self._cube.get_origin()
        self._cube.update_near_front_left(Vector3(origin.x - half_width, origin.y - half_height, origin.z - half_depth))
        self._cube.update_far_back_right(Vector3(origin.x + half_width, origin.y + half_height, origin.z + half_depth))
        self.__draw_cube()

    def __normalize_projected_vertex(self, projected_vertex: array) -> array:
        vertex_4d = projected_vertex
        if vertex_4d[3] != 0:
            vertex_4d /= vertex_4d[3]
        return vertex_4d
    
    def __display_focal_point(self) -> None:
        self._canvas.create_oval(
            self._offset_x.get() + self.FOCAL_POINT_SIZE_OFFSETS[0], 
            self._offset_y.get() + self.FOCAL_POINT_SIZE_OFFSETS[0],
            self._offset_x.get() + self.FOCAL_POINT_SIZE_OFFSETS[1],
            self._offset_y.get() + self.FOCAL_POINT_SIZE_OFFSETS[1],
            fill=self.FOCAL_POINT_COLOR, 
            outline=self.FOCAL_POINT_COLOR)

    def __update_labels(self, *args):
        self._fov_label.configure(text=f"Fov ({self._fov.get()})")
        self._scale_label.configure(text=f"Scale ({round(self._scale.get(), 1)})")
        self._offset_x_label.configure(text=f"Offset X ({self._offset_x.get()})")
        self._offset_y_label.configure(text=f"Offset Y ({self._offset_y.get()})")
        self._aspect_ratio_label.configure(text=f"Aspect Ratio ({round(self._aspect_ratio.get(), 1)})")
        self._rotation_x_label.configure(text=f"Rotation X ({self._rotation_x.get()})")
        self._rotation_y_label.configure(text=f"Rotation Y ({self._rotation_y.get()})")
        self._rotation_z_label.configure(text=f"Rotation Z ({self._rotation_z.get()})")
        self._translation_x_label.configure(text=f"Translation X ({self._translation_x.get()})")
        self._translation_y_label.configure(text=f"Translation Y ({self._translation_y.get()})")
        self._translation_z_label.configure(text=f"Translation Z ({self._translation_z.get()})")
        self._cube_width_label.configure(text=f"Cube Width ({self._cube_width.get()})")
        self._cube_height_label.configure(text=f"Cube Height ({self._cube_height.get()})")
        self._cube_depth_label.configure(text=f"Cube Depth ({self._cube_depth.get()})")
        
    def __bind_size_change(self) -> None:
        self.bind("<Configure>", self.__on_size_change)

    def __on_size_change(self, event) -> None:
        if event.width == self._width and event.height == self._height:
            return
        self._offset_x.set(event.width / 2)
        self._offset_y.set(event.height / 2)
        self.__update_labels()
        self.__draw_cube()
    
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
    
    def add_cube(self, cube: Cube) -> None:
        self._cube = cube
        width, height, depth = cube.width, cube.height, cube.depth

        self._cube_width.set(width)
        self._cube_height.set(height)
        self._cube_depth.set(depth)
        
        self.__update_labels()
        self.__draw_cube()