from numpy import tan, radians


class ProjectionMatrix:
    INITIAL_FOV = 90
    DISTANCE_FAR_PLANE = 1000
    DISTANCE_NEAR_PLANE = 0.1
    INITIAL_ASPECT_RATIO = 1

    def __init__(self, 
                 fov: int = INITIAL_FOV, 
                 aspect_ratio: float = INITIAL_ASPECT_RATIO, 
                 distance_far_plane: float = DISTANCE_FAR_PLANE,
                 distance_near_plane: float = DISTANCE_NEAR_PLANE) -> None:
        self._fov = fov
        self._aspect_ratio = aspect_ratio
        self._distance_far_plane = distance_far_plane
        self._distance_near_plane = distance_near_plane

    def get_matrix(self):
        scale_x = (1 / tan(radians(self._fov / 2))) / self._aspect_ratio
        scale_y = 1 / tan(radians(self._fov / 2))
        scale_z = ((self._distance_far_plane + self._distance_near_plane) * -1) / (self._distance_far_plane - self._distance_near_plane)
        translate_z = (-2 * self._distance_far_plane * self._distance_near_plane) / (self._distance_far_plane - self._distance_near_plane)
    
        return [
            [scale_x, 0, 0, 0],
            [0, scale_y, 0, 0],
            [0, 0, scale_z, translate_z],
            [0, 0, -1, 0]
        ]
    
    def update(self, 
               fov: int = None,
               aspect_ratio: float = None,
               distance_far_plane: float = None,
               distance_near_plane: float = None) -> None:
        self._fov = self._fov if fov is None else fov
        self._aspect_ratio = self._aspect_ratio if aspect_ratio is None else aspect_ratio
        self._distance_far_plane = self._distance_far_plane if distance_far_plane is None else distance_far_plane
        self._distance_near_plane = self._distance_near_plane if distance_near_plane is None else distance_near_plane