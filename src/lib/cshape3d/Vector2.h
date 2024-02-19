
#ifndef __VECTOR2_H__
#define __VECTOR2_H__

class Vector2 {

    public:

        float x, y;

        Vector2() : x(0), y(0) {}

        Vector2(float x, float y) : x(x), y(y) {}

        Vector2 operator+(const Vector2& other) {
            return Vector2(x + other.x, y + other.y);
        }

        Vector2 operator-(const Vector2& other) {
            return Vector2(x - other.x, y - other.y);
        }

        Vector2 operator*(const float& scalar) {
            return Vector2(x * scalar, y * scalar);
        }

        Vector2 operator/(const float& scalar) {
            return Vector2(x / scalar, y / scalar);
        }

        bool operator==(const Vector2& other) {
            if (this == &other) return true;
            return x == other.x && y == other.y;
        }

        std::string toString() {
            return "Vector2(" + std::to_string(x) + ", " + std::to_string(y) + ")";
        }
};

#endif