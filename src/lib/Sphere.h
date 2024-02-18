
#if !defined(__VECTOR3_H__)
#define __VECTOR3_H__
#include "Vector3.h"
#endif

#if !defined(__SHAPE3D_H__)
#define __SHAPE3D_H__
#include "Shape3D.h"
#endif

class Sphere: public Shape3D {

    private:

        int getDefaultIfEmpty(int defaultValue, int value) {
            return value == 0 ? defaultValue : value;
        }

    public:
        Sphere() : Shape3D(Vector3(0, 0, 0), Vector3(0, 0, 0), Vector3(0, 0, 0), 0, 0, 0, 0) {}

        Sphere(Vector3 origin, Vector3 rotation, Vector3 translation, int verticeCount, int width, int height, int depth): 
            Shape3D(origin, rotation, translation, verticeCount, width, this->getDefaultIfEmpty(width, height), this->getDefaultIfEmpty(width, depth)) {}

        std::vector<Vector3> getVertices() {
            // TODO: Implement this method
            return std::vector<Vector3>();
        }

        std::vector<std::tuple<int, int>> getEdges() {
            // TODO: Implement this method
            return std::vector<std::tuple<int, int>>();
        }

};