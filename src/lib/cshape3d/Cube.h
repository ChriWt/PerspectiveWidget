#include "Vector3.h"
#include "Shape3D.h"


class Cube: public Shape3D {

    private:

        static const int VERTICE_COUNT = 8;

        Vector3 calculateNearLeftUp() {
            Vector3 origin = getOrigin();
            return Vector3(origin.x - getWidth() / 2, origin.y + getHeight() / 2, origin.z - getDepth() / 2);
        }

        Vector3 calculateFarRightBottom() {
            Vector3 origin = getOrigin();
            return Vector3(origin.x + getWidth() / 2, origin.y - getHeight() / 2, origin.z + getDepth() / 2);
        }

    public:

        Cube() : Shape3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), VERTICE_COUNT, 0, 0, 0) {}

        Cube(Vector3 origin, Vector3 rotation, Vector3 translation, int width, int height, int depth): 
            Shape3D(origin, rotation, translation, VERTICE_COUNT, width, height, depth) {}

        Cube(Vector3 origin, int width, int height, int depth): 
            Shape3D(origin, Vector3(0, 0, 0), Vector3(0, 0, 0), VERTICE_COUNT, width, height, depth) {}

        Cube(Vector3 origin, int width): 
            Shape3D(origin, Vector3(0, 0, 0), Vector3(0, 0, 0), VERTICE_COUNT, width, width, width) {}

        std::vector<Vector3> getVertices() {
            Vector3 nearLeftUp = calculateNearLeftUp();
            Vector3 farRightBottom = calculateFarRightBottom();

            return {
                nearLeftUp,
                Vector3(nearLeftUp.x, farRightBottom.y, nearLeftUp.z),
                Vector3(farRightBottom.x, nearLeftUp.y, nearLeftUp.z),
                Vector3(farRightBottom.x, farRightBottom.y, nearLeftUp.z),
                farRightBottom,
                Vector3(nearLeftUp.x, farRightBottom.y, farRightBottom.z),
                Vector3(nearLeftUp.x, nearLeftUp.y, farRightBottom.z),
                Vector3(farRightBottom.x, nearLeftUp.y, farRightBottom.z)
            };
        }

        std::vector<std::tuple<int, int>> getEdges() {
            return {
                std::make_tuple(0, 1),
                std::make_tuple(1, 3),
                std::make_tuple(3, 2),
                std::make_tuple(2, 0),

                std::make_tuple(0, 6),
                std::make_tuple(6, 7),
                std::make_tuple(7, 2),
                std::make_tuple(2, 7),
                
                std::make_tuple(7, 4),
                std::make_tuple(4, 3),
                std::make_tuple(3, 4),
                std::make_tuple(4, 7),

                std::make_tuple(7, 4),
                std::make_tuple(4, 5),
                std::make_tuple(5, 1),
                std::make_tuple(1, 5),

                std::make_tuple(5, 4),
                std::make_tuple(5, 6),
            };
        }

        Shape3D* clone() {
            return new Cube(getOrigin(), getRotation(), getTranslation(), getWidth(), getHeight(), getDepth());
        }
};