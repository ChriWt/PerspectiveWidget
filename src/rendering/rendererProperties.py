from numpy import tan, radians


class RendererProperties:
    INITIAL_FOV = 90
    DISTANCE_FAR_PLANE = 1000
    DISTANCE_NEAR_PLANE = 0.1
    INITIAL_ASPECT_RATIO = 1
    INITIAL_SCALE = 150
    INITIAL_OFFSET_X = 400
    INITIAL_OFFSET_Y = 400

    def __init__(self, 
                 fov: int = INITIAL_FOV, 
                 aspect_ratio: float = INITIAL_ASPECT_RATIO, 
                 distance_far_plane: float = DISTANCE_FAR_PLANE,
                 distance_near_plane: float = DISTANCE_NEAR_PLANE,
                 scale: float = INITIAL_SCALE,
                 offset_x: int = INITIAL_OFFSET_X,
                 offset_y: int = INITIAL_OFFSET_Y) -> None:
        self._fov = fov
        self._aspect_ratio = aspect_ratio
        self._distance_far_plane = distance_far_plane
        self._distance_near_plane = distance_near_plane
        self._scale = scale
        self._offset_x = offset_x
        self._offset_y = offset_y
        self.__build_projection_matrix()

    def get_projection_matrix(self) -> list[list[float]]:
        return self._projection_matrix
    
    def get_scale(self) -> float:
        return self._scale
    
    def get_offset_x(self) -> int:
        return self._offset_x
    
    def get_offset_y(self) -> int:
        return self._offset_y
        
    def __build_projection_matrix(self) -> list[list[float]]:
        scale_x = (1 / tan(radians(self._fov / 2))) / self._aspect_ratio
        scale_y = 1 / tan(radians(self._fov / 2))
        scale_z = ((self._distance_far_plane + self._distance_near_plane) * -1) / (self._distance_far_plane - self._distance_near_plane)
        translate_z = (-2 * self._distance_far_plane * self._distance_near_plane) / (self._distance_far_plane - self._distance_near_plane)
    
        self._projection_matrix = [
            [scale_x, 0, 0, 0],
            [0, scale_y, 0, 0],
            [0, 0, scale_z, translate_z],
            [0, 0, -1, 0]
        ]
    
    def update(self, 
               fov: int = None,
               aspect_ratio: float = None,
               distance_far_plane: float = None,
               distance_near_plane: float = None,
               scale: float = None,
               offset_x: int = None,
               offset_y: int = None) -> None:
        self._fov = self._fov if fov is None else fov
        self._aspect_ratio = self._aspect_ratio if aspect_ratio is None else aspect_ratio
        self._distance_far_plane = self._distance_far_plane if distance_far_plane is None else distance_far_plane
        self._distance_near_plane = self._distance_near_plane if distance_near_plane is None else distance_near_plane
        self._scale = self._scale if scale is None else scale
        self._offset_x = self._offset_x if offset_x is None else offset_x
        self._offset_y = self._offset_y if offset_y is None else offset_y

        if fov is not None or aspect_ratio is not None:
            self.__build_projection_matrix()