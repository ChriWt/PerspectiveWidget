
#ifndef __VECTOR4_H__
#define __VECTOR4_H__

class Vector4 {

    public:
        float x, y, z, w;

        Vector4() : x(0), y(0), z(0), w(0) {}

        Vector4(float x, float y, float z, float w) : x(x), y(y), z(z), w(w) {}

        Vector4 operator+(const Vector4& other) {
            return Vector4(x + other.x, y + other.y, z + other.z, w + other.w);
        }

        Vector4 operator-(const Vector4& other) {
            return Vector4(x - other.x, y - other.y, z - other.z, w - other.w);
        }

        Vector4 operator*(const float& scalar) {
            return Vector4(x * scalar, y * scalar, z * scalar, w * scalar);
        }

        Vector4 operator/(const float& scalar) {
            return Vector4(x / scalar, y / scalar, z / scalar, w / scalar);
        }

        bool operator==(const Vector4& other) {
            if (this == &other) return true;
            return x == other.x && y == other.y && z == other.z && w == other.w;
        }

        std::string toString() {
            return "Vector4(" + std::to_string(x) + ", " + std::to_string(y) + ", " + std::to_string(z) + ", " + std::to_string(w) + ")";
        }
};

#endif