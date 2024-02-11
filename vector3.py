
class Vector3:
    # Constructor to initialize a 3D vector with x, y, and z components.
    def __init__(self, x, y, z=0):
        self.x = x
        self.y = y
        self.z = z

    # Overloads the addition operator to add two vectors.
    def __add__(self, other):
        # Returns a new Vector3 which is the sum of this vector and another.
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    # Overloads the subtraction operator to subtract two vectors.
    def __sub__(self, other):
        # Returns a new Vector3 which is the difference of this vector and another.
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    # Overloads the multiplication operator to scale the vector by a scalar.
    def __mul__(self, scalar):
        # Returns a new Vector3 which is this vector scaled by the scalar value.
        return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)

    # Overloads the true division operator to divide the vector by a scalar.
    def __truediv__(self, scalar):
        # Returns a new Vector3 which is this vector divided by the scalar value.
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    # Returns a string representation of the vector.
    def __str__(self):
        # Formats the x, y, and z components.
        return f"({self.x}, {self.y}, {self.z})"