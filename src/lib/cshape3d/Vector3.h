#include <string>

#ifndef __VECTOR3_H__
#define __VECTOR3_H__

class Vector3 {

    public:
        float x, y, z;

        Vector3() : x(0), y(0), z(0) {}

        Vector3(float x, float y, float z) {
            this->x = x;
            this->y = y;
            this->z = z;
        }

        Vector3 operator+(const Vector3& other) {
            return Vector3(x + other.x, y + other.y, z + other.z);
        }

        Vector3 operator-(const Vector3& other) {
            return Vector3(x - other.x, y - other.y, z - other.z);
        }

        Vector3 operator*(const float& scalar) {
            return Vector3(x * scalar, y * scalar, z * scalar);
        }

        Vector3 operator/(const float& scalar) {
            return Vector3(x / scalar, y / scalar, z / scalar);
        }

        std::string toString() {
            return "Vector3(" + std::to_string(x) + ", " + std::to_string(y) + ", " + std::to_string(z) + ")";
        }

        bool operator==(const Vector3& other) {
            if (this == &other) return true;
            return x == other.x && y == other.y && z == other.z;
        }

        bool operator!=(const Vector3& other) {
            return !(*this == other);
        }
};

#endif